"""add participation mode to student profiles

Revision ID: 20260618_0009
Revises: 20260515_0008
Create Date: 2026-06-18 00:00:00.000000

"""

import sqlalchemy as sa

from alembic import op
from app.core.config import get_settings

revision = "20260618_0009"
down_revision = "20260515_0008"
branch_labels = None
depends_on = None

settings = get_settings()
schema_name = settings.POSTGRES_SCHEMA


def upgrade() -> None:
    op.add_column(
        "student_profiles",
        sa.Column("participation", sa.String(length=20), nullable=True),
        schema=schema_name,
    )
    op.create_index(
        "ix_student_profiles_participation",
        "student_profiles",
        ["participation"],
        schema=schema_name,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_student_profiles_participation",
        table_name="student_profiles",
        schema=schema_name,
    )
    op.drop_column("student_profiles", "participation", schema=schema_name)
