"""add announcement soft delete

Revision ID: 20260724_0012
Revises: 20260723_0011
Create Date: 2026-07-24 15:42:00.000000

"""

import sqlalchemy as sa
from alembic import op
from app.core.config import get_settings

revision = "20260724_0012"
down_revision = "20260723_0011"
branch_labels = None
depends_on = None

settings = get_settings()
schema_name = settings.POSTGRES_SCHEMA


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [c["name"] for c in inspector.get_columns("student_updates", schema=schema_name)]

    if "is_deleted" not in columns:
        op.add_column(
            "student_updates",
            sa.Column(
                "is_deleted",
                sa.Boolean(),
                nullable=False,
                server_default=sa.text("false"),
            ),
            schema=schema_name,
        )
        op.create_index(
            op.f("ix_student_updates_is_deleted"),
            "student_updates",
            ["is_deleted"],
            unique=False,
            schema=schema_name,
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [c["name"] for c in inspector.get_columns("student_updates", schema=schema_name)]

    if "is_deleted" in columns:
        op.drop_index(
            op.f("ix_student_updates_is_deleted"),
            table_name="student_updates",
            schema=schema_name,
        )
        op.drop_column("student_updates", "is_deleted", schema=schema_name)
