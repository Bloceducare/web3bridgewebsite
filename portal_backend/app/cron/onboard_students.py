"""
Cron job: onboard paid non-ZK students from backend_v2.

Queries cohort_participant for ACCEPTED + paid students, creates portal
accounts, and sends activation emails.  Designed to be called by system
cron (e.g. every 5 minutes):

    python -m app.cron.onboard_students

Each run is tracked via ExternalSyncRecord so the next run only picks up
students updated since the last successful cursor.
"""

import asyncio
import logging
import re
from datetime import UTC, datetime

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import create_activation_token
from app.db.session import SessionLocal
from app.models.portal import (
    AccountState,
    ApprovalStatus,
    AuditLog,
    ExternalStudentMap,
    ExternalSyncRecord,
    OnboardingStatus,
    StudentProfile,
    StudentStatusHistory,
    SyncJobStatus,
    User,
    UserRole,
)
from app.services.email import EmailService
from app.services.status_mapping import normalize_approval_status

settings = get_settings()
logger = logging.getLogger(__name__)

JOB_NAME = "cron_onboard_students"

_ZK_PATTERN = re.compile(r"\bzk\b|\bzero[- ]?knowledge\b", re.IGNORECASE)


def _is_zk_course(course_name: str | None) -> bool:
    return bool(_ZK_PATTERN.search(course_name or ""))


def _build_activation_url(token: str) -> str:
    return f"{settings.PORTAL_FRONTEND_URL.rstrip('/')}/activate/onboard?token={token}"


async def _get_last_successful_cursor(session: AsyncSession) -> str | None:
    """Retrieve the cursor from the most recent successful run."""
    result = await session.execute(
        select(ExternalSyncRecord)
        .where(
            ExternalSyncRecord.job_name == JOB_NAME,
            ExternalSyncRecord.status == SyncJobStatus.SUCCESS.value,
        )
        .order_by(ExternalSyncRecord.ended_at.desc())
        .limit(1)
    )
    record = result.scalar_one_or_none()
    return record.cursor if record else None


async def _fetch_paid_non_zk_students(session: AsyncSession, *, cursor: str | None) -> list[dict]:
    """Query backend_v2 cohort_participant for paid, accepted students."""
    base_query = """
        SELECT
            p.id AS external_student_id,
            LOWER(TRIM(p.email)) AS email,
            p.name AS full_name,
            p.cohort AS cohort,
            c.name AS course_name,
            c.start_date AS course_start_date,
            p.number AS phone,
            p.wallet_address AS wallet_address,
            p.status AS source_status,
            p.payment_status AS payment_status,
            COALESCE(p.updated_at, p.created_at) AS source_updated_at
        FROM cohort_participant AS p
        LEFT JOIN cohort_course AS c ON c.id = p.course_id
        WHERE UPPER(p.status) = 'ACCEPTED'
          AND p.payment_status = TRUE
          {cursor_filter}
        ORDER BY COALESCE(p.updated_at, p.created_at) ASC, p.id ASC
    """

    if cursor:
        parsed = datetime.fromisoformat(cursor)
        cursor_dt = parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
        statement = text(
            base_query.format(cursor_filter="AND COALESCE(p.updated_at, p.created_at) > :cursor_dt")
        )
        result = await session.execute(statement, {"cursor_dt": cursor_dt})
    else:
        statement = text(base_query.format(cursor_filter=""))
        result = await session.execute(statement)

    return [dict(row._mapping) for row in result.all()]


