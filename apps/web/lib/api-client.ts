import { groceryLeaderboard, mapFeatures, saskatchewanSummary, sourceStatus } from "./mock-data";
import type {
  BasketCalculation,
  CompareResponse,
  Indicator,
  RegionSeriesResponse,
  LeaderboardRow,
  Location,
  MapFeature,
  RegionSummary,
  SourceRun,
  SourceStatus,
  SavedRegion,
  SaveRegionPayload,
  UpdatePreferencesPayload,
  User,
  UserPreferences,
  WatchlistRegion,
  AlertRule,
  AlertRuleCreatePayload,
  AlertRuleUpdatePayload,
  Notification,
  NotificationPreferences,
  MonthlyReport
  ,AdminDashboardSummary,
  AdminSourceHealth,
  AdminJobRun,
  AdminJobTriggerPayload,
  AdminJobTriggerResponse,
  DataQualityFlag,
  AdminAuditLog,
  FeatureFlag,
  FeatureFlagUpdatePayload
  ,AdminUserRow
  ,NpemCitation,
  NpemGroup,
  NpemProvenance,
  NpemScenario,
  NpemScenarioDelta,
  NpemScoreResponse,
  NpemVariable,
  FeedbackPayload,
  BetaFeedback,
  FeedbackStatus
} from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

const npemFallbackScenarios: NpemScenario[] = [
  { scenario_code: "baseline", label: "Baseline", description: "Balanced N.P.E.M. weights.", enabled: true, model_version: "npem_v1_demo_2026", weights: { GCI: 0.1, CPII: 0.1, BBI: 0.15, HRI: 0.2, HCI: 0.1, ECI: 0.05, GAI: 0.08, DSI: 0.12, DLI: 0.1 } },
  { scenario_code: "housing_stress", label: "Housing stress", description: "Places more weight on housing and essentials.", enabled: true, model_version: "npem_v1_demo_2026", weights: { GCI: 0.07, CPII: 0.1, BBI: 0.16, HRI: 0.3, HCI: 0.08, ECI: 0.04, GAI: 0.1, DSI: 0.08, DLI: 0.07 } },
  { scenario_code: "income_strength", label: "Income strength", description: "Emphasizes income and discretionary capacity.", enabled: true, model_version: "npem_v1_demo_2026", weights: { GCI: 0.18, CPII: 0.07, BBI: 0.1, HRI: 0.12, HCI: 0.08, ECI: 0.04, GAI: 0.05, DSI: 0.24, DLI: 0.12 } }
];

const npemFallbackGroups: NpemGroup[] = [
  { group_code: "YA_UC", group_label: "Young adults without children", group_layer: "core", mutually_exclusive: true, baseline_year: 2025, governance_note: "Core headline group.", enabled: true },
  { group_code: "CP_FAM", group_label: "Couple-parent families", group_layer: "core", mutually_exclusive: true, baseline_year: 2025, governance_note: "Core headline group.", enabled: true },
  { group_code: "LP_FAM", group_label: "Lone-parent families", group_layer: "core", mutually_exclusive: true, baseline_year: 2025, governance_note: "Core headline group.", enabled: true },
  { group_code: "RENTER", group_label: "Renters overlay", group_layer: "overlay", mutually_exclusive: false, baseline_year: 2025, governance_note: "Overlapping cohort.", enabled: true }
];

