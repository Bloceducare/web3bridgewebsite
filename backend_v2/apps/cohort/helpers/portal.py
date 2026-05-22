import logging
import re
import time
from datetime import date, datetime, time as dt_time, timedelta

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone
from utils.enums.models import RegistrationStatus

DEFAULT_PORTAL_INVITE_REGISTERED_FROM = date(2026, 4, 17)

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


def auto_accept_participant_on_payment(participant) -> bool:
    """
    Non-ZK participants are marked ACCEPTED when payment completes.
    ZK participants stay PENDING until an admin approves them.
    """
    course = getattr(participant, "course", None)
    course_name = getattr(course, "name", "") if course is not None else ""
    if is_zk_course_name(course_name):
        return False

    current_status = (getattr(participant, "status", None) or "").upper()
    if current_status == RegistrationStatus.REJECTED.value:
        return False

    if participant.status != RegistrationStatus.ACCEPTED.value:
        participant.status = RegistrationStatus.ACCEPTED.value
        return True

    return False


def normalize_approval_status(raw_status):
    status_lc = (raw_status or "").lower().strip()
    if not status_lc:
        return "approved"
    return _APPROVAL_STATUS_ALIASES.get(status_lc, "approved")


PORTAL_INVITE_VALIDATION_SKIP_REASONS = frozenset(
    {
        "missing_email",
        "evicted",
        "unpaid",
        "missing_course",
        "not_accepted",
        "rejected",
    }
)


def portal_invite_skip_message(reason: str) -> str:
    messages = {
        "missing_email": "Participant has no email address.",
        "evicted": "Participant was evicted and cannot receive a portal invite.",
        "unpaid": "Participant has not paid yet.",
        "missing_course": "Participant has no course assigned.",
        "not_accepted": (
            "ZK students must be approved (ACCEPTED) before a portal invite can be sent."
        ),
        "rejected": "Participant was rejected and cannot receive a portal invite.",
    }
    return messages.get(reason, f"Cannot send portal invite ({reason}).")


