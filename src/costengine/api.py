from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from costengine.estimate import estimate
from costengine.models import LineItem, Project, Variation
from costengine.tracking import cost_tracking

app = FastAPI(title="Construction cost estimator", version="0.1.0")


class ItemIn(BaseModel):
    code: str
    description: str
    unit: str
    quantity: float
    unit_rate: float
    waste_pct: float = 0.0


class VariationIn(BaseModel):
    variation_id: str
    description: str
    amount: float
    status: str = "pending"


class ProjectIn(BaseModel):
    project_id: str
    name: str
    margin_pct: float = 10.0
    gst_pct: float = 15.0
    budget: float = 0.0


class EstimateIn(BaseModel):
    project: ProjectIn
    items: list[ItemIn]
    variations: list[VariationIn] = []
    approve_threshold: float = 5000.0


class TrackingIn(BaseModel):
    budget: float
    committed: float
    actual: float
    percent_complete: float


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/estimate")
def run_estimate(payload: EstimateIn) -> dict:
    result = estimate(
        Project(**payload.project.model_dump()),
        [LineItem(**item.model_dump()) for item in payload.items],
        [Variation(**v.model_dump()) for v in payload.variations],
        approve_threshold=payload.approve_threshold,
    )
    return result.__dict__ | {"audit": [a.__dict__ | {"at": a.at.isoformat()} for a in result.audit]}


@app.post("/cost-tracking")
def run_tracking(payload: TrackingIn) -> dict:
    return cost_tracking(payload.budget, payload.committed, payload.actual, payload.percent_complete)