function npemFallbackScores(province = "AB", scenario = "baseline"): NpemScoreResponse {
  const scores = npemFallbackGroups.map((group, index) => ({
    score_id: `fallback-${province}-${group.group_code}-${scenario}`,
    geography_code: province.startsWith("CA-") ? province : `CA-${province}`,
    reference_year: 2025,
    group_code: group.group_code,
    group_label: group.group_label,
    group_layer: group.group_layer,
    scenario_code: scenario,
    base_composite: 72 - index * 6,
    paf_value: 1,
    final_score: 72 - index * 6,
    rank: index + 1,
    model_version: "npem_v1_demo_2026",
    confidence: { confidence_score: 68, confidence_grade: "C", confidence_label: "Moderate confidence", coverage_ratio: 0.76, recency_score: 0.78, directness_score: 0.62, reliability_score: 0.78, proxy_share: 0.38, suppression_penalty: 0.04 },
    components: ["GCI", "CPII", "BBI", "HRI", "HCI", "ECI", "GAI", "DSI", "DLI"].map((component, cIndex) => ({ component_code: component, component_label: component, raw_value: 50 + cIndex, normalized_score: 70 - index * 4 - cIndex, direction: component === "GCI" || component === "DSI" ? "benefit" : "burden", imputation_level: 2, confidence_component: 68 })),
    proxy_warnings: ["Demo fallback N.P.E.M. scores are estimated."],
    overlap_warnings: group.group_layer === "overlay" ? ["Overlapping cohort."] : [],
    provenance_summary: ["Everyday Economy fallback N.P.E.M. demo scaffold."]
  }));
  return {
    province,
    geography_code: province.startsWith("CA-") ? province : `CA-${province}`,
    reference_year: 2025,
    scenario: npemFallbackScenarios.find((row) => row.scenario_code === scenario) ?? npemFallbackScenarios[0],
    latest_available_year: 2025,
    model_version: "npem_v1_demo_2026",
    scores,
    warnings: ["Backend N.P.E.M. data unavailable. Showing local demo fallback."]
  };
}

async function fetchJson<T>(path: string, fallback: T): Promise<T> {
  if (process.env.NEXT_PHASE === "phase-production-build" && !process.env.ALLOW_BUILD_API_FETCH) {
    return fallback;
  }
  try {
    const response = await fetch(`${API_BASE_URL}${path}`, { next: { revalidate: 300 } });
    if (!response.ok) return fallback;
    return (await response.json()) as T;
  } catch {
    return fallback;
  }
}

async function fetchJsonAuthed<T>(path: string, token: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers ?? {});
  headers.set("authorization", `Bearer ${token}`);
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers,
    cache: "no-store"
  });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return (await response.json()) as T;
}

export async function getMapFeatures(indicator = "cpi_food_yoy"): Promise<MapFeature[]> {
  const response = await fetchJson<{ features: MapFeature[] }>(`/map?indicator=${indicator}`, {
    features: mapFeatures
  });
  return response.features;
}

export async function getMapData(indicator = "cpi_food_yoy") {
  return fetchJson<{ features: MapFeature[]; period: string; source: string }>(`/map?indicator=${indicator}`, {
    features: mapFeatures,
    period: "2026-04",
    source: "Statistics Canada"
  });
}

export async function getLocations(): Promise<Location[]> {
  return fetchJson<Location[]>("/locations", []);
}

export async function searchLocations(query: string): Promise<Location[]> {
  return fetchJson<Location[]>(`/locations/search?q=${encodeURIComponent(query)}`, []);
}

export async function getIndicators(): Promise<Indicator[]> {
  return fetchJson<Indicator[]>("/indicators", []);
}

export async function getRegionSummary(locationId = "CA-SK"): Promise<RegionSummary> {
  return fetchJson<RegionSummary>(`/regions/${locationId}/summary`, saskatchewanSummary);
}

export async function getLeaderboard(type = "grocery_basket"): Promise<LeaderboardRow[]> {
  const response = await fetchJson<{ rows: LeaderboardRow[] }>(`/leaderboards/${type}`, {
    rows: groceryLeaderboard
  });
  return response.rows;
}

export async function getLeaderboards(type = "grocery_basket") {
  return fetchJson<{ rows: LeaderboardRow[]; period: string; leaderboard_type: string }>(`/leaderboards/${type}`, {
    rows: groceryLeaderboard,
    period: "2026-04",
    leaderboard_type: type
  });
}

export async function getLeaderboardsByParams(params: {
  type?: string;
  geography_level?: string;
  period?: string;
  sort?: string;
  limit?: number;
}) {
  const query = new URLSearchParams({
    type: params.type ?? "grocery_basket",
    geography_level: params.geography_level ?? "province",
    period: params.period ?? "latest",
    sort: params.sort ?? "desc",
    limit: String(params.limit ?? 10)
  });
  return fetchJson<{ rows: LeaderboardRow[]; period: string; leaderboard_type: string }>(`/leaderboards?${query.toString()}`, {
    rows: groceryLeaderboard,
    period: "2026-04",
    leaderboard_type: params.type ?? "grocery_basket"
  });
}

