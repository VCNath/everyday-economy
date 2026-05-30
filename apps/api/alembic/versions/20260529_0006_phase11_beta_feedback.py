"""phase11_beta_feedback

Revision ID: 20260529_0006
Revises: 20260528_0005
Create Date: 2026-05-29
"""

from alembic import op


revision = "20260529_0006"
down_revision = "20260528_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS beta_feedback (
            id VARCHAR(36) PRIMARY KEY,
            user_id VARCHAR(36) NULL REFERENCES users(id),
            page_path TEXT,
            feedback_type TEXT NOT NULL,
            rating INTEGER,
            message TEXT NOT NULL,
            email TEXT,
            metadata JSON,
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_beta_feedback_status ON beta_feedback(status);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_beta_feedback_type ON beta_feedback(feedback_type);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_beta_feedback_created_at ON beta_feedback(created_at);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS beta_feedback;")
