import logging
import re
import time

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _admission_smtp_configured() -> bool:
    """Use admission SMTP only when both credentials are non-empty."""
    user = getattr(settings, "ADMISSION_EMAIL_HOST_USER", None)
    password = getattr(settings, "ADMISSION_EMAIL_HOST_PASSWORD", None)
    return bool(user and password)


def _admission_from_email() -> str:
    """From-address for admission mail; avoids None when ADMISSION_EMAIL_* is unset."""
    addr = getattr(settings, "ADMISSION_EMAIL_HOST_USER", None)
    if addr:
        return addr
    default = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    return default or "admission@web3bridge.com"


def _operations_alert_recipients() -> list[str]:
    raw = getattr(settings, "OPERATIONS_ALERT_EMAILS", None) or []
    return [r for r in raw if r]


def _notify_registration_welcome_failure(
    *,
    email: str,
    course_id,
    participant_display: str,
    attempts: int,
    exc: BaseException | None,
    reason: str,
) -> None:
    """Email ops when the post-payment registration welcome mail cannot be delivered."""
    recipients = _operations_alert_recipients()
    if not recipients:
        return
    lines = [
        f"Reason: {reason}",
        f"Student email: {email}",
        f"Course ID: {course_id}",
        f"Participant: {participant_display}",
        f"Send attempts: {attempts}",
    ]
    if exc is not None:
        lines.append(f"Error: {exc!s}")
    body = "\n".join(lines)
    try:
        send_mail(
            subject="[Web3Bridge] Registration welcome email (post-payment) failed",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=True,
        )
    except Exception:
        logger.exception(
            "Failed to send registration welcome failure alert to operations"
        )


# Testimonial image storage location


def testimonial_image_location(instance, filename):
    full_name_processed = instance.full_name.replace(" ", "_")
    return f"{settings.ENVIROMENT}/Testimonial/{full_name_processed}/{filename}"


def _web2_registration_template_and_subject(course_name):
    """
    Map Web2 course titles to welcome email template and subject.
    Order: specific tracks before generic Web2 / Launchpad fallback.
    """
    name_lc = (course_name or "").lower()
    if "advanced backend" in name_lc:
        return (
            "cohort/web2_advanced_backend_registration_email.html",
            "Welcome to Web2 Advanced Backend – Web3Bridge",
        )
    if "advanced frontend" in name_lc:
        return (
            "cohort/web2_advanced_frontend_registration_email.html",
            "Welcome to Web2 Advanced Frontend – Web3Bridge",
        )
    if "launchpad" in name_lc:
        return (
            "cohort/web2_launchpad_registration_email.html",
            "Welcome to Web2 Launchpad – Web3Bridge",
        )
    return (
        "cohort/web2_launchpad_registration_email.html",
        "Welcome to Web2 Launchpad – Web3Bridge",
    )


def _build_registration_success_email_message(
    email, course_id, participant, activation_url=None
):
    """
    Build the post-payment registration welcome email (does not send).

    Raises ``cohort.models.Course.DoesNotExist`` when ``course_id`` is invalid.
    """
    from cohort.models import Course
    from django.core.mail import get_connection

    course = Course.objects.get(pk=course_id)
    name_lc = (course.name or "").lower()
    is_zk = bool(re.search(r"\bzk\b|\bzero[- ]?knowledge\b", name_lc))

    if re.search(r"\brust\b", name_lc):
        subject = "Rust Masterclass Registration Success"
        template_name = "cohort/rust_registration_email.html"
        context = {
            "name": participant,
            "activation_url": None if is_zk else activation_url,
        }
    elif re.search(r"\bweb2\b", name_lc):
        template_name, subject = _web2_registration_template_and_subject(course.name)
        context = {}
    elif re.search(r"\bweb3\b", name_lc):
        subject = "Web3 Registration Success"
        template_name = "cohort/web3_registration_email.html"
        context = {
            "name": participant,
            "activation_url": None if is_zk else activation_url,
        }
    elif is_zk:
        subject = "🎉 Welcome to the Web3Bridge Zero Knowledge Program!"
        template_name = "cohort/zk_registration_email.html"
        context = {"name": participant}
    else:
        subject = f"{course.name} Registration Success"
        template_name = "other_registration_email.html"
        context = {
            "name": participant,
            "activation_url": None if is_zk else activation_url,
        }
    message = render_to_string(template_name, context)

    from_email = _admission_from_email()
    email_msg = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=[email],
    )
    email_msg.content_subtype = "html"

    if _admission_smtp_configured():
        connection = get_connection(
            host=getattr(settings, "ADMISSION_EMAIL_HOST", settings.EMAIL_HOST),
            port=getattr(settings, "ADMISSION_EMAIL_PORT", settings.EMAIL_PORT),
            username=getattr(settings, "ADMISSION_EMAIL_HOST_USER"),
            password=getattr(settings, "ADMISSION_EMAIL_HOST_PASSWORD"),
            use_tls=getattr(
                settings, "ADMISSION_EMAIL_USE_TLS", settings.EMAIL_USE_TLS
            ),
        )
        email_msg.connection = connection

    return email_msg


