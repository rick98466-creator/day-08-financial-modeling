"""Central configuration for the financial valuation model."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "financials.csv"
CASH_FLOW_OUTPUT = PROJECT_ROOT / "data" / "processed" / "forecast_cash_flows.csv"
VALUATION_OUTPUT = PROJECT_ROOT / "data" / "processed" / "valuation_results.csv"
SENSITIVITY_OUTPUT = PROJECT_ROOT / "data" / "processed" / "valuation_sensitivity.csv"
EXCEL_REPORT = PROJECT_ROOT / "reports" / "valuation_report.xlsx"

FORECAST_YEARS = 5

# Illustrative assumptions for learning, not investment advice.
REVENUE_GROWTH_RATE = 0.05
OPERATING_COST_RATIO = 0.75
TAX_RATE = 0.25
DEPRECIATION_RATIO = 0.03
CAPEX_RATIO = 0.05
WORKING_CAPITAL_RATIO = 0.01

DISCOUNT_RATE = 0.10
TERMINAL_GROWTH_RATE = 0.025

SENSITIVITY_DISCOUNT_RATES = (0.08, 0.10, 0.12)
SENSITIVITY_TERMINAL_GROWTH_RATES = (0.015, 0.025, 0.035)