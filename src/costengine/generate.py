from __future__ import annotations

import json
from pathlib import Path


def demo() -> dict:
    return {
        "project": {"project_id": "P-100", "name": "Kauri Road Upgrade", "margin_pct": 10, "gst_pct": 15, "budget": 850000},
        "items": [
            {"code": "C1", "description": "Excavation", "unit": "m3", "quantity": 1200, "unit_rate": 42.5, "waste_pct": 5},
            {"code": "C2", "description": "Concrete 25MPa", "unit": "m3", "quantity": 240, "unit_rate": 310.0, "waste_pct": 3},
            {"code": "C3", "description": "Reinforcement", "unit": "t", "quantity": 28, "unit_rate": 1850.0, "waste_pct": 7},
        ],
        "variations": [
            {"variation_id": "V1", "description": "Additional drainage", "amount": 12500.0, "status": "approved"},
            {"variation_id": "V2", "description": "Utility diversion", "amount": 8500.0, "status": "pending"},
        ],
        "approve_threshold": 5000,
    }


def main() -> None:
    path = Path("data/demo.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(demo(), indent=2))
    print(path)


if __name__ == "__main__":
    main()
