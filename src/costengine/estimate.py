from __future__ import annotations

from datetime import datetime, timezone

from costengine.models import AuditEntry, Estimate, LineItem, Project, Variation


def line_total(item: LineItem) -> float:
    base = item.quantity * item.unit_rate
    return round(base * (1 + item.waste_pct / 100.0), 2)


def estimate(project: Project, items: list[LineItem], variations: list[Variation] | None = None,
             approve_threshold: float = 5000.0) -> Estimate:
    base = round(sum(item.quantity * item.unit_rate for item in items), 2)
    waste = round(sum(line_total(item) - item.quantity * item.unit_rate for item in items), 2)
    approved = [v for v in (variations or []) if v.status == "approved"]
    pending = [v for v in (variations or []) if v.status == "pending"]
    variation_total = round(sum(v.amount for v in approved), 2)
    subtotal = round(base + waste + variation_total, 2)
    margin = round(subtotal * project.margin_pct / 100.0, 2)
    gst = round((subtotal + margin) * project.gst_pct / 100.0, 2)
    total = round(subtotal + margin + gst, 2)
    audit = [
        AuditEntry(datetime.now(timezone.utc), "estimate", f"items={len(items)} approved_variations={len(approved)} pending_variations={len(pending)}"),
    ]
    if pending:
        audit.append(AuditEntry(datetime.now(timezone.utc), "pending_variations",
                                ",".join(v.variation_id for v in pending)))
        if any(v.amount > approve_threshold for v in pending):
            audit.append(AuditEntry(datetime.now(timezone.utc), "approval_required", "variation above threshold"))
    return Estimate(project.project_id, base, waste, subtotal, margin, gst, total, audit)
