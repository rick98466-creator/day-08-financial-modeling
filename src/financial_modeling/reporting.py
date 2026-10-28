"""DCF sensitivity analysis and Excel reporting."""

import pandas as pd

from financial_modeling.config import (
    SENSITIVITY_DISCOUNT_RATES,
    SENSITIVITY_TERMINAL_GROWTH_RATES,
    EXCEL_REPORT,
)


def calculate_sensitivity(forecast: pd.DataFrame) -> pd.DataFrame:
    """Calculate enterprise value across discount/growth assumptions."""
    cash_flows = forecast["fcff"].astype(float).tolist()
    final_fcff = cash_flows[-1]
    rows = []

    for discount_rate in SENSITIVITY_DISCOUNT_RATES:
        for growth_rate in SENSITIVITY_TERMINAL_GROWTH_RATES:
            if discount_rate <= growth_rate:
                raise ValueError(
                    "Each discount rate must exceed terminal growth."
                )

            pv_forecast = sum(
                cash_flow / (1 + discount_rate) ** period
                for period, cash_flow in enumerate(cash_flows, start=1)
            )

            terminal_value = (
                final_fcff * (1 + growth_rate)
                / (discount_rate - growth_rate)
            )
            pv_terminal = terminal_value / (
                1 + discount_rate
            ) ** len(cash_flows)

            rows.append({
                "discount_rate": discount_rate,
                "terminal_growth_rate": growth_rate,
                "enterprise_value": pv_forecast + pv_terminal,
            })

    return pd.DataFrame(rows)


def export_valuation_report(
    forecast: pd.DataFrame,
    valuation: dict,
    sensitivity: pd.DataFrame,
) -> None:
    """Write forecasts, valuation summary and sensitivity to Excel."""
    EXCEL_REPORT.parent.mkdir(parents=True, exist_ok=True)

    summary = pd.DataFrame(
        [{"metric": key, "value": value} for key, value in valuation.items()]
    )

    with pd.ExcelWriter(EXCEL_REPORT, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Valuation Summary", index=False)
        forecast.to_excel(writer, sheet_name="Cash Flow Forecast", index=False)
        sensitivity.to_excel(
            writer, sheet_name="Sensitivity Analysis", index=False
        )