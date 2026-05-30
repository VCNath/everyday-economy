"""Phase 6 admin operations console schema.

Revision ID: 20260528_0004
Revises: 20260528_0003
Create Date: 2026-05-28 16:00:00
"""

from alembic import op

revision = "20260528_0004"
down_revision = "20260528_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS job_runs (
            id UUID PRIMARY KEY,
            job_type TEXT NOT NULL,
            job_name TEXT NOT NULL,
            status TEXT NOT NULL,
            triggered_by_user_id UUID REFERENCES users(id),
            trigger_source TEXT NOT NULL,
            started_at TIMESTAMP NOT NULL DEFAULT NOW(),
            finished_at TIMESTAMP,
            rows_fetched INTEGER DEFAULT 0,
            rows_inserted INTEGER DEFAULT 0,
            rows_updated INTEGER DEFAULT 0,
            rows_failed INTEGER DEFAULT 0,
            error_message TEXT,
            metadata JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_job_runs_job_type ON job_runs(job_type);
        CREATE INDEX IF NOT EXISTS idx_job_runs_status ON job_runs(status);
        CREATE INDEX IF NOT EXISTS idx_job_runs_started_at ON job_runs(started_at);
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS admin_audit_logs (
            id UUID PRIMARY KEY,
            user_id UUID REFERENCES users(id),
            action TEXT NOT NULL,
            entity_type TEXT,
            entity_id TEXT,
            details JSONB,
            ip_address TEXT,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_admin_audit_logs_user_id ON admin_audit_logs(user_id);
        CREATE INDEX IF NOT EXISTS idx_admin_audit_logs_action ON admin_audit_logs(action);
        CREATE INDEX IF NOT EXISTS idx_admin_audit_logs_created_at ON admin_audit_logs(created_at);
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS feature_flags (
            key TEXT PRIMARY KEY,
            enabled BOOLEAN DEFAULT FALSE,
            description TEXT,
            updated_by_user_id UUID REFERENCES users(id),
            updated_at TIMESTAMP DEFAULT NOW(),
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_feature_flags_enabled ON feature_flags(enabled);
        """
    )
    op.execute("ALTER TABLE data_quality_flags ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMP;")
    op.execute("ALTER TABLE data_quality_flags ADD COLUMN IF NOT EXISTS reviewed_by_user_id UUID REFERENCES users(id);")
    op.execute("ALTER TABLE data_quality_flags ADD COLUMN IF NOT EXISTS review_note TEXT;")


def downgrade() -> None:
    op.execute("ALTER TABLE data_quality_flags DROP COLUMN IF EXISTS review_note;")
    op.execute("ALTER TABLE data_quality_flags DROP COLUMN IF EXISTS reviewed_by_user_id;")
    op.execute("ALTER TABLE data_quality_flags DROP COLUMN IF EXISTS reviewed_at;")
    op.execute("DROP TABLE IF EXISTS feature_flags;")
    op.execute("DROP TABLE IF EXISTS admin_audit_logs;")
    op.execute("DROP TABLE IF EXISTS job_runs;")

