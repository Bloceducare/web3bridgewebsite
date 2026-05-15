"""mentor assessment questions + student results; drop generated_assessment blobs

Revision ID: 20260515_0008
Revises: 20260514_0007
Create Date: 2026-05-15 00:00:00.000000

"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op
from app.core.config import get_settings

revision = "20260515_0008"
down_revision = "20260514_0007"
branch_labels = None
depends_on = None

settings = get_settings()
schema_name = settings.POSTGRES_SCHEMA

_json_array_default = sa.text("'[]'::jsonb")
_json_object_default = sa.text("'{}'::jsonb")


def upgrade() -> None:
    op.add_column(
        "mentor_assessments",
        sa.Column(
            "questions",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=_json_array_default,
        ),
        schema=schema_name,
    )
    op.add_column(
        "mentor_assessments",
        sa.Column("duration_minutes", sa.Integer(), nullable=False, server_default=sa.text("60")),
        schema=schema_name,
    )
    op.add_column(
        "mentor_assessments",
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
        schema=schema_name,
    )
    op.add_column(
        "mentor_assessments",
        sa.Column("total_questions", sa.Integer(), nullable=False, server_default=sa.text("0")),
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_mentor_assessments_due_at"),
        "mentor_assessments",
        ["due_at"],
        unique=False,
        schema=schema_name,
    )

    op.drop_column("mentor_assessments", "generated_assessment", schema=schema_name)
    op.drop_column("mentor_assessments", "input_context", schema=schema_name)

    op.create_table(
        "assessment_results",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("mentor_assessment_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column(
            "responses",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=_json_object_default,
        ),
        sa.Column(
            "grading",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=_json_object_default,
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
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
            ["mentor_assessment_id"],
            [f"{schema_name}.mentor_assessments.id"],
            name=op.f("fk_assessment_results_mentor_assessment_id_mentor_assessments"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            [f"{schema_name}.users.id"],
            name=op.f("fk_assessment_results_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_assessment_results")),
        sa.UniqueConstraint(
            "mentor_assessment_id",
            "user_id",
            name="uq_assessment_result_per_student",
        ),
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_assessment_results_mentor_assessment_id"),
        "assessment_results",
        ["mentor_assessment_id"],
        unique=False,
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_assessment_results_user_id"),
        "assessment_results",
        ["user_id"],
        unique=False,
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_assessment_results_status"),
        "assessment_results",
        ["status"],
        unique=False,
        schema=schema_name,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_assessment_results_status"),
        table_name="assessment_results",
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_assessment_results_user_id"),
        table_name="assessment_results",
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_assessment_results_mentor_assessment_id"),
        table_name="assessment_results",
        schema=schema_name,
    )
    op.drop_table("assessment_results", schema=schema_name)

    op.add_column(
        "mentor_assessments",
        sa.Column(
            "input_context",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=_json_object_default,
        ),
        schema=schema_name,
    )
    op.add_column(
        "mentor_assessments",
        sa.Column(
            "generated_assessment",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=_json_object_default,
        ),
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_mentor_assessments_due_at"),
        table_name="mentor_assessments",
        schema=schema_name,
    )
    op.drop_column("mentor_assessments", "total_questions", schema=schema_name)
    op.drop_column("mentor_assessments", "due_at", schema=schema_name)
    op.drop_column("mentor_assessments", "duration_minutes", schema=schema_name)
    op.drop_column("mentor_assessments", "questions", schema=schema_name)
