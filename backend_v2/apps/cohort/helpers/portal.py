import logging
import re
import time

import requests
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def _notify_portal_invite_failure(
    *,
    participant,
    portal_onboarding_url: str,
    attempts: int,
    exc: BaseException | None,
    reason: str,
) -> None:
    recipients = list(getattr(settings, "OPERATIONS_ALERT_EMAILS", None) or [])
    if not recipients:
        return
    pid = getattr(participant, "id", None)
    email = getattr(participant, "email", "")
    lines = [
        f"Reason: {reason}",
        f"Participant ID: {pid}",
        f"Student email: {email}",
        f"Invite endpoint: {portal_onboarding_url}",
        f"Attempts: {attempts}",
    ]
    if exc is not None:
        lines.append(f"Error: {exc!s}")
    body = "\n".join(lines)
    try:
        send_mail(
            subject=f"[Web3Bridge] Portal onboarding invite failed (participant {pid})",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=True,
        )
    except Exception:
        logger.exception("Failed to send portal invite failure alert email")

_APPROVAL_STATUS_ALIASES: dict[str, str] = {
    "accepted": "approved",
    "approved": "approved",
    "active": "approved",
    "rejected": "rejected",
    "declined": "rejected",
    "revoked": "revoked",
    "suspended": "revoked",
    "pending": "pending",
    "in_review": "pending",
}


def _retryable_status_codes() -> set[int]:
    status_codes = getattr(
        settings, "PORTAL_REQUEST_RETRY_STATUS_CODES", (429, 500, 502, 503, 504)
    )
    return {int(code) for code in status_codes}


def _should_retry_request_error(exc: requests.RequestException) -> bool:
    if isinstance(exc, (requests.Timeout, requests.ConnectionError)):
        return True

    response = getattr(exc, "response", None)
    if response is None:
        return False

    return int(response.status_code) in _retryable_status_codes()


def is_zk_course_name(course_name):
    name_lc = (course_name or "").lower().strip()
    return bool(re.search(r"\bzk\b|\bzero[- ]?knowledge\b", name_lc))


def normalize_approval_status(raw_status):
    status_lc = (raw_status or "").lower().strip()
    if not status_lc:
        return "approved"
    return _APPROVAL_STATUS_ALIASES.get(status_lc, "approved")


def validate_participant_for_portal_invite(participant) -> tuple[bool, str]:
    """
    Return (eligible, reason) for sending a portal onboarding invite.

    Paid non-ZK participants may be invited or re-invited. Already-active portal
    accounts are reported as skipped by the portal API, not as validation errors.
    """
    email = (getattr(participant, "email", None) or "").strip()
    if not email:
        return False, "missing_email"

    if getattr(participant, "is_evicted", False):
        return False, "evicted"

    if not getattr(participant, "payment_status", False):
        return False, "unpaid"

    course = getattr(participant, "course", None)
    course_name = getattr(course, "name", "") if course is not None else ""
    if not course_name:
        return False, "missing_course"

    if is_zk_course_name(course_name):
        return False, "zk_course"

    status_value = (getattr(participant, "status", None) or "").upper()
    if status_value and status_value not in ("ACCEPTED", "APPROVED"):
        return False, "not_accepted"

    return True, ""


def _empty_portal_invite_result(*, reason: str) -> dict:
    return {
        "ok": False,
        "activation_url": None,
        "reason": reason,
        "portal_invite_created": False,
    }


