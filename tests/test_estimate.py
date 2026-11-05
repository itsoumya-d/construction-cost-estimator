from costengine.estimate import estimate, line_total
from costengine.models import LineItem, Project, Variation
from costengine.tracking import cost_tracking


def item(code="C1", qty=10, rate=100, waste=2):
    return LineItem(code, "Test item", "m3", qty, rate, waste)


def test_line_total_with_waste():
    assert line_total(item()) == 1020.0


def test_estimate_math_and_variations():
    project = Project("P1", "Test", margin_pct=10, gst_pct=15, budget=20000)
    result = estimate(project, [item(qty=10, rate=100, waste=0)],
                      [Variation("V1", "Approved", 1000, "approved"), Variation("V2", "Pending", 500, "pending")])
    assert result.base == 1000.0
    assert result.subtotal == 2000.0
    assert result.margin == 200.0
    assert result.gst == 330.0
    assert result.total == 2530.0
    assert any(a.action == "pending_variations" for a in result.audit)


def test_variation_approval_threshold():
    project = Project("P1", "Test")
    result = estimate(project, [item()], [Variation("V1", "Big", 9000, "pending")], approve_threshold=5000)
    assert any(a.action == "approval_required" for a in result.audit)


def test_cost_tracking():
    result = cost_tracking(1000, 400, 300, 40)
    assert result["forecast_at_completion"] == 750.0
    assert result["variance"] == 250.0
    assert result["over_budget"] is False
