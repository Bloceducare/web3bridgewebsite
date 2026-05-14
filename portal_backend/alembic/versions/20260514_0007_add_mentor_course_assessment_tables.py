"""add mentor, course materials, guarantor forms, assessments

Revision ID: 20260514_0007
Revises: 20260422_0006
Create Date: 2026-05-14 00:00:00.000000

"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op
from app.core.config import get_settings

revision = "20260514_0007"
down_revision = "20260422_0006"
branch_labels = None
depends_on = None

settings = get_settings()
schema_name = settings.POSTGRES_SCHEMA

_json_object_default = sa.text("'{}'::jsonb")


def upgrade() -> None:
    op.create_table(
        "mentors",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
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
            ["user_id"],
            [f"{schema_name}.users.id"],
            name=op.f("fk_mentors_user_id_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_mentors")),
        sa.UniqueConstraint("user_id", name=op.f("uq_mentors_user_id")),
        sa.UniqueConstraint("email", name=op.f("uq_mentors_email")),
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_mentors_is_active"),
        "mentors",
        ["is_active"],
        unique=False,
        schema=schema_name,
    )

    op.create_table(
        "mentor_course_map",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("mentor_id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
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
            name=op.f("fk_mentor_course_map_mentor_id_mentors"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_mentor_course_map")),
        sa.UniqueConstraint("mentor_id", "course_id", name="uq_mentor_course"),
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_mentor_course_map_course_id"),
        "mentor_course_map",
        ["course_id"],
        unique=False,
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_mentor_course_map_mentor_id"),
        "mentor_course_map",
        ["mentor_id"],
        unique=False,
        schema=schema_name,
    )

    op.create_table(
        "mentor_assessments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("mentor_id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("special_prompt", sa.Text(), nullable=True),
        sa.Column(
            "input_context",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=_json_object_default,
        ),
        sa.Column(
            "generated_assessment",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=_json_object_default,
        ),
        sa.Column("assessment_type", sa.String(length=30), nullable=False),
        sa.Column("evaluation_mode", sa.String(length=20), nullable=False),
        sa.Column("result_release_mode", sa.String(length=30), nullable=False),
        sa.Column(
            "accepted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
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
            name=op.f("fk_mentor_assessments_mentor_id_mentors"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_mentor_assessments")),
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_mentor_assessments_accepted"),
        "mentor_assessments",
        ["accepted"],
        unique=False,
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_mentor_assessments_assessment_type"),
        "mentor_assessments",
        ["assessment_type"],
        unique=False,
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_mentor_assessments_course_id"),
        "mentor_assessments",
        ["course_id"],
        unique=False,
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_mentor_assessments_evaluation_mode"),
        "mentor_assessments",
        ["evaluation_mode"],
        unique=False,
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_mentor_assessments_mentor_id"),
        "mentor_assessments",
        ["mentor_id"],
        unique=False,
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_mentor_assessments_result_release_mode"),
        "mentor_assessments",
        ["result_release_mode"],
        unique=False,
        schema=schema_name,
    )

    op.create_table(
        "course_materials",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("material_type", sa.String(length=30), nullable=False),
        sa.Column("resource_url", sa.String(length=1000), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column(
            "metadata_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=_json_object_default,
        ),
        sa.Column("uploaded_by", sa.Integer(), nullable=True),
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
            ["uploaded_by"],
            [f"{schema_name}.users.id"],
            name=op.f("fk_course_materials_uploaded_by_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_course_materials")),
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_course_materials_course_id"),
        "course_materials",
        ["course_id"],
        unique=False,
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_course_materials_material_type"),
        "course_materials",
        ["material_type"],
        unique=False,
        schema=schema_name,
    )

    op.create_table(
        "guarantor_forms",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("form_url", sa.String(length=1000), nullable=False),
        sa.Column("cohort", sa.String(length=100), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column("uploaded_by", sa.Integer(), nullable=True),
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
            ["uploaded_by"],
            [f"{schema_name}.users.id"],
            name=op.f("fk_guarantor_forms_uploaded_by_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_guarantor_forms")),
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_guarantor_forms_cohort"),
        "guarantor_forms",
        ["cohort"],
        unique=False,
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_guarantor_forms_is_active"),
        "guarantor_forms",
        ["is_active"],
        unique=False,
        schema=schema_name,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_guarantor_forms_is_active"),
        table_name="guarantor_forms",
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_guarantor_forms_cohort"),
        table_name="guarantor_forms",
        schema=schema_name,
    )
    op.drop_table("guarantor_forms", schema=schema_name)

    op.drop_index(
        op.f("ix_course_materials_material_type"),
        table_name="course_materials",
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_course_materials_course_id"),
        table_name="course_materials",
        schema=schema_name,
    )
    op.drop_table("course_materials", schema=schema_name)

    op.drop_index(
        op.f("ix_mentor_assessments_result_release_mode"),
        table_name="mentor_assessments",
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_mentor_assessments_mentor_id"),
        table_name="mentor_assessments",
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_mentor_assessments_evaluation_mode"),
        table_name="mentor_assessments",
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_mentor_assessments_course_id"),
        table_name="mentor_assessments",
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_mentor_assessments_assessment_type"),
        table_name="mentor_assessments",
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_mentor_assessments_accepted"),
        table_name="mentor_assessments",
        schema=schema_name,
    )
    op.drop_table("mentor_assessments", schema=schema_name)

    op.drop_index(
        op.f("ix_mentor_course_map_mentor_id"),
        table_name="mentor_course_map",
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_mentor_course_map_course_id"),
        table_name="mentor_course_map",
        schema=schema_name,
    )
    op.drop_table("mentor_course_map", schema=schema_name)

    op.drop_index(op.f("ix_mentors_is_active"), table_name="mentors", schema=schema_name)
    op.drop_table("mentors", schema=schema_name)
