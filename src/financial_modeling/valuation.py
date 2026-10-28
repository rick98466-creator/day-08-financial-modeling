"""Discounted cash flow valuation."""

import pandas as pd

from financial_modeling.config import (
    DISCOUNT_RATE,
    TERMINAL_GROWTH_RATE,
    VALUATION_OUTPUT,
)


def calculate_dcf(forecast: pd.DataFrame) -> dict:
    """Calculate enterprise value from forecast FCFF."""
    if forecast.empty:
        raise ValueError("Forecast cannot be empty.")

    if DISCOUNT_RATE <= TERMINAL_GROWTH_RATE:
        raise ValueError(
            "Discount rate must exceed terminal growth rate."
        )

    if DISCOUNT_RATE <= -1:
        raise ValueError("Discount rate must exceed -100%.")

    if TERMINAL_GROWTH_RATE <= -1:
        raise ValueError("Terminal growth rate must exceed -100%.")

    forecast = forecast.sort_values("year").reset_index(drop=True)

    if (forecast["year"].diff().dropna() != 1).any():
        raise ValueError("Forecast years must be consecutive.")

    if not forecast["fcff"].map(
        lambda value: pd.notna(value) and abs(value) != float("inf")
    ).all():
        raise ValueError("FCFF must contain finite values.")

    periods = range(1, len(forecast) + 1)
    discount_factors = [
        (1 + DISCOUNT_RATE) ** period for period in periods
    ]

    forecast["discount_factor"] = discount_factors
    forecast["present_value_fcff"] = (
        forecast["fcff"] / forecast["discount_factor"]
    )

    final_fcff = float(forecast.iloc[-1]["fcff"])
    terminal_value = (
        final_fcff * (1 + TERMINAL_GROWTH_RATE)
        / (DISCOUNT_RATE - TERMINAL_GROWTH_RATE)
    )

    terminal_present_value = (
        terminal_value / discount_factors[-1]
    )

    pv_forecast_cash_flows = float(
        forecast["present_value_fcff"].sum()
    )
    enterprise_value = (
        pv_forecast_cash_flows + terminal_present_value
    )

    result = {
        "pv_forecast_cash_flows": pv_forecast_cash_flows,
        "terminal_value": terminal_value,
        "terminal_present_value": terminal_present_value,
        "enterprise_value": enterprise_value,
        "discount_rate": DISCOUNT_RATE,
        "terminal_growth_rate": TERMINAL_GROWTH_RATE,
    }

    VALUATION_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([result]).to_csv(VALUATION_OUTPUT, index=False)

    return result