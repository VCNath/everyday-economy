export type MetricKey =
  | "cpi_all_items_index"
  | "cpi_all_items_yoy"
  | "cpi_food_index"
  | "cpi_food_yoy"
  | "cpi_shelter_index"
  | "cpi_shelter_yoy"
  | "gas_regular_cents_litre"
  | "unemployment_rate"
  | "employment_rate"
  | "participation_rate"
  | "basic_basket_monthly_cost"
  | "basic_basket_yoy"
  | "affordability_score"
  | "boc_policy_rate"
  | "cad_usd_exchange_rate";

export interface MapFeature {
  location_id: string;
  name: string;
  value: number;
  rank: number;
  geometry_ref: string;
  yoy_change?: number;
  updated: string;
}

export interface RegionSummary {
  location_id: string;
  name: string;
  period: string;
  metrics: Record<string, number>;
  insight: string;
  sources: string[];
}

export interface LeaderboardRow {
  rank: number;
  location_id: string;
  name: string;
  value: number;
  unit: string;
  yoy_change?: number;
  mom_change?: number;
  previous_rank?: number;
  rank_change?: number;
  source: string;
  updated: string;
}

export interface SourceStatus {
  source: string;
  dataset: string;
  latest_period: string;
  last_checked: string;
  status: string;
  notes?: string | null;
}

export interface Location {
  id: string;
  name: string;
  country_code: string;
  region_code?: string | null;
  geography_level: string;
  parent_location_id?: string | null;
  latitude?: number | null;
  longitude?: number | null;
}

export interface Indicator {
  id: string;
  name: string;
  category: string;
  description: string;
  unit: string;
  frequency: string;
  source_id: string;
  higher_is_good: boolean;
  display_precision: number;
  human_translation: string;
}

export interface BasketLineItem {
  item_id: string;
  name: string;
  quantity: number;
  unit: string;
  unit_price: number;
  monthly_cost: number;
}

export interface BasketCalculation {
  location_id: string;
  basket_type: string;
  period: string;
  total_cost: number;
  yoy_change: number;
  coverage_score: number;
  items: BasketLineItem[];
}

export interface SourceRun {
  source_id: string;
  job_name: string;
  status: string;
  started_at?: string | null;
  finished_at?: string | null;
  rows_fetched: number;
  rows_inserted: number;
  rows_updated: number;
  error_message?: string | null;
}

export interface MetricTrustMetadata {
  source_id?: string | null;
  source_name?: string | null;
  source_table_id?: string | null;
  source_series_id?: string | null;
  latest_period?: string | null;
  last_checked?: string | null;
  freshness_status: string;
  is_estimated: boolean;
  is_cached: boolean;
  coverage_score?: number | null;
  notes?: string | null;
}

export interface SeriesPoint {
  period: string;
  value: number | null;
  yoy_change?: number | null;
  mom_change?: number | null;
  trust: MetricTrustMetadata;
}

export interface IndicatorSeries {
  indicator_id: string;
  indicator_name: string;
  unit: string;
  points: SeriesPoint[];
}

export interface RegionSeriesResponse {
  location_id: string;
  location_name: string;
  window: string;
  start_period?: string | null;
  end_period?: string | null;
  series: IndicatorSeries[];
  freshness: MetricTrustMetadata[];
  warnings: Array<{ code: string; message: string; severity: string }>;
}

export interface CompareMetricRow {
  location_id: string;
  location_name: string;
  indicator_id: string;
  indicator_name: string;
  value: number | null;
  unit: string;
  period?: string | null;
  yoy_change?: number | null;
  mom_change?: number | null;
  trust: MetricTrustMetadata;
}

export interface CompareResponse {
  locations: Array<{ location_id: string; location_name: string }>;
  indicators: Array<{ indicator_id: string; indicator_name: string; unit: string }>;
  period: string;
  window: string;
  rows: CompareMetricRow[];
  series: IndicatorSeries[];
  freshness: MetricTrustMetadata[];
  warnings: Array<{ code: string; message: string; severity: string }>;
}

export interface User {
  id: string;
  email: string;
  display_name?: string | null;
  avatar_url?: string | null;
  role: string;
  created_at?: string | null;
}

