"""add programme and track to course_materials

Revision ID: 20260911_0014
Revises: 20260728_0013
Create Date: 2026-09-11 19:00:00.000000

"""

import sqlalchemy as sa
from alembic import op
from app.core.config import get_settings

revision = "20260911_0014"
down_revision = "20260728_0013"
branch_labels = None
depends_on = None

settings = get_settings()
schema_name = settings.POSTGRES_SCHEMA


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [c["name"] for c in inspector.get_columns("course_materials", schema=schema_name)]

    if "programme" not in columns:
        op.add_column(
            "course_materials",
            sa.Column("programme", sa.String(length=255), nullable=True),
            schema=schema_name,
        )
    if "track" not in columns:
        op.add_column(
            "course_materials",
            sa.Column("track", sa.String(length=255), nullable=True),
            schema=schema_name,
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [c["name"] for c in inspector.get_columns("course_materials", schema=schema_name)]

    if "track" in columns:
        op.drop_column("course_materials", "track", schema=schema_name)
    if "programme" in columns:
        op.drop_column("course_materials", "programme", schema=schema_name)
