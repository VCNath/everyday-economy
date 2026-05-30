from pydantic import BaseModel


class NpemGroup(BaseModel):
    group_code: str
    group_label: str
    group_layer: str
    mutually_exclusive: bool
    baseline_year: int | None = None
    governance_note: str | None = None
    enabled: bool


class NpemVariable(BaseModel):
    variable_code: str
    label: str
    definition: str
    unit_code: str
    preferred_source: str | None = None
    fallback_source: str | None = None
    expected_year: int | None = None
    metric_family: str | None = None
    requires_nowcast: bool
    proxy_allowed: bool
    notes: str | None = None


class NpemScenario(BaseModel):
    scenario_code: str
    label: str
    description: str | None = None
    enabled: bool
    model_version: str
    weights: dict[str, float]


class NpemConfidence(BaseModel):
    confidence_score: float
    confidence_grade: str
    confidence_label: str
    coverage_ratio: float | None = None
    recency_score: float | None = None
    directness_score: float | None = None
    reliability_score: float | None = None
    proxy_share: float | None = None
    suppression_penalty: float | None = None


class NpemComponentScore(BaseModel):
    component_code: str
    component_label: str
    raw_value: float | None
    normalized_score: float | None
    direction: str
    imputation_level: int
    confidence_component: float | None


class NpemScore(BaseModel):
    score_id: str
    geography_code: str
    reference_year: int
    group_code: str
    group_label: str
    group_layer: str
    scenario_code: str
    base_composite: float | None
    paf_value: float | None
    final_score: float | None
    rank: int | None
    model_version: str
    confidence: NpemConfidence
    components: list[NpemComponentScore]
    proxy_warnings: list[str]
    overlap_warnings: list[str]
    provenance_summary: list[str]


class NpemScoreResponse(BaseModel):
    province: str
    geography_code: str
    reference_year: int
    scenario: NpemScenario
    latest_available_year: int
    model_version: str
    scores: list[NpemScore]
    warnings: list[str]


class NpemTrendPoint(BaseModel):
    year: int
    final_score: float | None
    confidence_grade: str | None


class NpemScenarioDelta(BaseModel):
    group_code: str
    group_label: str
    scenario_a_score: float | None
    scenario_b_score: float | None
    delta: float | None
    rank_change: int | None


class NpemProvenance(BaseModel):
    provenance_id: str
    source_system: str
    source_series_id: str | None = None
    citation_text: str | None = None
    release_date: str | None = None
    access_date: str | None = None
    transform_step: str | None = None
    licence_note: str | None = None
    source_url: str | None = None
    source_hash: str | None = None


class NpemCitation(BaseModel):
    citation_text: str | None
    source_url: str | None
    source_system: str
    licence_note: str | None
