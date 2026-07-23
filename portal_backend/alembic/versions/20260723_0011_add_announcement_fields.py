"""add fields to student_updates

Revision ID: 20260723_0011
Revises: 20260721_0010
Create Date: 2026-07-23 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op
from app.core.config import get_settings

revision = "20260723_0011"
down_revision = "20260721_0010"
branch_labels = None
depends_on = None

settings = get_settings()
schema_name = settings.POSTGRES_SCHEMA


def upgrade() -> None:
    op.add_column(
        "student_updates",
        sa.Column("programme", sa.String(length=255), nullable=True),
        schema=schema_name,
    )
    op.add_column(
        "student_updates",
        sa.Column("track", sa.String(length=255), nullable=True),
        schema=schema_name,
    )
    op.add_column(
        "student_updates",
        sa.Column("target_role", sa.String(length=50), nullable=True),
        schema=schema_name,
    )


def downgrade() -> None:
    op.drop_column("student_updates", "target_role", schema=schema_name)
    op.drop_column("student_updates", "track", schema=schema_name)
    op.drop_column("student_updates", "programme", schema=schema_name)
