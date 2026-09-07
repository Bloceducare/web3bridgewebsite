"""add mentor course programme track

Revision ID: 20260728_0013
Revises: 20260724_0012
Create Date: 2026-07-28 15:50:00.000000

"""

import sqlalchemy as sa
from alembic import op
from app.core.config import get_settings

revision = "20260728_0013"
down_revision = "20260724_0012"
branch_labels = None
depends_on = None

settings = get_settings()
schema_name = settings.POSTGRES_SCHEMA


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [c["name"] for c in inspector.get_columns("mentor_course_map", schema=schema_name)]

    if "programme" not in columns:
        op.add_column(
            "mentor_course_map",
            sa.Column("programme", sa.String(length=255), nullable=True),
            schema=schema_name,
        )
    if "track" not in columns:
        op.add_column(
            "mentor_course_map",
            sa.Column("track", sa.String(length=255), nullable=True),
            schema=schema_name,
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [c["name"] for c in inspector.get_columns("mentor_course_map", schema=schema_name)]

    if "track" in columns:
        op.drop_column("mentor_course_map", "track", schema=schema_name)
    if "programme" in columns:
        op.drop_column("mentor_course_map", "programme", schema=schema_name)