export async function getBasketDefault(): Promise<BasketCalculation> {
  return fetchJson<BasketCalculation>("/basket/default", {
    location_id: "CA-SK",
    basket_type: "basic",
    period: "2026-04",
    total_cost: 428.35,
    yoy_change: 3.7,
    coverage_score: 0.82,
    items: []
  });
}

export async function calculateBasket(payload: {
  location_id: string;
  basket_type?: string;
  household_size?: number;
  items: { item_id: string; quantity: number }[];
}): Promise<BasketCalculation> {
  try {
    const response = await fetch(`${API_BASE_URL}/basket/calculate`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
      next: { revalidate: 0 }
    });
    if (!response.ok) return getBasketDefault();
    return (await response.json()) as BasketCalculation;
  } catch {
    return getBasketDefault();
  }
}

export async function getSourceStatus(): Promise<SourceStatus[]> {
  const response = await fetchJson<{ sources: SourceStatus[] }>("/source-status", { sources: sourceStatus });
  return response.sources;
}

export async function getSourceRuns(): Promise<SourceRun[]> {
  const response = await fetchJson<{ runs: SourceRun[] }>("/source-status/runs", { runs: [] });
  return response.runs;
}

export async function getApiHealth(): Promise<{
  health: { status: string };
  db: { status: string; message?: string };
  cache: { status: string; message?: string };
  sources: { sources: SourceStatus[] };
}> {
  const [health, db, cache, sources] = await Promise.all([
    fetchJson<{ status: string }>("/health", { status: "unknown" }),
    fetchJson<{ status: string; message?: string }>("/health/db", { status: "unknown" }),
    fetchJson<{ status: string; message?: string }>("/health/cache", { status: "unknown" }),
    fetchJson<{ sources: SourceStatus[] }>("/health/sources", { sources: sourceStatus })
  ]);
  return { health, db, cache, sources };
}

export async function getRegionTimeSeries(
  locationId: string,
  params: { indicators?: string[]; window?: string; start_period?: string; end_period?: string; include_freshness?: boolean } = {}
): Promise<RegionSeriesResponse> {
  const query = new URLSearchParams({
    indicators: (params.indicators ?? ["cpi_food_yoy"]).join(","),
    window: params.window ?? "12m",
    include_freshness: String(params.include_freshness ?? true)
  });
  if (params.start_period) query.set("start_period", params.start_period);
  if (params.end_period) query.set("end_period", params.end_period);
  const defaultIndicator = (params.indicators ?? ["cpi_food_yoy"])[0];
  return fetchJson<RegionSeriesResponse>(`/regions/${locationId}/series?${query.toString()}`, {
    location_id: locationId,
    location_name: locationId,
    window: params.window ?? "12m",
    start_period: null,
    end_period: "2026-04",
    series: [
      {
        indicator_id: defaultIndicator,
        indicator_name: defaultIndicator,
        unit: "%",
        points: [
          {
            period: "2026-04",
            value: saskatchewanSummary.metrics[defaultIndicator as keyof typeof saskatchewanSummary.metrics] ?? 0,
            trust: {
              source_id: "seeded",
              source_name: "Fallback seeded data",
              latest_period: "2026-04",
              freshness_status: "estimated",
              is_estimated: true,
              is_cached: false,
              coverage_score: 0.6
            }
          }
        ]
      }
    ],
    freshness: [],
    warnings: [{ code: "fallback", message: "Fallback series data.", severity: "warning" }]
  });
}

export async function getCompareRegions(
  locationIds: string[],
  indicators?: string[],
  params: { window?: string; start_period?: string; end_period?: string; include_series?: boolean; include_freshness?: boolean } = {}
): Promise<CompareResponse> {
  const query = new URLSearchParams({ location_ids: locationIds.join(",") });
  if (indicators?.length) query.set("indicators", indicators.join(","));
  query.set("window", params.window ?? "12m");
  query.set("include_series", String(params.include_series ?? true));
  query.set("include_freshness", String(params.include_freshness ?? true));
  if (params.start_period) query.set("start_period", params.start_period);
  if (params.end_period) query.set("end_period", params.end_period);
  return fetchJson<CompareResponse>(`/compare?${query.toString()}`, {
    locations: locationIds.map((location_id) => ({ location_id, location_name: location_id })),
    indicators: [{ indicator_id: "cpi_food_yoy", indicator_name: "Food pressure", unit: "%" }],
    period: "2026-04",
    window: params.window ?? "12m",
    rows: locationIds.map((location_id) => ({
      location_id,
      location_name: location_id,
      indicator_id: "cpi_food_yoy",
      indicator_name: "Food pressure",
      value: saskatchewanSummary.metrics.cpi_food_yoy,
      unit: "%",
      period: "2026-04",
      trust: {
        source_id: "seeded",
        source_name: "Fallback seeded data",
        latest_period: "2026-04",
        freshness_status: "estimated",
        is_estimated: true,
        is_cached: false
      }
    })),
    series: [
      {
        indicator_id: "cpi_food_yoy",
        indicator_name: "Food pressure",
        unit: "%",
        points: [{ period: "2026-04", value: saskatchewanSummary.metrics.cpi_food_yoy, trust: { freshness_status: "estimated", is_estimated: true, is_cached: false, source_id: "seeded", source_name: "Fallback seeded data" } }]
      }
    ]
    ,
    freshness: [],
    warnings: [{ code: "fallback", message: "Fallback comparison data is being shown.", severity: "warning" }]
  });
}

