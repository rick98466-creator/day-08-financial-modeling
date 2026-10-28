"""Load historical financial data for the valuation model."""

import pandas as pd

from financial_modeling.config import INPUT_FILE

REQUIRED_COLUMNS = [
    "year",
    "revenue",
    "operating_costs",
    "tax_rate",
    "capital_expenditure",
    "depreciation",
    "change_in_working_capital",
]


def load_financial_data() -> pd.DataFrame:
    """Load financial data and check its basic structure."""
    df = pd.read_csv(INPUT_FILE)

    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if df.empty:
        raise ValueError("Financial dataset cannot be empty.")

    return df[REQUIRED_COLUMNS].copy()