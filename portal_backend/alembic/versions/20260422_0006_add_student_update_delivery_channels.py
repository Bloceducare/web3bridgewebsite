"""add student update delivery channels

Revision ID: 20260422_0006
Revises: 20260417_0005
Create Date: 2026-04-22 00:00:00.000000

"""

import sqlalchemy as sa

from alembic import op
from app.core.config import get_settings

revision = "20260422_0006"
down_revision = "20260417_0005"
branch_labels = None
depends_on = None

settings = get_settings()
schema_name = settings.POSTGRES_SCHEMA


def upgrade() -> None:
    op.add_column(
        "student_updates",
        sa.Column(
            "send_in_app",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        schema=schema_name,
    )
    op.add_column(
        "student_updates",
        sa.Column(
            "send_email",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_student_updates_send_in_app"),
        "student_updates",
        ["send_in_app"],
        unique=False,
        schema=schema_name,
    )
    op.create_index(
        op.f("ix_student_updates_send_email"),
        "student_updates",
        ["send_email"],
        unique=False,
        schema=schema_name,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_student_updates_send_email"),
        table_name="student_updates",
        schema=schema_name,
    )
    op.drop_index(
        op.f("ix_student_updates_send_in_app"),
        table_name="student_updates",
        schema=schema_name,
    )
    op.drop_column("student_updates", "send_email", schema=schema_name)
    op.drop_column("student_updates", "send_in_app", schema=schema_name)
