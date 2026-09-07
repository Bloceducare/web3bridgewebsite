"""add attendance_codes and attendances tables

Revision ID: 20260721_0010
Revises: 20260618_0009
Create Date: 2026-07-21 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op
from app.core.config import get_settings

revision = "20260721_0010"
down_revision = "20260618_0009"
branch_labels = None
depends_on = None

settings = get_settings()
schema_name = settings.POSTGRES_SCHEMA


def upgrade() -> None:
    op.create_table(
        "attendance_codes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("programme", sa.String(length=255), nullable=False),
        sa.Column("track", sa.String(length=255), nullable=False),
        sa.Column("duration", sa.Integer(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("mentor_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["mentor_id"],
            [f"{schema_name}.mentors.id"],
            name=op.f("fk_attendance_codes_mentor_id_mentors"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_attendance_codes")),
        sa.UniqueConstraint("code", name=op.f("uq_attendance_codes_code")),
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_portal_attendance_codes_code"),
        "attendance_codes",
        ["code"],
        unique=True,
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_portal_attendance_codes_expires_at"),
        "attendance_codes",
        ["expires_at"],
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_portal_attendance_codes_is_active"),
        "attendance_codes",
        ["is_active"],
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_portal_attendance_codes_mentor_id"),
        "attendance_codes",
        ["mentor_id"],
        schema=schema_name,
    )

    op.create_table(
        "attendances",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("attendance_code_id", sa.Integer(), nullable=False),
        sa.Column("student_name", sa.String(length=255), nullable=False),
        sa.Column("date", sa.String(length=50), nullable=False),
        sa.Column("time", sa.String(length=50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["attendance_code_id"],
            [f"{schema_name}.attendance_codes.id"],
            name=op.f("fk_attendances_attendance_code_id_attendance_codes"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_attendances")),
        sa.UniqueConstraint("attendance_code_id", "student_name", name=op.f("uq_attendance_code_student")),
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_portal_attendances_attendance_code_id"),
        "attendances",
        ["attendance_code_id"],
        schema=schema_name,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_portal_attendances_attendance_code_id"),
        table_name="attendances",
        schema=schema_name,
    )
    op.drop_table("attendances", schema=schema_name)
    op.drop_index(
        op.f("ix_portal_attendance_codes_mentor_id"),
        table_name="attendance_codes",
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_portal_attendance_codes_is_active"),
        table_name="attendance_codes",
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_portal_attendance_codes_expires_at"),
        table_name="attendance_codes",
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_portal_attendance_codes_code"),
        table_name="attendance_codes",
        schema=schema_name,
    )
    op.drop_table("attendance_codes", schema=schema_name)
