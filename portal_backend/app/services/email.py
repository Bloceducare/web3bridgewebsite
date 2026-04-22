import logging
from email.message import EmailMessage

import aiosmtplib

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class EmailService:
    """Async email service using aiosmtplib.

    All public methods are fire-and-forget safe — they log errors but never
    raise, so callers don't need to wrap them in try/except.
    """

    def __init__(
        self,
        *,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        use_tls: bool | None = None,
        from_email: str | None = None,
    ) -> None:
        self.host = host or settings.EMAIL_HOST
        self.port = port or settings.EMAIL_PORT
        self.username = username or settings.EMAIL_HOST_USER
        self.password = password or settings.EMAIL_HOST_PASSWORD
        self.use_tls = use_tls if use_tls is not None else settings.EMAIL_USE_TLS
        self.from_email = (
            from_email or settings.ADMISSION_EMAIL_HOST_USER or settings.DEFAULT_FROM_EMAIL
        )

    async def send_email(
        self,
        *,
        to_email: str,
        subject: str,
        html_body: str,
    ) -> bool:
        """Send an HTML email. Returns True on success, False on failure."""
        if not self.username or not self.password:
            logger.warning("Email not sent to %s — SMTP credentials not configured", to_email)
            return False

        message = EmailMessage()
        message["From"] = self.from_email
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content("Please view this email in an HTML-capable client.", subtype="plain")
        message.add_alternative(html_body, subtype="html")

        try:
            await aiosmtplib.send(
                message,
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                start_tls=self.use_tls,
            )
            logger.info("Onboarding email sent successfully to %s", to_email)
            return True
        except aiosmtplib.SMTPException:
            logger.exception("SMTP error sending email to %s", to_email)
            return False
        except Exception:
            logger.exception("Unexpected error sending email to %s", to_email)
            return False

    async def send_onboarding_email(
        self,
        *,
        to_email: str,
        student_name: str,
        activation_url: str,
    ) -> bool:
        """Send the portal onboarding/activation email to a student."""
        from app.services.templates.onboarding_email import render_onboarding_email

        subject, html_body = render_onboarding_email(
            name=student_name, activation_url=activation_url
        )
        return await self.send_email(to_email=to_email, subject=subject, html_body=html_body)

    async def send_verification_email(
        self,
        *,
        to_email: str,
        student_name: str,
        code: str,
    ) -> bool:
        """Send a 6-digit email verification code to a student."""
        from app.services.templates.verification_email import render_verification_email

        subject, html_body = render_verification_email(name=student_name, code=code)
        return await self.send_email(to_email=to_email, subject=subject, html_body=html_body)

    async def send_update_notification_email(
        self,
        *,
        to_email: str,
        title: str,
        body: str,
    ) -> bool:
        """Send a portal in-app notification as email."""
        from app.services.templates.update_notification_email import (
            render_update_notification_email,
        )

        subject, html_body = render_update_notification_email(title=title, body=body)
        return await self.send_email(to_email=to_email, subject=subject, html_body=html_body)
