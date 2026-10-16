# Contributing to LynxPath

LynxPath v0.1 is intentionally small. Contributions should preserve four principles:

1. **Clinical requirements are inputs.** The project must not infer diagnosis or required care in the reference demo.
2. **Operational estimates are inspectable.** Keep components, freshness and uncertainty visible.
3. **Scenarios are reproducible.** Prefer checked-in deterministic fixtures over screenshots or undocumented demos.
4. **Synthetic/demo behavior is never represented as clinically validated.**

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
streamlit run app.py
```

Or:

```bash
docker compose up --build
```

## Good first contributions

- add a new synthetic scenario under `scenarios/`;
- add a schema example for a new operational signal;
- improve explanation text without changing ranking semantics;
- add tests for stale-data uncertainty;
- write an adapter prototype that converts an example external payload into a capacity snapshot.

See `docs/GOOD_FIRST_ISSUES.md` for ready-to-open issue descriptions.

## Pull requests

Please include:

- a short description of the behavior change;
- tests for ranking, eligibility or schema changes;
- an updated scenario when user-visible demo behavior changes;
- no real patient data, credentials or confidential hospital data.

## Schema changes

Treat `schema/capacity-snapshot.schema.json` as a public interface. For breaking changes, explain why the existing field cannot represent the signal and update `schema_version` plus all fixtures.