def validate_participant_for_portal_invite(participant) -> tuple[bool, str]:
    """
    Return (eligible, reason) for sending a portal onboarding invite.

    Paid non-ZK participants may be invited or re-invited without manual approval.
    ZK participants must be ACCEPTED (admin approve) before an invite is sent.
    Rejected registrations are always blocked. Already-active portal accounts are
    reported as skipped by the portal API, not as validation errors.
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

    status_value = (getattr(participant, "status", None) or "").upper()
    if status_value in ("REJECTED",):
        return False, "rejected"

    if is_zk_course_name(course_name):
        if status_value not in ("ACCEPTED", "APPROVED"):
            return False, "not_accepted"

    return True, ""


def _empty_portal_invite_result(*, reason: str) -> dict:
    return {
        "ok": False,
        "activation_url": None,
        "reason": reason,
        "portal_invite_created": False,
    }


def create_portal_onboarding_invite(participant, *, delivery_email: str | None = None):
    """
    Call portal_backend to create or resend an onboarding invite.

    Returns a dict with ``activation_url``, ``reason``, and ``portal_invite_created`` from
    the portal API, or ``ok=False`` when the request could not be completed.

    Not wired from ``handle_payment_success`` / verify-payment while the student portal is
    not publicly active—payment flows send only the standard course welcome mail.
    """
    course = getattr(participant, "course", None)
    course_name = getattr(course, "name", "") if course is not None else ""

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

    to_email = (delivery_email or participant.email or "").strip()
    payload = {
        "email": to_email,
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


def send_portal_invite_for_participant(
    participant,
    *,
    delivery_email: str | None = None,
    skip_validation: bool = False,
) -> dict:
    """
    Validate and trigger a portal onboarding invite for one participant.

    Returns a dict suitable for admin API responses with keys:
    participant_id, email, sent, skipped, reason, activation_url, error.
    """
    participant_id = getattr(participant, "id", None)
    email = (getattr(participant, "email", None) or "").strip()

    eligible, skip_reason = (
        (True, "")
        if skip_validation
        else validate_participant_for_portal_invite(participant)
    )
    if not eligible:
        message = portal_invite_skip_message(skip_reason)
        return {
            "participant_id": participant_id,
            "email": email,
            "sent": False,
            "skipped": True,
            "reason": skip_reason,
            "message": message,
            "activation_url": None,
            "portal_invite_created": False,
            "error": message,
        }

    try:
        portal_result = create_portal_onboarding_invite(
            participant, delivery_email=delivery_email
        )
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
    delivery = (delivery_email or email).strip()
    return {
        "participant_id": participant_id,
        "email": email,
        "delivery_email": delivery,
        "sent": sent,
        "skipped": not sent,
        "reason": reason or ("portal_invite_sent" if sent else "portal_invite_failed"),
        "activation_url": activation_url,
        "portal_invite_created": portal_invite_created,
        "error": None if sent else (reason or "portal_invite_failed"),
    }


def resolve_open_programme_cohort_labels() -> list[str]:
    """Cohort labels for current intake programmes (newest open reg per track)."""
    from .cohort_label import normalize_cohort_label, resolve_current_open_registration_ids
    from ..models import Registration

    reg_ids = resolve_current_open_registration_ids()
    if not reg_ids:
        return []

    labels: list[str] = []
    seen: set[str] = set()
    for registration in Registration.objects.filter(id__in=reg_ids).order_by(
        "-updated_at", "-id"
    ):
        for raw in (registration.cohort, registration.name):
            label = normalize_cohort_label(raw)
            if label and label not in seen:
                seen.add(label)
                labels.append(label)
    return labels


def describe_current_open_programmes() -> list[dict]:
    """Metadata for logging / management command output."""
    from .cohort_label import resolve_current_open_registration_ids
    from ..models import Registration

    reg_ids = resolve_current_open_registration_ids()
    programmes = []
    for registration in Registration.objects.filter(id__in=reg_ids).order_by(
        "-updated_at", "-id"
    ):
        programmes.append(
            {
                "id": registration.id,
                "name": registration.name,
                "cohort": registration.cohort or "",
                "is_open": registration.is_open,
            }
        )
    return programmes


def _paid_participant_base(queryset):
    return queryset.filter(payment_status=True, is_evicted=False).exclude(
        status=RegistrationStatus.REJECTED.value
    )


def parse_registered_from_date(value: str | date | None = None) -> date:
    if isinstance(value, date):
        return value
    raw = value or getattr(
        settings, "PORTAL_INVITE_REGISTERED_FROM", DEFAULT_PORTAL_INVITE_REGISTERED_FROM.isoformat()
    )
    return date.fromisoformat(str(raw).strip()[:10])


def _start_of_day(value: date) -> datetime:
    return timezone.make_aware(datetime.combine(value, dt_time.min))


def paid_participant_ids_for_registration_window(
    queryset,
    *,
    registered_from: date | None = None,
    registered_to: date | None = None,
    cohort_label: str | None = None,
) -> list[int]:
    """
    Paid participants by enrolment time (``participant.created_at``).

    Default window: registered on or after 2026-04-17 (current intake cutoff).
    """
    from_date = parse_registered_from_date(registered_from)
    qs = _paid_participant_base(queryset).filter(created_at__gte=_start_of_day(from_date))
    if registered_to is not None:
        qs = qs.filter(
            created_at__lt=_start_of_day(registered_to) + timedelta(days=1)
        )
    if (cohort_label or "").strip():
        qs = qs.filter(_cohort_text_match_q(cohort_label.strip()))
    rows = qs.order_by("-created_at", "-id").values_list("id", flat=True)
    return list(dict.fromkeys(rows))


def _cohort_text_match_q(*labels: str) -> Q:
    """Match ``participant.cohort`` with exact, normalized, and substring variants."""
    from .cohort_label import normalize_cohort_label

    combined = Q()
    for raw in labels:
        label = (raw or "").strip()
        if not label:
            continue
        combined |= Q(cohort__iexact=label) | Q(cohort__icontains=label)
        normalized = normalize_cohort_label(label)
        if normalized and normalized != label:
            combined |= Q(cohort__iexact=normalized) | Q(cohort__icontains=normalized)
        cohort_match = re.search(r"\bcohort\s*([ivxlcdm0-9]+)\b", label, flags=re.IGNORECASE)
        if cohort_match:
            token = cohort_match.group(1).upper()
            combined |= Q(cohort__icontains=token)
        master_match = re.search(
            r"master\s*class(?:\s*cohort)?\s*([ivxlcdm0-9]+)",
            label,
            flags=re.IGNORECASE,
        )
        if master_match:
            token = master_match.group(1).upper()
            combined |= Q(cohort__icontains=token) | Q(cohort__icontains="master")
    return combined


def paid_participant_ids_for_open_intake(queryset) -> list[int]:
    """
    Paid participants on the **current** open intake per track (newest ``is_open`` reg only).

    Requires ``participant.registration_id`` on that programme. When a course is set, it
    must belong to the same registration (aligned enrolment).
    """
    from .cohort_label import resolve_current_open_registration_ids

    open_reg_ids = resolve_current_open_registration_ids()
    if not open_reg_ids:
        return []

    rows = (
        _paid_participant_base(queryset)
        .filter(registration_id__in=open_reg_ids)
        .filter(Q(course_id__isnull=True) | Q(course__registration_id=F("registration_id")))
        .order_by("-created_at", "-id")
        .values_list("id", flat=True)
    )
    return list(dict.fromkeys(rows))


def _paid_participant_ids_for_all_open_registrations(queryset) -> list[int]:
    """Legacy broad selector (any ``is_open`` reg) — used only in breakdown stats."""
    from ..models import Registration

    open_reg_ids = list(
        Registration.objects.filter(is_open=True).values_list("id", flat=True)
    )
    if not open_reg_ids:
        return []
    intake_q = Q(registration_id__in=open_reg_ids) | Q(
        course__registration_id__in=open_reg_ids
    )
    rows = (
        _paid_participant_base(queryset)
        .filter(intake_q)
        .order_by("-created_at", "-id")
        .values_list("id", flat=True)
    )
    return list(dict.fromkeys(rows))


def paid_participant_ids_for_cohorts(queryset, cohort_labels: list[str]) -> list[int]:
    """Paid participants whose cohort label matches any of the given strings (fuzzy)."""
    if not cohort_labels:
        return []

    rows = (
        _paid_participant_base(queryset)
        .filter(_cohort_text_match_q(*cohort_labels))
        .order_by("-created_at", "-id")
        .values_list("id", flat=True)
    )
    return list(dict.fromkeys(rows))


def resolve_paid_participant_ids(
    queryset,
    *,
    cohort: str | None = None,
    all_paid: bool = False,
    registered_from: date | str | None = None,
    registered_to: date | str | None = None,
) -> tuple[list[int], str, dict]:
    """
    Return (participant_ids, selection_mode, selection_meta).

    Default: paid + registered on/after ``PORTAL_INVITE_REGISTERED_FROM`` (2026-04-17).
    """
    explicit = (cohort or "").strip()
    if all_paid:
        rows = (
            _paid_participant_base(queryset)
            .order_by("-created_at", "-id")
            .values_list("id", flat=True)
        )
        return list(dict.fromkeys(rows)), "all_paid", {}

    from_date = parse_registered_from_date(registered_from)
    to_date = None
    if registered_to:
        to_date = (
            registered_to
            if isinstance(registered_to, date)
            else date.fromisoformat(str(registered_to).strip()[:10])
        )

    ids = paid_participant_ids_for_registration_window(
        queryset,
        registered_from=from_date,
        registered_to=to_date,
        cohort_label=explicit or None,
    )
    mode = "registered_since_and_cohort" if explicit else "registered_since"
    return (
        ids,
        mode,
        {
            "registered_from": from_date.isoformat(),
            "registered_to": to_date.isoformat() if to_date else None,
            "cohort_filter": explicit or None,
        },
    )


def portal_invite_selection_breakdown(
    queryset,
    *,
    registered_from: date | str | None = None,
    registered_to: date | str | None = None,
) -> dict:
    """Counts for management command / API diagnostics."""
    from_date = parse_registered_from_date(registered_from)
    to_date = None
    if registered_to:
        to_date = (
            registered_to
            if isinstance(registered_to, date)
            else date.fromisoformat(str(registered_to).strip()[:10])
        )

    base = _paid_participant_base(queryset)
    window_ids = paid_participant_ids_for_registration_window(
        queryset,
        registered_from=from_date,
        registered_to=to_date,
    )
    return {
        "total_paid": base.count(),
        "registered_since_count": len(window_ids),
        "registered_from": from_date.isoformat(),
        "registered_to": to_date.isoformat() if to_date else None,
        "registration_field": "participant.created_at",
    }


def execute_portal_invite_for_paid_cohort(
    *,
    queryset,
    cohort: str | None = None,
    dry_run: bool = False,
    registered_from: date | str | None = None,
    registered_to: date | str | None = None,
) -> dict:
    """
    Send portal invites to every paid participant in a cohort.

    When ``cohort`` is omitted, uses paid participants registered on/after the configured
    registration cutoff date (default 2026-04-17).
    """
    participant_ids, selection_mode, selection_meta = resolve_paid_participant_ids(
        queryset,
        cohort=cohort,
        registered_from=registered_from,
        registered_to=registered_to,
    )

    breakdown = portal_invite_selection_breakdown(
        queryset,
        registered_from=registered_from,
        registered_to=registered_to,
    )

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "selection_mode": selection_mode,
            "selection": selection_meta,
            "participant_ids": participant_ids,
            "eligible_count": len(participant_ids),
            "breakdown": breakdown,
        }

    if not participant_ids:
        return {
            "ok": False,
            "reason": "no_participants",
            "message": (
                "No paid participants found for this registration window. "
                "Adjust PORTAL_INVITE_REGISTERED_FROM or pass --registered-from."
            ),
            "participant_ids": [],
            "eligible_count": 0,
            "selection_mode": selection_mode,
            "selection": selection_meta,
            "breakdown": breakdown,
        }

    summary = execute_portal_invite_bulk(
        participant_ids=participant_ids,
        queryset=queryset,
    )
    summary["ok"] = True
    summary["selection_mode"] = selection_mode
    summary["selection"] = selection_meta
    summary["eligible_count"] = len(participant_ids)
    summary["breakdown"] = portal_invite_selection_breakdown(queryset)
    return summary


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