async def _onboard_student(
    session: AsyncSession,
    student: dict,
    email_service: EmailService,
) -> str:
    """
    Create or update a portal user for a single student.
    Returns 'created', 'updated', or 'skipped'.
    """
    email = (student["email"] or "").strip().lower()
    full_name = (student["full_name"] or "").strip()
    external_id = str(student["external_student_id"])

    if not email or not full_name:
        logger.info(
            "Skipping portal onboarding for external_student_id=%s due to missing identity fields",
            external_id,
        )
        return "skipped"

    if _is_zk_course(student["course_name"]):
        logger.info(
            "Skipping portal onboarding for external_student_id=%s due to ZK course '%s'",
            external_id,
            student["course_name"],
        )
        return "skipped"

    # Check if already mapped
    result = await session.execute(
        select(ExternalStudentMap).where(ExternalStudentMap.external_student_id == external_id)
    )
    external_map = result.scalar_one_or_none()

    # Resolve existing user
    user = None
    if external_map is not None:
        result = await session.execute(select(User).where(User.id == external_map.user_id))
        user = result.scalar_one_or_none()
    if user is None:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

    created = False
    if user is None:
        user = User(
            email=email,
            role=UserRole.STUDENT.value,
            account_state=AccountState.INVITED.value,
        )
        session.add(user)
        await session.flush()
        created = True

        session.add(
            StudentStatusHistory(
                user_id=user.id,
                from_state=None,
                to_state=AccountState.INVITED.value,
                reason="cron_onboard_paid_student",
                changed_at=datetime.now(UTC),
            )
        )

    # Upsert profile
    result = await session.execute(select(StudentProfile).where(StudentProfile.user_id == user.id))
    profile = result.scalar_one_or_none()

    if profile is None:
        profile = StudentProfile(
            user_id=user.id,
            full_name=full_name,
            phone=student["phone"],
            wallet_address=student["wallet_address"],
            cohort=student["cohort"],
            onboarding_status=OnboardingStatus.INVITED.value,
        )
        session.add(profile)
    else:
        profile.full_name = full_name
        profile.phone = student["phone"]
        profile.wallet_address = student["wallet_address"]
        profile.cohort = student["cohort"]

    # Upsert external map
    source_email = email
    now = datetime.now(UTC)
    if external_map is None:
        normalized_approval_status = normalize_approval_status(
            student.get("source_status"),
            default=ApprovalStatus.APPROVED.value,
        )
        external_map = ExternalStudentMap(
            user_id=user.id,
            source_system="backend_v2",
            external_student_id=external_id,
            source_email=source_email,
            approval_status=normalized_approval_status,
            approval_updated_at=student["source_updated_at"],
            last_synced_at=now,
        )
        session.add(external_map)
    else:
        normalized_approval_status = normalize_approval_status(
            student.get("source_status"),
            default=ApprovalStatus.APPROVED.value,
        )
        external_map.user_id = user.id
        external_map.source_email = source_email
        external_map.approval_status = normalized_approval_status
        external_map.approval_updated_at = student["source_updated_at"]
        external_map.last_synced_at = now

    # Send activation email only for newly created users
    if created:
        token, token_jti, expires_at = create_activation_token(user_id=user.id, email=user.email)
        user.activation_token_jti = token_jti
        user.activation_token_expires_at = expires_at

        activation_url = _build_activation_url(token)
        try:
            class_start_date = student.get("course_start_date")
            if isinstance(class_start_date, datetime):
                class_start_date = class_start_date.date()
            await email_service.send_onboarding_email(
                to_email=email,
                student_name=full_name,
                activation_url=activation_url,
                class_start_date=class_start_date,
            )
        except Exception:
            logger.exception("Failed to send onboarding email to %s", email)

    session.add(
        AuditLog(
            actor_user_id=None,
            action="cron_onboard_upserted" if not created else "cron_onboard_created",
            resource_type="user",
            resource_id=str(user.id),
            after_json={
                "external_student_id": external_id,
                "email": email,
                "cohort": student["cohort"],
                "course_name": student["course_name"],
            },
            created_at=now,
        )
    )

    result_state = "created" if created else "updated"
    logger.info(
        "Portal onboarding %s for external_student_id=%s email=%s user_id=%s",
        result_state,
        external_id,
        email,
        user.id,
    )
    return result_state


async def run_onboard_cron() -> dict:
    """Main cron entry point. Returns a summary dict."""
    email_service = EmailService()

    started_at = datetime.now(UTC)
    async with SessionLocal() as session:
        cursor = await _get_last_successful_cursor(session)

        # Create a sync record to track this run
        record = ExternalSyncRecord(
            job_name=JOB_NAME,
            cursor=cursor,
            status=SyncJobStatus.RUNNING.value,
            started_at=datetime.now(UTC),
        )
        session.add(record)
        await session.flush()

        try:
            students = await _fetch_paid_non_zk_students(session, cursor=cursor)

            created = 0
            updated = 0
            skipped = 0

            for student in students:
                result = await _onboard_student(session, student, email_service)
                if result == "created":
                    created += 1
                elif result == "updated":
                    updated += 1
                else:
                    skipped += 1

            # Update cursor to latest student timestamp
            next_cursor = cursor
            if students:
                last_ts = students[-1]["source_updated_at"]
                next_cursor = last_ts.isoformat() if last_ts else cursor

            record.status = SyncJobStatus.SUCCESS.value
            record.cursor = next_cursor
            record.ended_at = datetime.now(UTC)
            record.error_payload = None

            await session.commit()

            ended_at = datetime.now(UTC)
            lag_seconds = None
            if students and students[-1]["source_updated_at"] is not None:
                lag_seconds = max(
                    0.0,
                    (ended_at - students[-1]["source_updated_at"]).total_seconds(),
                )
                if lag_seconds >= settings.ONBOARD_CURSOR_LAG_WARNING_SECONDS:
                    logger.warning(
                        "Onboard cursor lag is high: %.2f seconds (threshold=%s)",
                        lag_seconds,
                        settings.ONBOARD_CURSOR_LAG_WARNING_SECONDS,
                    )

            summary = {
                "job_name": JOB_NAME,
                "integration_mode": "db_coupled_cron",
                "source_system": "backend_v2",
                "processed": len(students),
                "created": created,
                "updated": updated,
                "skipped": skipped,
                "cursor": next_cursor,
                "started_at": started_at.isoformat(),
                "ended_at": ended_at.isoformat(),
                "duration_seconds": max(0.0, (ended_at - started_at).total_seconds()),
                "cursor_lag_seconds": lag_seconds,
            }
            logger.info("Cron onboard completed: %s", summary)
            return summary

        except Exception as exc:
            await session.rollback()
            record.status = SyncJobStatus.FAILED.value
            record.ended_at = datetime.now(UTC)
            record.error_payload = {"message": str(exc)}
            await session.commit()
            logger.exception("Cron onboard failed")
            raise


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    result = asyncio.run(run_onboard_cron())
    print(f"Done: {result}")


if __name__ == "__main__":
    main()