def send_registration_success_mail(email, course_id, participant, activation_url=None):
    """
    Send the post-payment registration welcome email with retries, then alert ops on failure.
    """
    from cohort.models import Course

    try:
        email_msg = _build_registration_success_email_message(
            email, course_id, participant, activation_url=activation_url
        )
    except Course.DoesNotExist:
        return
    except Exception as exc:
        logger.exception(
            "registration welcome email build failed email=%s course_id=%s",
            email,
            course_id,
        )
        _notify_registration_welcome_failure(
            email=email,
            course_id=course_id,
            participant_display=str(participant),
            attempts=0,
            exc=exc,
            reason="failed to build registration welcome email (template or data error)",
        )
        return

    max_retries = max(
        1, int(getattr(settings, "REGISTRATION_WELCOME_EMAIL_MAX_RETRIES", 3))
    )
    backoff = float(
        getattr(settings, "REGISTRATION_WELCOME_EMAIL_RETRY_BACKOFF_SECONDS", 1.0)
    )
    last_exc: BaseException | None = None
    for attempt in range(max_retries):
        try:
            email_msg.send(fail_silently=False)
            return
        except Exception as exc:
            last_exc = exc
            logger.warning(
                "registration welcome email send attempt %s/%s failed for %s: %s",
                attempt + 1,
                max_retries,
                email,
                exc,
            )
            if attempt < max_retries - 1:
                time.sleep(backoff)
                try:
                    email_msg = _build_registration_success_email_message(
                        email, course_id, participant, activation_url=activation_url
                    )
                except Exception as rebuild_exc:
                    logger.exception(
                        "registration welcome email rebuild failed after send error "
                        "email=%s course_id=%s",
                        email,
                        course_id,
                    )
                    _notify_registration_welcome_failure(
                        email=email,
                        course_id=course_id,
                        participant_display=str(participant),
                        attempts=attempt + 1,
                        exc=rebuild_exc,
                        reason="rebuild failed after SMTP error (transient)",
                    )
                    return

    _notify_registration_welcome_failure(
        email=email,
        course_id=course_id,
        participant_display=str(participant),
        attempts=max_retries,
        exc=last_exc,
        reason="SMTP send failed after all retries",
    )


def send_participant_details(email, course_id, participant):
    """
    Legacy no-op. Registration details are available in the student portal; we no longer
    email duplicate participant data.
    """
    return


def send_reschedule_assessment_email(email, name, cohort, assessment_link):
    """
    Send an assessment rescheduled notification to a student.
    Includes a CTA button with the assessment link and a 3-day deadline notice.
    """
    try:
        context = {
            "name": name,
            "cohort": cohort,
            "assessment_link": assessment_link,
        }
        message = render_to_string("cohort/reschedule_assessment_email.html", context)

        subject = f"Your Assessment Has Been Rescheduled – {cohort}"
        from_email = _admission_from_email()

        email_msg = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[email],
        )
        email_msg.content_subtype = "html"

        if _admission_smtp_configured():
            from django.core.mail import get_connection

            connection = get_connection(
                host=getattr(settings, "ADMISSION_EMAIL_HOST", settings.EMAIL_HOST),
                port=getattr(settings, "ADMISSION_EMAIL_PORT", settings.EMAIL_PORT),
                username=getattr(settings, "ADMISSION_EMAIL_HOST_USER"),
                password=getattr(settings, "ADMISSION_EMAIL_HOST_PASSWORD"),
                use_tls=getattr(
                    settings, "ADMISSION_EMAIL_USE_TLS", settings.EMAIL_USE_TLS
                ),
            )
            email_msg.connection = connection

        email_msg.send(fail_silently=False)
    except Exception:
        pass


