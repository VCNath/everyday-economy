"""Phase 5 alerts notifications and reports.

Revision ID: 20260528_0003
Revises: 20260528_0002
Create Date: 2026-05-28 14:30:00
"""

from alembic import op

revision = "20260528_0003"
down_revision = "20260528_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS alert_rules (
            id UUID PRIMARY KEY,
            user_id UUID REFERENCES users(id),
            location_id TEXT REFERENCES locations(id),
            indicator_id TEXT REFERENCES indicators(id),
            alert_type TEXT NOT NULL,
            comparison_operator TEXT NOT NULL,
            threshold_value NUMERIC,
            change_value NUMERIC,
            rank_value INTEGER,
            frequency TEXT DEFAULT 'on_change',
            enabled BOOLEAN DEFAULT TRUE,
            channel_in_app BOOLEAN DEFAULT TRUE,
            channel_email BOOLEAN DEFAULT FALSE,
            last_triggered_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_alert_rules_user_id ON alert_rules(user_id);
        CREATE INDEX IF NOT EXISTS idx_alert_rules_location_id ON alert_rules(location_id);
        CREATE INDEX IF NOT EXISTS idx_alert_rules_enabled ON alert_rules(enabled);
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id UUID PRIMARY KEY,
            user_id UUID REFERENCES users(id),
            alert_rule_id UUID REFERENCES alert_rules(id),
            location_id TEXT REFERENCES locations(id),
            indicator_id TEXT REFERENCES indicators(id),
            type TEXT NOT NULL,
            severity TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            value NUMERIC,
            threshold_value NUMERIC,
            period DATE,
            source_id TEXT,
            freshness_status TEXT,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
        CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
        CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at);
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS monthly_reports (
            id UUID PRIMARY KEY,
            user_id UUID REFERENCES users(id),
            location_id TEXT REFERENCES locations(id),
            report_period DATE NOT NULL,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            report_json JSONB NOT NULL,
            generated_at TIMESTAMP DEFAULT NOW(),
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_monthly_reports_user_id ON monthly_reports(user_id);
        CREATE INDEX IF NOT EXISTS idx_monthly_reports_location_id ON monthly_reports(location_id);
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS notification_preferences (
            user_id UUID PRIMARY KEY REFERENCES users(id),
            in_app_enabled BOOLEAN DEFAULT TRUE,
            email_enabled BOOLEAN DEFAULT FALSE,
            monthly_report_enabled BOOLEAN DEFAULT TRUE,
            data_release_alerts_enabled BOOLEAN DEFAULT TRUE,
            source_health_alerts_enabled BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS notification_preferences;")
    op.execute("DROP TABLE IF EXISTS monthly_reports;")
    op.execute("DROP TABLE IF EXISTS notifications;")
    op.execute("DROP TABLE IF EXISTS alert_rules;")

