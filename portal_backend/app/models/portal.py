from datetime import datetime
from enum import StrEnum

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import get_settings
from app.db.base import Base, TimestampMixin

settings = get_settings()
schema_prefix = f"{settings.POSTGRES_SCHEMA}."


class UserRole(StrEnum):
    STUDENT = "student"
    STAFF = "staff"
    ADMIN = "admin"
    MENTOR = "mentor"
    GENERAL_ADMIN = "general_admin"
    SYSTEM_ADMIN = "system_admin"


class AccountState(StrEnum):
    INVITED = "invited"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"


class OnboardingStatus(StrEnum):
    PENDING = "pending"
    INVITED = "invited"
    COMPLETED = "completed"


class ParticipationMode(StrEnum):
    ONSITE = "onsite"
    ONLINE = "online"


class ApprovalStatus(StrEnum):
    APPROVED = "approved"
    REVOKED = "revoked"
    REJECTED = "rejected"
    PENDING = "pending"


class UpdateTargetType(StrEnum):
    INDIVIDUAL = "individual"
    COHORT = "cohort"
    COURSE = "course"
    ALL_ACTIVE = "all_active"


class SyncJobStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class NotificationScope(StrEnum):
    PLATFORM = "platform"
    COURSE = "course"


class NotificationSenderType(StrEnum):
    MENTOR = "mentor"
    GENERAL_ADMIN = "general_admin"
    SYSTEM_ADMIN = "system_admin"


class CourseMaterialType(StrEnum):
    PDF = "pdf"
    VIDEO = "video"
    LINK = "link"
    DOC = "doc"
    TEXT = "text"


class AssessmentType(StrEnum):
    COMBINED = "combined"
    MULTIPLE_CHOICE = "multiple_choice"
    OPEN_ENDED = "open_ended"


class EvaluationMode(StrEnum):
    AI = "ai"
    MANUAL = "manual"


class ResultReleaseMode(StrEnum):
    IMMEDIATE = "immediate"
    MENTOR_CONTROLLED = "mentor_controlled"


class StudentAssessmentStatus(StrEnum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    GRADED = "graded"


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
    participation: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
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
    programme: Mapped[str | None] = mapped_column(String(255), nullable=True)
    track: Mapped[str | None] = mapped_column(String(255), nullable=True)
    target_role: Mapped[str | None] = mapped_column(String(50), nullable=True)



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


class Mentor(TimestampMixin, Base):
    __tablename__ = "mentors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey(f"{schema_prefix}users.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
        index=True,
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    programme: Mapped[str | None] = mapped_column(String(255), nullable=True)
    track: Mapped[str | None] = mapped_column(String(255), nullable=True)



class MentorCourseMap(TimestampMixin, Base):
    __tablename__ = "mentor_course_map"
    __table_args__ = (UniqueConstraint("mentor_id", "course_id", name="uq_mentor_course"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mentor_id: Mapped[int] = mapped_column(
        ForeignKey(f"{schema_prefix}mentors.id", ondelete="CASCADE"), nullable=False, index=True
    )
    course_id: Mapped[int] = mapped_column(nullable=False, index=True)


class CourseMaterial(TimestampMixin, Base):
    __tablename__ = "course_materials"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    material_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    resource_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    uploaded_by: Mapped[int | None] = mapped_column(
        ForeignKey(f"{schema_prefix}users.id", ondelete="SET NULL"), nullable=True
    )


class MentorAssessment(TimestampMixin, Base):
    """Mentor-authored assessment for a course. Publish via ``released_at``; students attempt via ``results``."""

    __tablename__ = "mentor_assessments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mentor_id: Mapped[int] = mapped_column(
        ForeignKey(f"{schema_prefix}mentors.id", ondelete="CASCADE"), nullable=False, index=True
    )
    course_id: Mapped[int] = mapped_column(nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    special_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    assessment_type: Mapped[str] = mapped_column(
        String(30), nullable=False, default=AssessmentType.MULTIPLE_CHOICE.value, index=True
    )
    evaluation_mode: Mapped[str] = mapped_column(
        String(20), nullable=False, default=EvaluationMode.AI.value, index=True
    )
    result_release_mode: Mapped[str] = mapped_column(
        String(30), nullable=False, default=ResultReleaseMode.MENTOR_CONTROLLED.value, index=True
    )
    accepted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    released_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    questions: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    results: Mapped[list["AssessmentResult"]] = relationship(back_populates="mentor_assessment")


class AssessmentResult(TimestampMixin, Base):
    """Per-student attempt linked to a mentor assessment (progress, score, responses)."""

    __tablename__ = "assessment_results"
    __table_args__ = (
        UniqueConstraint(
            "mentor_assessment_id",
            "user_id",
            name="uq_assessment_result_per_student",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mentor_assessment_id: Mapped[int] = mapped_column(
        ForeignKey(f"{schema_prefix}mentor_assessments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(f"{schema_prefix}users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=StudentAssessmentStatus.NOT_STARTED.value,
        index=True,
    )
    responses: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    grading: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    mentor_assessment: Mapped[MentorAssessment] = relationship(back_populates="results")
    user: Mapped[User] = relationship()


class GuarantorForm(TimestampMixin, Base):
    __tablename__ = "guarantor_forms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    form_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    cohort: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    uploaded_by: Mapped[int | None] = mapped_column(
        ForeignKey(f"{schema_prefix}users.id", ondelete="SET NULL"), nullable=True
    )


class AttendanceCode(TimestampMixin, Base):
    __tablename__ = "attendance_codes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    programme: Mapped[str] = mapped_column(String(255), nullable=False)
    track: Mapped[str] = mapped_column(String(255), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    mentor_id: Mapped[int] = mapped_column(
        ForeignKey(f"{schema_prefix}mentors.id", ondelete="CASCADE"), nullable=False, index=True
    )

    mentor: Mapped["Mentor"] = relationship()
    attendances: Mapped[list["Attendance"]] = relationship(
        back_populates="attendance_code", cascade="all, delete-orphan"
    )


class Attendance(TimestampMixin, Base):
    __tablename__ = "attendances"
    __table_args__ = (
        UniqueConstraint("attendance_code_id", "student_name", name="uq_attendance_code_student"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    attendance_code_id: Mapped[int] = mapped_column(
        ForeignKey(f"{schema_prefix}attendance_codes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    student_name: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[str] = mapped_column(String(50), nullable=False)
    time: Mapped[str] = mapped_column(String(50), nullable=False)

    attendance_code: Mapped["AttendanceCode"] = relationship(back_populates="attendances")

