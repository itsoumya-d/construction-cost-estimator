from __future__ import annotations


def cost_tracking(budget: float, committed: float, actual: float, percent_complete: float) -> dict:
    if percent_complete < 0 or percent_complete > 100:
        raise ValueError("percent_complete must be between 0 and 100")
    forecast = (actual / percent_complete * 100) if percent_complete > 0 else 0.0
    variance = round(budget - forecast, 2)
    return {
        "budget": round(budget, 2),
        "committed": round(committed, 2),
        "actual": round(actual, 2),
        "percent_complete": percent_complete,
        "forecast_at_completion": round(forecast, 2),
        "variance": variance,
        "over_budget": variance < 0,
    }