def send_approval_email(participant, payment_link: str | None = None):
    """
    Send approval emails by course. For ZK courses, include a payment link.
    """
    try:
        course_name = participant.course.name or ""
        name_lc = course_name.lower()
        recipient_email = participant.email
        participant_name = participant.name

        # Detect ZK
        is_zk = bool(re.search(r"\bzk\b|\bzero[- ]?knowledge\b", name_lc))

        if is_zk:
            subject = "You’re Approved – Proceed to Payment (Web3Bridge ZK Program)"
            template_name = "cohort/zk_approval_email.html"
            link = payment_link or "https://payment.web3bridgeafrica.com"
            context = {
                "name": participant_name,
                "payment_link": link,
                "course_name": course_name,
            }
        else:
            subject = f"You’re Approved for {course_name} – Next Steps"
            template_name = "cohort/approval_email.html"
            context = {"name": participant_name, "course_name": course_name}

        message = render_to_string(template_name, context)

        from_email = _admission_from_email()
        email_msg = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[recipient_email],
        )
        email_msg.content_subtype = "html"

        if _admission_smtp_configured():
            from django.core.mail import get_connection

            connection = get_connection(
                host=getattr(settings, "ADMISSION_EMAIL_HOST", settings.EMAIL_HOST),
                port=getattr(settings, "ADMISSION_EMAIL_PORT", settings.EMAIL_PORT),
                username=getattr(settings, "ADMISSION_EMAIL_HOST_USER"),
                password=getattr(settings, "ADMISSION_EMAIL_HOST_PASSWORD"),
                use_tls=getattr(
                    settings, "ADMISSION_EMAIL_USE_TLS", settings.EMAIL_USE_TLS
                ),
            )
            email_msg.connection = connection

        email_msg.send(fail_silently=True)
    except Exception:
        pass


def _format_assessment_breakdown(breakdown):
    """Format breakdown for HTML email: readable lines only, never raw API/JSON dumps."""
    meta_keys = frozenset({"email", "score", "passed"})

    if breakdown in (None, "", {}, []):
        return None

    def _humanize_key(key):
        return str(key).replace("_", " ").strip().title()

    if isinstance(breakdown, dict):
        filtered = {
            k: v for k, v in breakdown.items() if str(k).lower() not in meta_keys
        }
        if not filtered:
            return None
        lines = []
        for k, v in filtered.items():
            if isinstance(v, dict):
                inner = ", ".join(f"{_humanize_key(ik)}: {iv}" for ik, iv in v.items())
                lines.append(f"{_humanize_key(k)}: {inner}")
            elif isinstance(v, list):
                lines.append(f"{_humanize_key(k)}: {', '.join(map(str, v))}")
            else:
                lines.append(f"{_humanize_key(k)}: {v}")
        return "\n".join(lines)

    if isinstance(breakdown, list):
        return "\n".join(str(x) for x in breakdown) if breakdown else None

    return str(breakdown)


def send_assessment_passed_email(email, name, cohort, score, breakdown=None):
    """Send welcome / onboarding next-steps email when a participant passes the assessment (submit-assessment only)."""
    try:
        context = {"name": name}
        message = render_to_string("cohort/assessment_passed_email.html", context)
        subject = f"Welcome to Web3Bridge – {cohort}" if cohort else "Welcome to Web3Bridge"
        from_email = _admission_from_email()

        email_msg = EmailMessage(subject=subject, body=message, from_email=from_email, to=[email])
        email_msg.content_subtype = "html"

        if _admission_smtp_configured():
            from django.core.mail import get_connection
            connection = get_connection(
                host=getattr(settings, "ADMISSION_EMAIL_HOST", settings.EMAIL_HOST),
                port=getattr(settings, "ADMISSION_EMAIL_PORT", settings.EMAIL_PORT),
                username=getattr(settings, "ADMISSION_EMAIL_HOST_USER"),
                password=getattr(settings, "ADMISSION_EMAIL_HOST_PASSWORD"),
                use_tls=getattr(settings, "ADMISSION_EMAIL_USE_TLS", settings.EMAIL_USE_TLS),
            )
            email_msg.connection = connection

        email_msg.send(fail_silently=False)
    except Exception:
        pass


def send_assessment_failed_email(email, name, cohort, score, breakdown=None):
    """Send an encouraging email when a participant fails their assessment."""
    try:
        context = {
            "name": name,
            "cohort": cohort,
            "score": score,
            "breakdown_display": _format_assessment_breakdown(breakdown),
        }
        message = render_to_string("cohort/assessment_failed_email.html", context)
        subject = f"Your Web3Bridge Assessment Result – {cohort}"
        from_email = _admission_from_email()

        email_msg = EmailMessage(subject=subject, body=message, from_email=from_email, to=[email])
        email_msg.content_subtype = "html"

        if _admission_smtp_configured():
            from django.core.mail import get_connection
            connection = get_connection(
                host=getattr(settings, "ADMISSION_EMAIL_HOST", settings.EMAIL_HOST),
                port=getattr(settings, "ADMISSION_EMAIL_PORT", settings.EMAIL_PORT),
                username=getattr(settings, "ADMISSION_EMAIL_HOST_USER"),
                password=getattr(settings, "ADMISSION_EMAIL_HOST_PASSWORD"),
                use_tls=getattr(settings, "ADMISSION_EMAIL_USE_TLS", settings.EMAIL_USE_TLS),
            )
            email_msg.connection = connection

        email_msg.send(fail_silently=False)
    except Exception:
        pass