export interface UserPreferences {
  default_location_id?: string | null;
  default_metric?: string | null;
  default_period?: string | null;
  default_basket_id?: string | null;
  household_size: number;
  theme: string;
  data_density: string;
}

export interface UpdatePreferencesPayload {
  default_location_id?: string | null;
  default_metric?: string | null;
  default_period?: string | null;
  default_basket_id?: string | null;
  household_size?: number;
  theme?: string;
  data_density?: string;
}

export interface SavedRegion {
  location_id: string;
  name: string;
  label?: string | null;
  saved_at: string;
}

export interface WatchlistRegion {
  location_id: string;
  name: string;
  label?: string | null;
  saved_at: string;
  summary: Record<string, number>;
  freshness: MetricTrustMetadata;
}

export interface SaveRegionPayload {
  location_id: string;
  label?: string | null;
}

export interface AuthState {
  loading: boolean;
  isAuthenticated: boolean;
  isAdmin: boolean;
  token: string | null;
  user: User | null;
}

export type AlertSeverity = "info" | "warning" | "error" | "positive" | "negative";
export type AlertType = "threshold" | "change" | "rank" | "data_release" | "source_health";
export type NotificationType = "alert" | "report" | "source_health" | "data_release";

export interface AlertRule {
  id: string;
  user_id: string;
  location_id: string;
  location_name: string;
  indicator_id: string;
  indicator_name: string;
  alert_type: string;
  comparison_operator: string;
  threshold_value?: number | null;
  change_value?: number | null;
  rank_value?: number | null;
  frequency: string;
  enabled: boolean;
  channels: { in_app: boolean; email: boolean };
  last_triggered_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface AlertRuleCreatePayload {
  location_id: string;
  indicator_id: string;
  alert_type: string;
  comparison_operator: string;
  threshold_value?: number;
  change_value?: number;
  rank_value?: number;
  frequency?: string;
  enabled?: boolean;
  channel_in_app?: boolean;
  channel_email?: boolean;
}

export type AlertRuleUpdatePayload = Partial<AlertRuleCreatePayload>;

export interface Notification {
  id: string;
  type: string;
  severity: string;
  title: string;
  message: string;
  location_id?: string | null;
  indicator_id?: string | null;
  value?: number | null;
  threshold_value?: number | null;
  period?: string | null;
  source_id?: string | null;
  freshness_status?: string | null;
  is_read: boolean;
  created_at: string;
}

export interface NotificationPreferences {
  in_app_enabled: boolean;
  email_enabled: boolean;
  monthly_report_enabled: boolean;
  data_release_alerts_enabled: boolean;
  source_health_alerts_enabled: boolean;
}

export interface MonthlyReport {
  id: string;
  location_id: string;
  report_period: string;
  title: string;
  summary: string;
  report_json: Record<string, unknown>;
  generated_at: string;
}

export interface MonthlyReportSummary {
  items: MonthlyReport[];
}

export type AdminJobRunStatus = "pending" | "running" | "succeeded" | "failed" | "skipped" | "queued";

export interface AdminDashboardSummary {
  healthy_sources: number;
  stale_sources: number;
  failed_jobs: number;
  open_data_quality_flags: number;
  alert_rules_active: number;
  notifications_generated_today: number;
  reports_generated_this_month: number;
}

export interface AdminSourceHealth {
  source: string;
  dataset: string;
  status: string;
  latest_period?: string | null;
  last_checked?: string | null;
  last_successful_run?: string | null;
  error_message?: string | null;
  rows_fetched: number;
  rows_inserted: number;
  rows_updated: number;
}

export interface AdminJobRun {
  id: string;
  job_type: string;
  job_name: string;
  status: AdminJobRunStatus | string;
  trigger_source: string;
  triggered_by_user_id?: string | null;
  started_at: string;
  finished_at?: string | null;
  duration_seconds?: number | null;
  rows_fetched: number;
  rows_inserted: number;
  rows_updated: number;
  rows_failed: number;
  error_message?: string | null;
  metadata?: Record<string, unknown> | null;
}

export interface AdminJobTriggerPayload {
  job_name: string;
}

export interface AdminJobTriggerResponse {
  job_run: AdminJobRun;
}

export interface DataQualityFlag {
  id: number;
  flag_type: string;
  severity: string;
  message?: string | null;
  created_at: string;
  reviewed_at?: string | null;
  reviewed_by_user_id?: string | null;
  review_note?: string | null;
}

export interface AdminAuditLog {
  id: string;
  user_id?: string | null;
  action: string;
  entity_type?: string | null;
  entity_id?: string | null;
  details?: Record<string, unknown> | null;
  ip_address?: string | null;
  user_agent?: string | null;
  created_at: string;
}

export interface FeatureFlag {
  key: string;
  enabled: boolean;
  description?: string | null;
  updated_by_user_id?: string | null;
  updated_at: string;
  created_at: string;
}

export interface FeatureFlagUpdatePayload {
  enabled: boolean;
  description?: string | null;
}

export interface AdminUserRow {
  id: string;
  email: string;
  display_name?: string | null;
  role: string;
  created_at?: string | null;
  saved_region_count: number;
  alert_rule_count: number;
  notification_count: number;
}

export interface NpemGroup {
  group_code: string;
  group_label: string;
  group_layer: "core" | "overlay" | string;
  mutually_exclusive: boolean;
  baseline_year?: number | null;
  governance_note?: string | null;
  enabled: boolean;
}

export interface NpemVariable {
  variable_code: string;
  label: string;
  definition: string;
  unit_code: string;
  preferred_source?: string | null;
  fallback_source?: string | null;
  expected_year?: number | null;
  metric_family?: string | null;
  requires_nowcast: boolean;
  proxy_allowed: boolean;
  notes?: string | null;
}

export interface NpemScenario {
  scenario_code: string;
  label: string;
  description?: string | null;
  enabled: boolean;
  model_version: string;
  weights: Record<string, number>;
}

export interface NpemConfidence {
  confidence_score: number;
  confidence_grade: string;
  confidence_label: string;
  coverage_ratio?: number | null;
  recency_score?: number | null;
  directness_score?: number | null;
  reliability_score?: number | null;
  proxy_share?: number | null;
  suppression_penalty?: number | null;
}

export interface NpemComponentScore {
  component_code: string;
  component_label: string;
  raw_value?: number | null;
  normalized_score?: number | null;
  direction: string;
  imputation_level: number;
  confidence_component?: number | null;
}

export interface NpemScore {
  score_id: string;
  geography_code: string;
  reference_year: number;
  group_code: string;
  group_label: string;
  group_layer: string;
  scenario_code: string;
  base_composite?: number | null;
  paf_value?: number | null;
  final_score?: number | null;
  rank?: number | null;
  model_version: string;
  confidence: NpemConfidence;
  components: NpemComponentScore[];
  proxy_warnings: string[];
  overlap_warnings: string[];
  provenance_summary: string[];
}

export interface NpemScoreResponse {
  province: string;
  geography_code: string;
  reference_year: number;
  scenario: NpemScenario;
  latest_available_year: number;
  model_version: string;
  scores: NpemScore[];
  warnings: string[];
}

export interface NpemScenarioDelta {
  group_code: string;
  group_label: string;
  scenario_a_score?: number | null;
  scenario_b_score?: number | null;
  delta?: number | null;
  rank_change?: number | null;
}

export interface NpemProvenance {
  provenance_id: string;
  source_system: string;
  source_series_id?: string | null;
  citation_text?: string | null;
  release_date?: string | null;
  access_date?: string | null;
  transform_step?: string | null;
  licence_note?: string | null;
  source_url?: string | null;
  source_hash?: string | null;
}

export interface NpemCitation {
  citation_text?: string | null;
  source_url?: string | null;
  source_system: string;
  licence_note?: string | null;
}

export type FeedbackType = "bug" | "data_issue" | "confusing" | "feature_request" | "design_feedback" | "general";
export type FeedbackStatus = "new" | "reviewed" | "planned" | "fixed" | "closed";

export interface FeedbackPayload {
  page_path?: string | null;
  feedback_type: FeedbackType;
  rating?: number | null;
  message: string;
  email?: string | null;
  metadata?: Record<string, unknown> | null;
}

export interface BetaFeedback {
  id: string;
  user_id?: string | null;
  page_path?: string | null;
  feedback_type: string;
  rating?: number | null;
  message: string;
  email?: string | null;
  metadata?: Record<string, unknown> | null;
  status: FeedbackStatus | string;
  created_at: string;
  updated_at: string;
}
