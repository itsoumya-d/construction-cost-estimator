# construction-cost-estimator

[![ci](https://github.com/itsoumya-d/construction-cost-estimator/actions/workflows/ci.yml/badge.svg)](https://github.com/itsoumya-d/construction-cost-estimator/actions/workflows/ci.yml)

A tested reference for construction cost management and quantity-surveying
software:

- Bill-of-quantities line items with quantities, unit rates and waste factors.
- Estimate build-up: base, waste, approved variations, margin and GST.
- Pending variations, approval thresholds and audit entries.
- Cost tracking: budget, committed, actual, forecast at completion, variance
  and over-budget flag.
- FastAPI surface and synthetic demo data.

This is a **reference implementation**, not a claim of production quantity
surveying or CivCost experience. It uses synthetic rates and no live project
data.

## Run

```bash
uv venv --python 3.12
source .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn costengine.api:app --reload
python -m costengine.generate
```

## License

MIT
