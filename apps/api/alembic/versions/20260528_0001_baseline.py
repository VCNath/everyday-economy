"""Baseline schema for Everyday Economy.

Revision ID: 20260528_0001
Revises:
Create Date: 2026-05-28 00:00:00
"""

from alembic import op

revision = "20260528_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Baseline marker migration.
    # Existing local bootstrap currently uses infra/postgres/init.sql.
    # New schema changes should be introduced with Alembic revisions after this point.
    pass


def downgrade() -> None:
    pass