def create_portal_onboarding_invite(participant):
    """
    Call portal_backend to create or resend an onboarding invite.

    Returns a dict with ``activation_url``, ``reason``, and ``portal_invite_created`` from
    the portal API, or ``ok=False`` when the request could not be completed.

    Not wired from ``handle_payment_success`` / verify-payment while the student portal is
    not publicly active—payment flows send only the standard course welcome mail.
    """
    course = getattr(participant, "course", None)
    course_name = getattr(course, "name", "")

    if is_zk_course_name(course_name):
        return _empty_portal_invite_result(reason="zk_course")

    portal_onboarding_url = (getattr(settings, "PORTAL_ONBOARDING_URL", "") or "").strip()
    internal_api_key = getattr(settings, "PORTAL_INTERNAL_API_KEY", "")
    read_timeout = float(getattr(settings, "PORTAL_REQUEST_TIMEOUT", 10))
    connect_timeout = float(getattr(settings, "PORTAL_REQUEST_CONNECT_TIMEOUT", 5))
    max_retries = max(0, int(getattr(settings, "PORTAL_REQUEST_MAX_RETRIES", 1)))
    backoff_seconds = float(
        getattr(settings, "PORTAL_REQUEST_RETRY_BACKOFF_SECONDS", 0.5)
    )
    wall_seconds = float(getattr(settings, "PORTAL_REQUEST_MAX_WALL_SECONDS", 24))
    deadline = time.monotonic() + wall_seconds

    if not portal_onboarding_url or not internal_api_key:
        logger.warning(
            "Portal onboarding invite skipped for participant %s because portal config is incomplete",
            getattr(participant, "id", None),
        )
        return _empty_portal_invite_result(reason="portal_not_configured")

    payload = {
        "email": participant.email,
        "full_name": participant.name,
        "cohort": participant.cohort,
        "course_name": course_name,
        "external_student_id": str(participant.id),
        "source_system": "backend_v2",
        "source_email": participant.email,
        "approval_status": normalize_approval_status(getattr(participant, "status", None)),
    }

    for attempt in range(max_retries + 1):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            logger.warning(
                "Portal onboarding invite aborted for participant %s: wall-clock budget exceeded "
                "(%ss) before attempt %s",
                getattr(participant, "id", None),
                wall_seconds,
                attempt + 1,
            )
            return _empty_portal_invite_result(reason="wall_clock_exceeded")
        # Stay under gunicorn worker timeout: shrink read timeout on the last slice of the budget.
        per_attempt_read = min(read_timeout, max(0.5, remaining))

        try:
            response = requests.post(
                portal_onboarding_url,
                json=payload,
                headers={"X-Internal-API-Key": internal_api_key},
                timeout=(connect_timeout, per_attempt_read),
            )
            response.raise_for_status()
            response_data = response.json()
            break
        except requests.RequestException as exc:
            is_last_attempt = attempt >= max_retries
            if is_last_attempt or not _should_retry_request_error(exc):
                logger.exception(
                    "Portal onboarding invite failed for participant %s after %s attempt(s)",
                    getattr(participant, "id", None),
                    attempt + 1,
                )
                _notify_portal_invite_failure(
                    participant=participant,
                    portal_onboarding_url=portal_onboarding_url,
                    attempts=attempt + 1,
                    exc=exc,
                    reason="request_failed",
                )
                return _empty_portal_invite_result(reason="request_failed")

            sleep_seconds = min(
                backoff_seconds * (2**attempt),
                max(0.0, deadline - time.monotonic()),
            )
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
        except ValueError as exc:
            logger.exception(
                "Portal onboarding invite returned non-JSON response for participant %s",
                getattr(participant, "id", None),
            )
            _notify_portal_invite_failure(
                participant=participant,
                portal_onboarding_url=portal_onboarding_url,
                attempts=attempt + 1,
                exc=exc,
                reason="invalid_json_response",
            )
            return _empty_portal_invite_result(reason="invalid_json_response")

    activation_url = response_data.get("activation_url")
    reason = response_data.get("reason")
    portal_invite_created = bool(response_data.get("portal_invite_created"))
    if not activation_url and reason in (
        "portal_invite_created",
        "portal_invite_resent",
    ):
        logger.warning(
            "Portal onboarding invite response missing activation_url for participant %s "
            "(reason=%s)",
            getattr(participant, "id", None),
            reason,
        )
    return {
        "ok": True,
        "activation_url": activation_url,
        "reason": reason,
        "portal_invite_created": portal_invite_created,
    }


