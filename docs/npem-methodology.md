# N.P.E.M. Methodology

N.P.E.M. stands for National Personal Economic Model. It is a transparent scoring layer for comparing economic pressure and resilience across Canadian provinces and territories by population archetype.

Public beta note: current N.P.E.M. values are deterministic demo/estimated scaffold data until production source adapters and governance review are complete. Use confidence grades, provenance, and known limitation notes when interpreting any score.

Current implementation status: deterministic demo/estimated scaffold. The schema, services, API, UI, scenario weights, confidence grading, and provenance model exist. Production source adapters still need to replace seeded/proxy raw values before public ranking claims are made.

## Source Architecture

Canonical backbone:

- Statistics Canada: population, CPI, income, labour, basket, and related national datasets.
- Bank of Canada: rates, debt, and financial context overlays.
- CMHC: housing cost and tenure context.
- CRA and Revenu Quebec: statutory direct tax parameters.
- CIHI: health expenditure structure, used cautiously.

Provincial and territorial sources may enrich local context, but they are not canonical dependencies for the v1 national model.

## Group Architecture

N.P.E.M. separates group selection from scoring.

Core archetypes are preferred for headline rankings:

- `YA_UC`: Young adults without children
- `CP_FAM`: Couple-parent families
- `LP_FAM`: Lone-parent families
- `SWA_SINGLE`: Single working-age adults
- `SENIOR_65P`: Seniors 65+

Overlay cohorts may overlap and must be labelled as such:

- `INDIG`: Indigenous identity overlay
- `IMM`: Immigrants overlay
- `RIMM`: Recent immigrants overlay
- `STUDENT`: Postsecondary students overlay
- `RENTER`: Renters overlay

Indigenous identity overlays require additional governance caution. They should not be treated as ordinary demographic filters, and small-cell/suppression risk must reduce confidence or suppress publication.

## Group Selection

Eligibility:

```text
Eligibility = 1 if PopShare >= threshold and Coverage >= 0.70
```

Thresholds:

- Provinces: population share at least 5%.
- Territories: population share at least 3% or group population count at least 1,000.

Ranking:

```text
RankScore = 0.45 * PopScore + 0.35 * Coverage + 0.20 * Distinctiveness
```

Selection:

1. Select mutually exclusive core groups first.
2. Use overlays only as labelled analytical cohorts.
3. Do not include more than two overlapping overlays in the top four.
4. Return fewer groups when coverage is insufficient.

## Components

| Code | Component | Direction |
| --- | --- | --- |
| `GCI` | GDP Contribution Index | Benefit |
| `CPII` | CPI Burden Index | Burden |
| `BBI` | Basic Basket Index | Burden |
| `HRI` | Housing Ratio Index | Burden |
| `HCI` | Health Cost Index | Burden |
| `ECI` | Education Cost Index | Burden |
| `GAI` | Gasoline and Transport Index | Burden |
| `DSI` | Discretionary Spending Index | Benefit |
| `DLI` | Debt Load Index | Burden |

Every component is normalized to 0-100. Higher final and component scores mean stronger economic position.

## Scenario Weights

Baseline:

| Component | Weight |
| --- | ---: |
| GCI | 0.10 |
| CPII | 0.10 |
| BBI | 0.15 |
| HRI | 0.20 |
| HCI | 0.10 |
| ECI | 0.05 |
| GAI | 0.08 |
| DSI | 0.12 |
| DLI | 0.10 |

Housing stress:

```text
GCI 0.07, CPII 0.10, BBI 0.16, HRI 0.30, HCI 0.08, ECI 0.04, GAI 0.10, DSI 0.08, DLI 0.07
```

Income strength:

```text
GCI 0.18, CPII 0.07, BBI 0.10, HRI 0.12, HCI 0.08, ECI 0.04, GAI 0.05, DSI 0.24, DLI 0.12
```

Scenario weights must sum to 1.00.

## Normalization

Winsorization:

```text
x_w = min(max(x, P5), P95)
```

Benefit metric:

```text
Norm+ = 100 * (x_w - P5) / (P95 - P5)
```

Burden metric:

```text
Norm- = 100 * (P95 - x_w) / (P95 - P5)
```

If `P95 - P5 = 0`, normalized score is 50.

## Provincial Adjustment Factor

```text
U = MBM_total / ModeledEssentials_prov
PAF = 1 + clip(0.25 * ((U - median_U) / median_U), -0.05, +0.05)
NPEM_final = NPEM_base * PAF
```

The adjustment is capped to +/- 5%. It should not double-count visible component burdens.

## Confidence

```text
Conf = 100 * (
  0.40 * Coverage
  + 0.25 * Recency
  + 0.20 * Directness
  + 0.15 * Reliability
)
```

Grades:

- A: 85-100, high confidence
- B: 70-84, good confidence
- C: 55-69, moderate confidence
- D: 40-54, low confidence
- E: below 40, experimental

Confidence also carries proxy share and suppression penalty.

## Provenance and Citations

Every published score should have provenance. Provenance records include:

- source system
- source series ID
- citation text
- release date
- access date
- transform step
- licence note
- source URL/hash

The current scaffold creates demo provenance records so the UI and API contract are ready before real source adapters land.

## Governance Limitations

- Seeded/demo values are not production facts.
- GCI and DLI currently use transparent proxy scaffolds.
- Overlay cohorts can overlap.
- Indigenous identity overlays require governance review before public use.
- Small-cell and suppression risk must reduce confidence or suppress output.
