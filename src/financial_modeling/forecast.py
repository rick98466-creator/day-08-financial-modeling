"""Forecast revenue and free cash flow for company valuation."""

import pandas as pd

from financial_modeling.config import (
    FORECAST_YEARS,
    REVENUE_GROWTH_RATE,
    OPERATING_COST_RATIO,
    TAX_RATE,
    DEPRECIATION_RATIO,
    CAPEX_RATIO,
    WORKING_CAPITAL_RATIO,
    CASH_FLOW_OUTPUT,
)


def forecast_free_cash_flow(df: pd.DataFrame) -> pd.DataFrame:
    """Project annual financials and calculate FCFF."""
    last = df.sort_values("year").iloc[-1]
    rows = []

    for period in range(1, FORECAST_YEARS + 1):
        year = int(last["year"]) + period
        revenue = float(last["revenue"]) * (
            1 + REVENUE_GROWTH_RATE
        ) ** period

        operating_costs = revenue * OPERATING_COST_RATIO
        depreciation = revenue * DEPRECIATION_RATIO
        ebit = revenue - operating_costs - depreciation
        taxes = max(ebit, 0) * TAX_RATE
        nopat = ebit - taxes
        capital_expenditure = revenue * CAPEX_RATIO
        change_in_working_capital = revenue * WORKING_CAPITAL_RATIO

        fcff = (
            nopat
            + depreciation
            - capital_expenditure
            - change_in_working_capital
        )

        rows.append({
            "year": year,
            "revenue": revenue,
            "operating_costs": operating_costs,
            "depreciation": depreciation,
            "ebit": ebit,
            "taxes": taxes,
            "nopat": nopat,
            "capital_expenditure": capital_expenditure,
            "change_in_working_capital": change_in_working_capital,
            "fcff": fcff,
        })

    forecast = pd.DataFrame(rows)
    CASH_FLOW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    forecast.to_csv(CASH_FLOW_OUTPUT, index=False)

    return forecast