def send_portal_invite_for_participant(participant) -> dict:
    """
    Validate and trigger a portal onboarding invite for one participant.

    Returns a dict suitable for admin API responses with keys:
    participant_id, email, sent, skipped, reason, activation_url, error.
    """
    participant_id = getattr(participant, "id", None)
    email = (getattr(participant, "email", None) or "").strip()

    eligible, skip_reason = validate_participant_for_portal_invite(participant)
    if not eligible:
        return {
            "participant_id": participant_id,
            "email": email,
            "sent": False,
            "skipped": True,
            "reason": skip_reason,
            "activation_url": None,
            "portal_invite_created": False,
            "error": skip_reason,
        }

    try:
        portal_result = create_portal_onboarding_invite(participant)
    except Exception as exc:  # noqa: BLE001
        logger.exception(
            "Unexpected portal invite failure for participant %s", participant_id
        )
        return {
            "participant_id": participant_id,
            "email": email,
            "sent": False,
            "skipped": False,
            "reason": "request_failed",
            "activation_url": None,
            "portal_invite_created": False,
            "error": str(exc),
        }

    if not portal_result.get("ok"):
        reason = portal_result.get("reason") or "portal_invite_failed"
        skipped = reason in (
            "portal_not_configured",
            "zk_course",
            "wall_clock_exceeded",
        )
        return {
            "participant_id": participant_id,
            "email": email,
            "sent": False,
            "skipped": skipped,
            "reason": reason,
            "activation_url": None,
            "portal_invite_created": False,
            "error": reason,
        }

    reason = portal_result.get("reason") or ""
    activation_url = portal_result.get("activation_url")
    portal_invite_created = bool(portal_result.get("portal_invite_created"))

    skipped_reasons = {
        "portal_invite_skipped_active_account",
        "portal_invite_skipped_suspended_account",
        "portal_invite_skipped_deactivated_account",
        "portal_invite_skipped_existing_account",
    }
    if reason in skipped_reasons:
        return {
            "participant_id": participant_id,
            "email": email,
            "sent": False,
            "skipped": True,
            "reason": reason,
            "activation_url": activation_url,
            "portal_invite_created": portal_invite_created,
            "error": reason,
        }

    sent = bool(activation_url) or reason in (
        "portal_invite_created",
        "portal_invite_resent",
    )
    return {
        "participant_id": participant_id,
        "email": email,
        "sent": sent,
        "skipped": not sent,
        "reason": reason or ("portal_invite_sent" if sent else "portal_invite_failed"),
        "activation_url": activation_url,
        "portal_invite_created": portal_invite_created,
        "error": None if sent else (reason or "portal_invite_failed"),
    }


def execute_portal_invite_bulk(*, participant_ids: list[int], queryset) -> dict:
    """Send portal invites for many participant IDs; ``queryset`` should be select_related."""
    participants = {p.id: p for p in queryset.filter(id__in=participant_ids)}

    results = []
    sent_count = 0
    skipped_count = 0
    failed_count = 0

    for participant_id in participant_ids:
        participant = participants.get(participant_id)
        if participant is None:
            row = {
                "participant_id": participant_id,
                "email": "",
                "sent": False,
                "skipped": False,
                "reason": "not_found",
                "activation_url": None,
                "portal_invite_created": False,
                "error": "not_found",
            }
            failed_count += 1
        else:
            row = send_portal_invite_for_participant(participant)
            if row.get("sent"):
                sent_count += 1
            elif row.get("skipped"):
                skipped_count += 1
            else:
                failed_count += 1
        results.append(row)

    return {
        "results": results,
        "sent_count": sent_count,
        "skipped_count": skipped_count,
        "failed_count": failed_count,
        "total": len(participant_ids),
    }