export async function getCurrentUser(token: string): Promise<User> {
  return fetchJsonAuthed<User>("/me", token);
}

export async function getUserPreferences(token: string): Promise<UserPreferences> {
  return fetchJsonAuthed<UserPreferences>("/me/preferences", token);
}

export async function updateUserPreferences(token: string, payload: UpdatePreferencesPayload): Promise<UserPreferences> {
  return fetchJsonAuthed<UserPreferences>("/me/preferences", token, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export async function getSavedRegions(token: string): Promise<SavedRegion[]> {
  return fetchJsonAuthed<SavedRegion[]>("/me/saved-regions", token);
}

export async function saveRegion(token: string, payload: SaveRegionPayload): Promise<SavedRegion> {
  return fetchJsonAuthed<SavedRegion>("/me/saved-regions", token, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export async function removeSavedRegion(token: string, locationId: string): Promise<void> {
  await fetchJsonAuthed<{ status: string }>(`/me/saved-regions/${locationId}`, token, { method: "DELETE" });
}

export async function getWatchlist(token: string): Promise<WatchlistRegion[]> {
  return fetchJsonAuthed<WatchlistRegion[]>("/me/watchlist", token);
}

export async function getAlertRules(token: string): Promise<AlertRule[]> {
  return fetchJsonAuthed<AlertRule[]>("/me/alerts", token);
}

export async function createAlertRule(token: string, payload: AlertRuleCreatePayload): Promise<AlertRule> {
  return fetchJsonAuthed<AlertRule>("/me/alerts", token, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export async function updateAlertRule(token: string, alertId: string, payload: AlertRuleUpdatePayload): Promise<AlertRule> {
  return fetchJsonAuthed<AlertRule>(`/me/alerts/${alertId}`, token, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export async function deleteAlertRule(token: string, alertId: string): Promise<void> {
  await fetchJsonAuthed<{ status: string }>(`/me/alerts/${alertId}`, token, { method: "DELETE" });
}

export async function enableAlertRule(token: string, alertId: string): Promise<void> {
  await fetchJsonAuthed<{ status: string }>(`/me/alerts/${alertId}/enable`, token, { method: "POST" });
}

export async function disableAlertRule(token: string, alertId: string): Promise<void> {
  await fetchJsonAuthed<{ status: string }>(`/me/alerts/${alertId}/disable`, token, { method: "POST" });
}

export async function getNotifications(token: string, unreadOnly = false): Promise<Notification[]> {
  const params = unreadOnly ? "?unread_only=true" : "";
  const data = await fetchJsonAuthed<{ items: Notification[] }>(`/me/notifications${params}`, token);
  return data.items;
}

export async function getUnreadNotificationCount(token: string): Promise<number> {
  const data = await fetchJsonAuthed<{ count: number }>("/me/notifications/unread-count", token);
  return data.count;
}

export async function markNotificationRead(token: string, notificationId: string): Promise<void> {
  await fetchJsonAuthed<{ status: string }>(`/me/notifications/${notificationId}/read`, token, { method: "POST" });
}

export async function markAllNotificationsRead(token: string): Promise<number> {
  const data = await fetchJsonAuthed<{ updated: number }>("/me/notifications/read-all", token, { method: "POST" });
  return data.updated;
}

export async function getNotificationPreferences(token: string): Promise<NotificationPreferences> {
  return fetchJsonAuthed<NotificationPreferences>("/me/notification-preferences", token);
}

export async function updateNotificationPreferences(token: string, payload: Partial<NotificationPreferences>): Promise<NotificationPreferences> {
  return fetchJsonAuthed<NotificationPreferences>("/me/notification-preferences", token, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export async function getMonthlyReports(token: string): Promise<MonthlyReport[]> {
  const data = await fetchJsonAuthed<{ items: MonthlyReport[] }>("/me/reports", token);
  return data.items;
}

export async function getMonthlyReport(token: string, reportId: string): Promise<MonthlyReport> {
  return fetchJsonAuthed<MonthlyReport>(`/me/reports/${reportId}`, token);
}

export async function generateMonthlyReport(token: string, locationId: string): Promise<MonthlyReport> {
  return fetchJsonAuthed<MonthlyReport>(`/me/reports/generate?location_id=${encodeURIComponent(locationId)}`, token, { method: "POST" });
}

export async function getAdminSummary(token: string): Promise<AdminDashboardSummary> {
  return fetchJsonAuthed<AdminDashboardSummary>("/admin/summary", token);
}

export async function getAdminSourceHealth(token: string): Promise<AdminSourceHealth[]> {
  return fetchJsonAuthed<AdminSourceHealth[]>("/admin/source-health", token);
}

export async function getAdminJobRuns(token: string, params: { job_type?: string; status?: string; limit?: number } = {}): Promise<AdminJobRun[]> {
  const query = new URLSearchParams();
  if (params.job_type) query.set("job_type", params.job_type);
  if (params.status) query.set("status", params.status);
  if (params.limit) query.set("limit", String(params.limit));
  const data = await fetchJsonAuthed<{ items: AdminJobRun[] }>(`/admin/job-runs${query.toString() ? `?${query.toString()}` : ""}`, token);
  return data.items;
}

export async function getAdminJobRun(token: string, jobRunId: string): Promise<AdminJobRun> {
  return fetchJsonAuthed<AdminJobRun>(`/admin/job-runs/${jobRunId}`, token);
}

export async function triggerAdminJob(token: string, endpoint: string, payload?: AdminJobTriggerPayload): Promise<AdminJobTriggerResponse> {
  return fetchJsonAuthed<AdminJobTriggerResponse>(`/admin/jobs/${endpoint}`, token, {
    method: "POST",
    headers: payload ? { "content-type": "application/json" } : undefined,
    body: payload ? JSON.stringify(payload) : undefined,
  });
}

export async function getAdminDataQualityFlags(
  token: string,
  params: { severity?: string; flag_type?: string; reviewed?: boolean } = {}
): Promise<DataQualityFlag[]> {
  const query = new URLSearchParams();
  if (params.severity) query.set("severity", params.severity);
  if (params.flag_type) query.set("flag_type", params.flag_type);
  if (params.reviewed !== undefined) query.set("reviewed", String(params.reviewed));
  const data = await fetchJsonAuthed<{ items: DataQualityFlag[] }>(`/admin/data-quality${query.toString() ? `?${query.toString()}` : ""}`, token);
  return data.items;
}

export async function markDataQualityFlagReviewed(token: string, flagId: number, review_note?: string): Promise<DataQualityFlag> {
  const path = `/admin/data-quality/${flagId}/review${review_note ? `?review_note=${encodeURIComponent(review_note)}` : ""}`;
  return fetchJsonAuthed<DataQualityFlag>(path, token, { method: "POST" });
}

export async function getAdminAuditLogs(token: string, params: { limit?: number } = {}): Promise<AdminAuditLog[]> {
  const query = new URLSearchParams();
  if (params.limit) query.set("limit", String(params.limit));
  return fetchJsonAuthed<AdminAuditLog[]>(`/admin/audit-logs${query.toString() ? `?${query.toString()}` : ""}`, token);
}

export async function getAdminFeatureFlags(token: string): Promise<FeatureFlag[]> {
  return fetchJsonAuthed<FeatureFlag[]>("/admin/feature-flags", token);
}

export async function updateAdminFeatureFlag(token: string, key: string, payload: FeatureFlagUpdatePayload): Promise<FeatureFlag> {
  return fetchJsonAuthed<FeatureFlag>(`/admin/feature-flags/${encodeURIComponent(key)}`, token, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function getAdminUsers(token: string): Promise<AdminUserRow[]> {
  const data = await fetchJsonAuthed<{ items: AdminUserRow[] }>("/admin/users", token);
  return data.items;
}

export async function submitFeedback(payload: FeedbackPayload, token?: string | null): Promise<BetaFeedback> {
  const headers = new Headers({ "content-type": "application/json" });
  if (token) headers.set("authorization", `Bearer ${token}`);
  const response = await fetch(`${API_BASE_URL}/feedback`, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error(`Feedback failed: ${response.status}`);
  }
  return (await response.json()) as BetaFeedback;
}

export async function getAdminFeedback(token: string, params: { status?: string; feedback_type?: string; limit?: number } = {}): Promise<BetaFeedback[]> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.feedback_type) query.set("feedback_type", params.feedback_type);
  if (params.limit) query.set("limit", String(params.limit));
  const data = await fetchJsonAuthed<{ items: BetaFeedback[] }>(`/admin/feedback${query.toString() ? `?${query.toString()}` : ""}`, token);
  return data.items;
}

export async function updateAdminFeedbackStatus(token: string, feedbackId: string, status: FeedbackStatus): Promise<BetaFeedback> {
  return fetchJsonAuthed<BetaFeedback>(`/admin/feedback/${feedbackId}`, token, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ status }),
  });
}

export async function getNpemGroups(): Promise<NpemGroup[]> {
  return fetchJson<NpemGroup[]>("/npem/groups", npemFallbackGroups);
}

export async function selectNpemGroups(params: { province: string; year?: number }) {
  const query = new URLSearchParams({ province: params.province, year: String(params.year ?? 2025) });
  return fetchJson(`/npem/groups/select?${query.toString()}`, { selected_groups: npemFallbackGroups, warnings: ["Fallback selection."] });
}

export async function getNpemVariables(): Promise<NpemVariable[]> {
  return fetchJson<NpemVariable[]>("/npem/variables", []);
}

export async function getNpemScenarios(): Promise<NpemScenario[]> {
  return fetchJson<NpemScenario[]>("/npem/scenarios", npemFallbackScenarios);
}

export async function getNpemScores(params: { province?: string; year?: number; scenario?: string } = {}): Promise<NpemScoreResponse> {
  const province = params.province ?? "AB";
  const scenario = params.scenario ?? "baseline";
  const query = new URLSearchParams({ province, year: String(params.year ?? 2025), scenario });
  return fetchJson<NpemScoreResponse>(`/npem?${query.toString()}`, npemFallbackScores(province, scenario));
}

export async function getNpemTrend(params: { province?: string; group?: string; from_year?: number; to_year?: number; scenario?: string } = {}) {
  const query = new URLSearchParams({
    province: params.province ?? "AB",
    group: params.group ?? "YA_UC",
    from_year: String(params.from_year ?? 2021),
    to_year: String(params.to_year ?? 2025),
    scenario: params.scenario ?? "baseline"
  });
  return fetchJson(`/npem/trend?${query.toString()}`, []);
}

export async function compareNpemScenarios(params: { province?: string; scenario_a?: string; scenario_b?: string; year?: number } = {}): Promise<NpemScenarioDelta[]> {
  const query = new URLSearchParams({
    province: params.province ?? "AB",
    scenario_a: params.scenario_a ?? "baseline",
    scenario_b: params.scenario_b ?? "housing_stress",
    year: String(params.year ?? 2025)
  });
  return fetchJson<NpemScenarioDelta[]>(`/npem/compare?${query.toString()}`, []);
}

export async function getNpemProvenance(params: { province?: string; group?: string; year?: number } = {}): Promise<NpemProvenance[]> {
  const query = new URLSearchParams({ province: params.province ?? "AB", group: params.group ?? "YA_UC", year: String(params.year ?? 2025) });
  return fetchJson<NpemProvenance[]>(`/npem/provenance?${query.toString()}`, []);
}

export async function getNpemCitations(params: { province?: string; group?: string; year?: number } = {}): Promise<NpemCitation[]> {
  const query = new URLSearchParams({ province: params.province ?? "AB", group: params.group ?? "YA_UC", year: String(params.year ?? 2025) });
  return fetchJson<NpemCitation[]>(`/npem/citations?${query.toString()}`, []);
}
