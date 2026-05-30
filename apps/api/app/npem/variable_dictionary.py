MODEL_VERSION = "npem_v1_demo_2026"

COMPONENTS = {
    "GCI": {"label": "GDP Contribution Index", "direction": "benefit"},
    "CPII": {"label": "CPI Burden Index", "direction": "burden"},
    "BBI": {"label": "Basic Basket Index", "direction": "burden"},
    "HRI": {"label": "Housing Ratio Index", "direction": "burden"},
    "HCI": {"label": "Health Cost Index", "direction": "burden"},
    "ECI": {"label": "Education Cost Index", "direction": "burden"},
    "GAI": {"label": "Gasoline and Transport Index", "direction": "burden"},
    "DSI": {"label": "Discretionary Spending Index", "direction": "benefit"},
    "DLI": {"label": "Debt Load Index", "direction": "burden"},
}

GROUPS = [
    {"group_code": "YA_UC", "group_label": "Young adults without children", "group_layer": "core", "mutually_exclusive": True, "baseline_year": 2025, "hh_size_default": 1.2, "adults_default": 1.2, "children_default": 0, "selection_priority": 10, "rule_json": {"age": "18-34", "children": 0}, "governance_note": "Core archetype used for headline ranking.", "enabled": True},
    {"group_code": "CP_FAM", "group_label": "Couple-parent families", "group_layer": "core", "mutually_exclusive": True, "baseline_year": 2025, "hh_size_default": 4, "adults_default": 2, "children_default": 2, "selection_priority": 20, "rule_json": {"family_type": "couple_parent"}, "governance_note": "Core archetype used for headline ranking.", "enabled": True},
    {"group_code": "LP_FAM", "group_label": "Lone-parent families", "group_layer": "core", "mutually_exclusive": True, "baseline_year": 2025, "hh_size_default": 2.6, "adults_default": 1, "children_default": 1.6, "selection_priority": 30, "rule_json": {"family_type": "lone_parent"}, "governance_note": "Core archetype used for headline ranking.", "enabled": True},
    {"group_code": "SWA_SINGLE", "group_label": "Single working-age adults", "group_layer": "core", "mutually_exclusive": True, "baseline_year": 2025, "hh_size_default": 1, "adults_default": 1, "children_default": 0, "selection_priority": 40, "rule_json": {"age": "25-64", "household": "single"}, "governance_note": "Core archetype used for headline ranking.", "enabled": True},
    {"group_code": "SENIOR_65P", "group_label": "Seniors 65+", "group_layer": "core", "mutually_exclusive": True, "baseline_year": 2025, "hh_size_default": 1.5, "adults_default": 1.5, "children_default": 0, "selection_priority": 50, "rule_json": {"age": "65+"}, "governance_note": "Core archetype used for headline ranking.", "enabled": True},
    {"group_code": "INDIG", "group_label": "Indigenous identity overlay", "group_layer": "overlay", "mutually_exclusive": False, "baseline_year": 2025, "hh_size_default": None, "adults_default": None, "children_default": None, "selection_priority": 90, "rule_json": {"identity": "indigenous"}, "governance_note": "Overlapping cohort. Requires Indigenous data governance caution; small-cell risk reduces confidence.", "enabled": True},
    {"group_code": "IMM", "group_label": "Immigrants overlay", "group_layer": "overlay", "mutually_exclusive": False, "baseline_year": 2025, "hh_size_default": None, "adults_default": None, "children_default": None, "selection_priority": 100, "rule_json": {"immigration": "immigrant"}, "governance_note": "Overlapping cohort, not a mutually exclusive headline group.", "enabled": True},
    {"group_code": "RIMM", "group_label": "Recent immigrants overlay", "group_layer": "overlay", "mutually_exclusive": False, "baseline_year": 2025, "hh_size_default": None, "adults_default": None, "children_default": None, "selection_priority": 110, "rule_json": {"immigration": "recent_immigrant"}, "governance_note": "Overlapping cohort with higher suppression risk in smaller regions.", "enabled": True},
    {"group_code": "STUDENT", "group_label": "Postsecondary students overlay", "group_layer": "overlay", "mutually_exclusive": False, "baseline_year": 2025, "hh_size_default": 1, "adults_default": 1, "children_default": 0, "selection_priority": 120, "rule_json": {"education": "postsecondary"}, "governance_note": "Overlapping cohort.", "enabled": True},
    {"group_code": "RENTER", "group_label": "Renters overlay", "group_layer": "overlay", "mutually_exclusive": False, "baseline_year": 2025, "hh_size_default": None, "adults_default": None, "children_default": None, "selection_priority": 130, "rule_json": {"tenure": "renter"}, "governance_note": "Overlapping cohort emphasizing housing stress.", "enabled": True},
]

