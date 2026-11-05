from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class LineItem:
    code: str
    description: str
    unit: str
    quantity: float
    unit_rate: float
    waste_pct: float = 0.0


@dataclass
class Variation:
    variation_id: str
    description: str
    amount: float
    status: str = "pending"


@dataclass
class Project:
    project_id: str
    name: str
    margin_pct: float = 10.0
    gst_pct: float = 15.0
    budget: float = 0.0


@dataclass
class AuditEntry:
    at: datetime
    action: str
    detail: str


@dataclass
class Estimate:
    project_id: str
    base: float
    waste: float
    subtotal: float
    margin: float
    gst: float
    total: float
    audit: list[AuditEntry] = field(default_factory=list)
