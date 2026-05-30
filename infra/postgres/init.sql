CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS locations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    country_code TEXT NOT NULL,
    region_code TEXT,
    geography_level TEXT NOT NULL,
    parent_location_id TEXT REFERENCES locations(id),
    statcan_geo_name TEXT,
    statcan_geo_code TEXT,
    latitude NUMERIC,
    longitude NUMERIC,
    geometry GEOMETRY,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS data_sources (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    provider TEXT NOT NULL,
    base_url TEXT,
    documentation_url TEXT,
    requires_api_key BOOLEAN DEFAULT FALSE,
    refresh_frequency TEXT,
    enabled BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS indicators (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    unit TEXT NOT NULL,
    frequency TEXT NOT NULL,
    source_id TEXT REFERENCES data_sources(id),
    external_table_id TEXT,
    external_series_id TEXT,
    calculation_type TEXT,
    higher_is_good BOOLEAN,
    display_precision INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS observations (
    id BIGSERIAL PRIMARY KEY,
    indicator_id TEXT REFERENCES indicators(id),
    location_id TEXT REFERENCES locations(id),
    period DATE NOT NULL,
    value NUMERIC,
    unit TEXT,
    source_id TEXT REFERENCES data_sources(id),
    source_table_id TEXT,
    source_series_id TEXT,
    source_released_at TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT NOW(),
    is_preliminary BOOLEAN DEFAULT FALSE,
    is_estimated BOOLEAN DEFAULT FALSE,
    UNIQUE (indicator_id, location_id, period, source_id)
);

CREATE TABLE IF NOT EXISTS observation_calculations (
    id BIGSERIAL PRIMARY KEY,
    observation_id BIGINT UNIQUE REFERENCES observations(id),
    yoy_change NUMERIC,
    mom_change NUMERIC,
    three_month_change NUMERIC,
    twelve_month_change NUMERIC,
    z_score NUMERIC,
    national_difference NUMERIC,
    calculated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS leaderboard_definitions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    indicator_id TEXT REFERENCES indicators(id),
    sort_direction TEXT NOT NULL,
    geography_level TEXT NOT NULL,
    unit TEXT,
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS leaderboard_snapshots (
    id BIGSERIAL PRIMARY KEY,
    leaderboard_id TEXT REFERENCES leaderboard_definitions(id),
    location_id TEXT REFERENCES locations(id),
    period DATE NOT NULL,
    rank INTEGER NOT NULL,
    previous_rank INTEGER,
    rank_change INTEGER,
    value NUMERIC,
    unit TEXT,
    yoy_change NUMERIC,
    mom_change NUMERIC,
    national_average NUMERIC,
    difference_from_average NUMERIC,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (leaderboard_id, location_id, period)
);

CREATE TABLE IF NOT EXISTS basket_items (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit TEXT NOT NULL,
    default_quantity NUMERIC NOT NULL,
    statcan_product_name TEXT,
    indicator_id TEXT REFERENCES indicators(id),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS basket_definitions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    household_size INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS basket_definition_items (
    basket_id TEXT REFERENCES basket_definitions(id),
    item_id TEXT REFERENCES basket_items(id),
    quantity NUMERIC NOT NULL,
    PRIMARY KEY (basket_id, item_id)
);

CREATE TABLE IF NOT EXISTS basket_observations (
    id BIGSERIAL PRIMARY KEY,
    basket_id TEXT REFERENCES basket_definitions(id),
    location_id TEXT REFERENCES locations(id),
    period DATE NOT NULL,
    total_cost NUMERIC,
    yoy_change NUMERIC,
    mom_change NUMERIC,
    source_coverage_score NUMERIC,
    calculated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (basket_id, location_id, period)
);

CREATE TABLE IF NOT EXISTS raw_source_payloads (
    id BIGSERIAL PRIMARY KEY,
    source_id TEXT REFERENCES data_sources(id),
    dataset_id TEXT NOT NULL,
    request_hash TEXT NOT NULL,
    period DATE,
    payload JSONB NOT NULL,
    fetched_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS source_refresh_runs (
    id BIGSERIAL PRIMARY KEY,
    source_id TEXT REFERENCES data_sources(id),
    job_name TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TIMESTAMP DEFAULT NOW(),
    finished_at TIMESTAMP,
    rows_fetched INTEGER DEFAULT 0,
    rows_inserted INTEGER DEFAULT 0,
    rows_updated INTEGER DEFAULT 0,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS source_freshness (
    source_id TEXT REFERENCES data_sources(id),
    dataset_id TEXT NOT NULL,
    latest_period DATE,
    latest_source_release TIMESTAMP,
    last_checked_at TIMESTAMP,
    status TEXT,
    notes TEXT,
    PRIMARY KEY (source_id, dataset_id)
);

CREATE TABLE IF NOT EXISTS score_weights (
    score_id TEXT,
    component_indicator_id TEXT REFERENCES indicators(id),
    weight NUMERIC NOT NULL,
    direction TEXT NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (score_id, component_indicator_id)
);

CREATE TABLE IF NOT EXISTS data_quality_flags (
    id BIGSERIAL PRIMARY KEY,
    observation_id BIGINT REFERENCES observations(id),
    flag_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    display_name TEXT,
    avatar_url TEXT,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

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

CREATE TABLE IF NOT EXISTS saved_regions (
    user_id UUID REFERENCES users(id),
    location_id TEXT REFERENCES locations(id),
    label TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, location_id)
);

CREATE TABLE IF NOT EXISTS saved_baskets (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    name TEXT NOT NULL,
    basket_json JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