SCENARIOS = {
    "baseline": {"label": "Baseline", "description": "Balanced National Personal Economic Model weights.", "weights": {"GCI": 0.10, "CPII": 0.10, "BBI": 0.15, "HRI": 0.20, "HCI": 0.10, "ECI": 0.05, "GAI": 0.08, "DSI": 0.12, "DLI": 0.10}},
    "housing_stress": {"label": "Housing stress", "description": "Scenario that places more weight on housing and essentials pressure.", "weights": {"GCI": 0.07, "CPII": 0.10, "BBI": 0.16, "HRI": 0.30, "HCI": 0.08, "ECI": 0.04, "GAI": 0.10, "DSI": 0.08, "DLI": 0.07}},
    "income_strength": {"label": "Income strength", "description": "Scenario that emphasizes income, discretionary room, and debt capacity.", "weights": {"GCI": 0.18, "CPII": 0.07, "BBI": 0.10, "HRI": 0.12, "HCI": 0.08, "ECI": 0.04, "GAI": 0.05, "DSI": 0.24, "DLI": 0.12}},
}

VARIABLES = [
    ("prov_pop_total", "Provincial population", "Total provincial or territorial population.", "persons", "Statistics Canada", None, 2025, "population", False, False, "Used for denominators and group selection."),
    ("group_pop_count", "Group population count", "Estimated population count for an archetype or overlay cohort.", "persons", "Statistics Canada", None, 2025, "population", False, True, "Overlay counts may overlap."),
    ("group_pop_share", "Group population share", "Group population share of province or territory.", "ratio", "Statistics Canada", None, 2025, "population", False, True, "Used for group eligibility."),
    ("prov_gdp_current", "Provincial GDP", "Current-dollar provincial GDP.", "CAD", "Statistics Canada", None, 2025, "income", False, False, None),
    ("prov_gdp_pc", "Provincial GDP per capita", "Current-dollar GDP divided by population.", "CAD/person", "Statistics Canada", None, 2025, "income", False, True, "Used as GCI proxy input."),
    ("group_median_aftertax_income", "Median after-tax income", "Group median after-tax income.", "CAD/year", "Statistics Canada", None, 2025, "income", True, True, None),
    ("group_median_employment_income", "Median employment income", "Group median employment income.", "CAD/year", "Statistics Canada", None, 2025, "income", True, True, None),
    ("group_employment_rate", "Employment rate", "Employment rate for group.", "percent", "Statistics Canada", None, 2025, "labour", True, True, None),
    ("cpi_all_items", "All-items CPI", "All-items Consumer Price Index.", "index", "Statistics Canada", None, 2025, "prices", False, False, None),
    ("cpi_shelter", "Shelter CPI", "Shelter Consumer Price Index.", "index", "Statistics Canada", None, 2025, "prices", False, False, None),
    ("cpi_transport", "Transport CPI", "Transportation Consumer Price Index.", "index", "Statistics Canada", None, 2025, "prices", False, False, None),
    ("cpi_health", "Health CPI", "Health and personal care CPI.", "index", "Statistics Canada", "CIHI", 2025, "health", False, True, None),
    ("cpi_education", "Education CPI", "Education CPI.", "index", "Statistics Canada", None, 2025, "education", False, True, None),
    ("mbm_threshold", "MBM threshold", "Market Basket Measure threshold.", "CAD/year", "Statistics Canada", None, 2025, "basket", True, False, None),
    ("housing_cost_group", "Group housing cost", "Group housing cost estimate.", "CAD/year", "CMHC", "Statistics Canada", 2025, "housing", True, True, None),
    ("housing_ratio", "Housing cost ratio", "Housing cost as share of after-tax income.", "ratio", "CMHC", "Statistics Canada", 2025, "housing", True, True, None),
    ("gasoline_transport_spend", "Gasoline and transport spend", "Group fuel and transport spending.", "CAD/year", "Statistics Canada", None, 2025, "transport", True, True, None),
    ("oop_health_spend", "Out-of-pocket health spend", "Out-of-pocket health expenditure.", "CAD/year", "CIHI", "Statistics Canada", 2025, "health", True, True, None),
    ("tuition_training_cost", "Tuition and training cost", "Tuition or training cost burden.", "CAD/year", "Statistics Canada", None, 2025, "education", True, True, None),
    ("effective_direct_tax_rate", "Effective direct tax rate", "Direct tax burden from statutory parameters.", "percent", "CRA/Revenu Quebec", None, 2025, "tax", True, True, None),
    ("savings_rate_proxy", "Savings-rate proxy", "Estimated household savings capacity.", "percent", "Statistics Canada", None, 2025, "discretionary", True, True, "Proxy variable."),
    ("debt_service_ratio", "Debt service ratio", "Debt service burden ratio.", "ratio", "Bank of Canada", None, 2025, "debt", True, True, "Group-level debt is proxy-based."),
    ("debt_to_income_ratio", "Debt-to-income ratio", "Debt load relative to income.", "ratio", "Bank of Canada", None, 2025, "debt", True, True, "Group-level debt is proxy-based."),
    ("student_debt", "Student debt", "Student debt burden.", "CAD", "Statistics Canada", None, 2025, "debt", True, True, None),
    ("discretionary_cash", "Discretionary cash", "After-tax income after essentials, taxes, and debt floor.", "CAD/year", "Everyday Economy", None, 2025, "discretionary", True, True, "Derived variable."),
]
