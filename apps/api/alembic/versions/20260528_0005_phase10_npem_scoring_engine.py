"""phase10_npem_scoring_engine

Revision ID: 20260528_0005
Revises: 20260528_0004
Create Date: 2026-05-28
"""

from alembic import op


revision = "20260528_0005"
down_revision = "20260528_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS npem_group_metadata (
            group_code TEXT PRIMARY KEY,
            group_label TEXT NOT NULL,
            group_layer TEXT NOT NULL,
            mutually_exclusive BOOLEAN NOT NULL,
            baseline_year SMALLINT,
            hh_size_default NUMERIC(4,2),
            adults_default NUMERIC(4,2),
            children_default NUMERIC(4,2),
            selection_priority SMALLINT,
            rule_json JSON,
            governance_note TEXT,
            enabled BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS npem_variables (
            variable_code TEXT PRIMARY KEY,
            label TEXT NOT NULL,
            definition TEXT NOT NULL,
            unit_code TEXT NOT NULL,
            preferred_source TEXT,
            fallback_source TEXT,
            expected_year SMALLINT,
            metric_family TEXT,
            requires_nowcast BOOLEAN DEFAULT FALSE,
            proxy_allowed BOOLEAN DEFAULT TRUE,
            notes TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS npem_raw_data (
            raw_id VARCHAR(36) PRIMARY KEY,
            source_system TEXT NOT NULL,
            source_series_id TEXT,
            geography_code TEXT NOT NULL,
            geography_name TEXT,
            reference_year SMALLINT NOT NULL,
            reference_period TEXT,
            variable_code TEXT REFERENCES npem_variables(variable_code),
            group_code TEXT REFERENCES npem_group_metadata(group_code),
            value_num NUMERIC(18,4),
            unit_code TEXT,
            release_date DATE,
            access_date DATE,
            source_url_hash TEXT,
            quality_flag TEXT,
            provenance_id VARCHAR(36),
            created_at TIMESTAMP,
            UNIQUE(source_system, source_series_id, geography_code, reference_year, group_code, variable_code)
        );
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_npem_raw_geo_year_group_variable ON npem_raw_data(geography_code, reference_year, group_code, variable_code);")
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS npem_normalized_scores (
            norm_id VARCHAR(36) PRIMARY KEY,
            geography_code TEXT NOT NULL,
            reference_year SMALLINT NOT NULL,
            group_code TEXT REFERENCES npem_group_metadata(group_code),
            component_code TEXT NOT NULL,
            raw_value NUMERIC(18,6),
            winsor_p5 NUMERIC(18,6),
            winsor_p95 NUMERIC(18,6),
            normalized_score NUMERIC(5,2),
            inversion_applied BOOLEAN,
            imputation_level SMALLINT,
            confidence_component NUMERIC(5,2),
            model_version TEXT NOT NULL,
            created_at TIMESTAMP,
            UNIQUE(geography_code, reference_year, group_code, component_code, model_version)
        );
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_npem_norm_geo_year_group ON npem_normalized_scores(geography_code, reference_year, group_code);")
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS npem_scenarios (
            scenario_code TEXT PRIMARY KEY,
            label TEXT NOT NULL,
            description TEXT,
            enabled BOOLEAN DEFAULT TRUE,
            model_version TEXT NOT NULL,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS npem_scenario_weights (
            scenario_code TEXT REFERENCES npem_scenarios(scenario_code),
            component_code TEXT NOT NULL,
            weight NUMERIC(8,6) NOT NULL,
            PRIMARY KEY (scenario_code, component_code)
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS npem_scores (
            score_id VARCHAR(36) PRIMARY KEY,
            geography_code TEXT NOT NULL,
            reference_year SMALLINT NOT NULL,
            group_code TEXT REFERENCES npem_group_metadata(group_code),
            scenario_code TEXT REFERENCES npem_scenarios(scenario_code),
            base_composite NUMERIC(5,2),
            paf_value NUMERIC(6,4),
            final_score NUMERIC(5,2),
            score_rank_within_geo SMALLINT,
            confidence_score NUMERIC(5,2),
            confidence_grade TEXT,
            model_version TEXT NOT NULL,
            created_at TIMESTAMP,
            UNIQUE(geography_code, reference_year, group_code, scenario_code, model_version)
        );
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_npem_scores_geo_year_scenario ON npem_scores(geography_code, reference_year, scenario_code);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_npem_scores_group ON npem_scores(group_code);")
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS npem_provenance (
            provenance_id VARCHAR(36) PRIMARY KEY,
            score_id VARCHAR(36) REFERENCES npem_scores(score_id),
            source_system TEXT NOT NULL,
            source_series_id TEXT,
            citation_text TEXT,
            release_date DATE,
            access_date DATE,
            transform_step TEXT,
            licence_note TEXT,
            source_url TEXT,
            source_hash TEXT,
            created_at TIMESTAMP
        );
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_npem_provenance_score ON npem_provenance(score_id);")
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS npem_quality_components (
            quality_id VARCHAR(36) PRIMARY KEY,
            geography_code TEXT NOT NULL,
            reference_year SMALLINT NOT NULL,
            group_code TEXT REFERENCES npem_group_metadata(group_code),
            coverage_ratio NUMERIC(5,4),
            recency_score NUMERIC(5,4),
            directness_score NUMERIC(5,4),
            reliability_score NUMERIC(5,4),
            suppression_penalty NUMERIC(5,4),
            proxy_share NUMERIC(5,4),
            confidence_score NUMERIC(5,2),
            confidence_grade TEXT,
            created_at TIMESTAMP,
            UNIQUE(geography_code, reference_year, group_code)
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS npem_provincial_adjustments (
            adjustment_id VARCHAR(36) PRIMARY KEY,
            geography_code TEXT NOT NULL,
            reference_year SMALLINT NOT NULL,
            mbm_total NUMERIC(18,4),
            modeled_essentials_prov NUMERIC(18,4),
            undercoverage_ratio NUMERIC(18,6),
            paf_value NUMERIC(6,4),
            created_at TIMESTAMP
        );
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS npem_provincial_adjustments;")
    op.execute("DROP TABLE IF EXISTS npem_quality_components;")
    op.execute("DROP TABLE IF EXISTS npem_provenance;")
    op.execute("DROP TABLE IF EXISTS npem_scores;")
    op.execute("DROP TABLE IF EXISTS npem_scenario_weights;")
    op.execute("DROP TABLE IF EXISTS npem_scenarios;")
    op.execute("DROP TABLE IF EXISTS npem_normalized_scores;")
    op.execute("DROP TABLE IF EXISTS npem_raw_data;")
    op.execute("DROP TABLE IF EXISTS npem_variables;")
    op.execute("DROP TABLE IF EXISTS npem_group_metadata;")
