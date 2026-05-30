"""Phase 4 user accounts and watchlist alignment.

Revision ID: 20260528_0002
Revises: 20260528_0001
Create Date: 2026-05-28 13:05:00
"""

from alembic import op

revision = "20260528_0002"
down_revision = "20260528_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            display_name TEXT,
            avatar_url TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS user_preferences (
            user_id UUID REFERENCES users(id),
            default_location_id TEXT,
            default_metric TEXT,
            default_period TEXT,
            default_basket_id TEXT,
            household_size INTEGER DEFAULT 1,
            theme TEXT DEFAULT 'system',
            data_density TEXT DEFAULT 'simple',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            PRIMARY KEY (user_id)
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS saved_regions (
            user_id UUID REFERENCES users(id),
            location_id TEXT REFERENCES locations(id),
            label TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            PRIMARY KEY (user_id, location_id)
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS saved_baskets (
            id UUID PRIMARY KEY,
            user_id UUID REFERENCES users(id),
            name TEXT NOT NULL,
            basket_json JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS saved_baskets;")
    op.execute("DROP TABLE IF EXISTS saved_regions;")
    op.execute("DROP TABLE IF EXISTS user_preferences;")
    op.execute("DROP TABLE IF EXISTS users;")

