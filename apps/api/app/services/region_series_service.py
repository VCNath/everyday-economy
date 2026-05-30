from datetime import date

from sqlalchemy import and_

from app.models.economic import ObservationModel
from app.schemas.freshness import DataWarning, MetricTrustMetadata
from app.schemas.series import IndicatorSeries, RegionSeriesResponse, SeriesPoint
from app.services.repository import EconomicRepository
from app.services.seed_data import METRICS, PERIOD
from app.services.time_window_service import resolve_time_window


def _period_label(period: date | None) -> str | None:
    if period is None:
        return None
    return period.strftime("%Y-%m")


class RegionSeriesService:
    def __init__(self, session):
        self.session = session
        self.repo = EconomicRepository(session)

    def get_series(
        self,
        *,
        location_id: str,
        indicators: list[str],
        start_period: str | None = None,
        end_period: str | None = None,
        window: str | None = None,
        include_freshness: bool = True,
    ) -> RegionSeriesResponse:
        location = self.repo.location_by_id(location_id)
        location_name = location.name if location else location_id
        freshness_index = {(row.source_id, row.dataset_id): row for row in self.repo.freshness()}
        latests = [self.repo.latest_period(indicator_id) for indicator_id in indicators]
        latest_period = max([period for period in latests if period is not None], default=None)
        resolved = resolve_time_window(
            latest_period=latest_period,
            start_period=start_period,
            end_period=end_period,
            window=window,
            default_window="12m",
        )

        series: list[IndicatorSeries] = []
        warnings: list[DataWarning] = []
        if location is None:
            warnings.append(
                DataWarning(
                    code="unknown_location",
                    message=f"Location {location_id} was not found. Returning available fallback data only.",
                )
            )
        freshness: list[MetricTrustMetadata] = []
        for indicator_id in indicators:
            indicator = self.repo.indicator_by_id(indicator_id)
            if indicator is None:
                warnings.append(DataWarning(code="unknown_indicator", message=f"Indicator {indicator_id} was not found."))
                series.append(IndicatorSeries(indicator_id=indicator_id, indicator_name=indicator_id, unit="", points=[]))
                continue

            query = self.session.query(ObservationModel).filter(
                ObservationModel.location_id == location_id,
                ObservationModel.indicator_id == indicator_id,
            )
            if resolved.start_period and resolved.end_period:
                query = query.filter(
                    and_(
                        ObservationModel.period >= resolved.start_period,
                        ObservationModel.period <= resolved.end_period,
                    )
                )
            rows = query.order_by(ObservationModel.period).all()

            points: list[SeriesPoint] = []
            if rows:
                for obs in rows:
                    period = _period_label(obs.period) or PERIOD
                    trust = self._trust_for_observation(obs, freshness_index)
                    points.append(
                        SeriesPoint(
                            period=period,
                            value=float(obs.value) if obs.value is not None else None,
                            yoy_change=float(obs.calculations[0].yoy_change) if obs.calculations and obs.calculations[0].yoy_change is not None else None,
                            mom_change=float(obs.calculations[0].mom_change) if obs.calculations and obs.calculations[0].mom_change is not None else None,
                            trust=trust,
                        )
                    )
                if include_freshness:
                    freshness.append(points[-1].trust)
            else:
                fallback = METRICS.get(location_id, {}).get(indicator_id)
                if fallback is not None:
                    trust = MetricTrustMetadata(
                        source_id="seeded",
                        source_name="Fallback seeded data",
                        latest_period=PERIOD,
                        freshness_status="estimated",
                        is_estimated=True,
                        notes="Persisted source series unavailable; showing fallback value.",
                    )
                    points.append(SeriesPoint(period=PERIOD, value=float(fallback), trust=trust))
                    if include_freshness:
                        freshness.append(trust)
                else:
                    warnings.append(
                        DataWarning(
                            code="missing_series",
                            message=f"No series points found for {indicator_id} in {location_id}.",
                        )
                    )
            series.append(
                IndicatorSeries(
                    indicator_id=indicator_id,
                    indicator_name=indicator.name,
                    unit=indicator.unit,
                    points=points,
                )
            )

        return RegionSeriesResponse(
            location_id=location_id,
            location_name=location_name,
            window=resolved.window,
            start_period=_period_label(resolved.start_period),
            end_period=_period_label(resolved.end_period),
            series=series,
            freshness=freshness,
            warnings=warnings,
        )

    def _trust_for_observation(self, obs: ObservationModel, freshness_index) -> MetricTrustMetadata:
        freshness = freshness_index.get((obs.source_id, obs.source_table_id or obs.source_series_id or ""))
        status = freshness.status if freshness and freshness.status else "healthy"
        return MetricTrustMetadata(
            source_id=obs.source_id,
            source_name=self._source_name(obs.source_id),
            source_table_id=obs.source_table_id,
            source_series_id=obs.source_series_id,
            latest_period=_period_label(obs.period),
            last_checked=freshness.last_checked_at.strftime("%Y-%m-%d") if freshness and freshness.last_checked_at else None,
            freshness_status=status,
            is_estimated=bool(obs.is_estimated),
            is_cached=False,
            coverage_score=1.0 if not obs.is_estimated else 0.6,
        )

    def _source_name(self, source_id: str | None) -> str | None:
        names = {
            "statcan": "Statistics Canada",
            "bank_of_canada": "Bank of Canada",
            "internal": "Everyday Economy",
            "seeded": "Fallback seeded data",
        }
        return names.get(source_id or "", source_id)
