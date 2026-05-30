"""Bank of Canada Valet series used by the Phase 2 data engine."""

BANK_OF_CANADA_SERIES = {
    "boc_policy_rate": {
        "series_id": "V39079",
        "dataset_id": "policy_rate",
        "unit": "%",
        "notes": "Target for the overnight rate.",
    },
    "cad_usd_exchange_rate": {
        "series_id": "FXUSDCAD",
        "dataset_id": "cad_usd_exchange_rate",
        "unit": "CAD per USD",
        "notes": "Daily CAD per USD exchange rate. Confirm exact Valet series if BOC changes IDs.",
    },
}
