from datetime import datetime
from enum import StrEnum

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import get_settings
from app.db.base import Base, TimestampMixin

settings = get_settings()
schema_prefix = f"{settings.POSTGRES_SCHEMA}."


class UserRole(StrEnum):
    STUDENT = "student"
    STAFF = "staff"
    ADMIN = "admin"


class AccountState(StrEnum):
    INVITED = "invited"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"


class OnboardingStatus(StrEnum):
    PENDING = "pending"
    INVITED = "invited"
    COMPLETED = "completed"


class ApprovalStatus(StrEnum):
    APPROVED = "approved"
    REVOKED = "revoked"
    REJECTED = "rejected"
    PENDING = "pending"


class UpdateTargetType(StrEnum):
    INDIVIDUAL = "individual"
    COHORT = "cohort"
    ALL_ACTIVE = "all_active"


class SyncJobStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default=UserRole.STUDENT.value)
    account_state: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=AccountState.INVITED.value,
        index=True,
    )
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    email_verification_code: Mapped[str | None] = mapped_column(String(6), nullable=True)
    email_verification_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    activation_token_jti: Mapped[str | None] = mapped_column(String(255), nullable=True)
    activation_token_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    profile: Mapped["StudentProfile | None"] = relationship(back_populates="user", uselist=False)


class StudentProfile(TimestampMixin, Base):
    __tablename__ = "student_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(f"{schema_prefix}users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    discord_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    discord_invite_link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    discord_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    wallet_address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cohort: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    onboarding_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=OnboardingStatus.PENDING.value,
        index=True,
    )
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped[User] = relationship(back_populates="profile")


class ExternalStudentMap(TimestampMixin, Base):
    __tablename__ = "external_student_map"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(f"{schema_prefix}users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_system: Mapped[str] = mapped_column(String(100), nullable=False, default="backend_v2")
    external_student_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    source_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    approval_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=ApprovalStatus.PENDING.value,
        index=True,
    )
    approval_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class StudentStatusHistory(Base):
    __tablename__ = "student_status_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(f"{schema_prefix}users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    from_state: Mapped[str | None] = mapped_column(String(20), nullable=True)
    to_state: Mapped[str] = mapped_column(String(20), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    changed_by: Mapped[int | None] = mapped_column(
        ForeignKey(f"{schema_prefix}users.id", ondelete="SET NULL"),
        nullable=True,
    )
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class StudentUpdate(TimestampMixin, Base):
    __tablename__ = "student_updates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    target_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    target_ref: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    send_in_app: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    send_email: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey(f"{schema_prefix}users.id", ondelete="SET NULL"),
        nullable=True,
    )


class StudentUpdateRead(Base):
    __tablename__ = "student_update_reads"
    __table_args__ = (UniqueConstraint("update_id", "user_id", name="uq_update_read_per_user"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    update_id: Mapped[int] = mapped_column(
        ForeignKey(f"{schema_prefix}student_updates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(f"{schema_prefix}users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    read_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(f"{schema_prefix}users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    jti: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ExternalSyncRecord(Base):
    __tablename__ = "external_sync_record"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    job_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    cursor: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=SyncJobStatus.PENDING.value,
        index=True,
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    actor_user_id: Mapped[int | None] = mapped_column(
        ForeignKey(f"{schema_prefix}users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    before_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    after_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
