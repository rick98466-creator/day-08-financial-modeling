"""Validation rules for historical financial data."""

import numpy as np
import pandas as pd

from financial_modeling.data_loader import REQUIRED_COLUMNS


def validate_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate required fields and basic financial constraints."""
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if df.empty:
        raise ValueError("Financial dataset cannot be empty.")

    result = df[REQUIRED_COLUMNS].copy()

    if result.isna().any().any():
        raise ValueError("Financial data cannot contain missing values.")

    numeric_columns = [column for column in REQUIRED_COLUMNS if column != "year"]

    for column in numeric_columns:
        result[column] = pd.to_numeric(result[column], errors="raise")

    if not np.isfinite(result[numeric_columns].to_numpy(dtype=float)).all():
        raise ValueError("Financial data must contain finite numeric values.")

    if result["year"].duplicated().any():
        raise ValueError("Years must not be duplicated.")

    if not result["year"].is_monotonic_increasing:
        raise ValueError("Years must be in ascending order.")

    if (result["revenue"] <= 0).any():
        raise ValueError("Revenue must be positive.")

    nonnegative_columns = [
        "operating_costs",
        "capital_expenditure",
        "depreciation",
    ]

    for column in nonnegative_columns:
        if (result[column] < 0).any():
            raise ValueError(f"{column} cannot be negative.")

    if not result["tax_rate"].between(0, 1).all():
        raise ValueError("Tax rate must be between 0 and 1.")

    if (result["change_in_working_capital"] < 0).any():
        raise ValueError("Change in working capital cannot be negative.")

    result["year"] = result["year"].astype(int)

    return result