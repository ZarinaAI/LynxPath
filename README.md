# Lynx path v0.1

> **Open capacity signals + explainable time-to-care estimation.**

Lynx path is an open-source research/demo project for one operational question:

> Given a clinician-declared set of required capabilities, which eligible facility currently has the shortest estimated time to those resources — and why?

The reference estimator combines:

```text
travel time
+ ED operational delay
+ required-resource delays
= estimated time-to-care
```

It then exposes the estimate as a **range**, together with signal freshness, confidence and a plain-language explanation of ranking changes.

**Synthetic data only. Not a medical device. Not for clinical or dispatch use.**

## Why this project exists

The nearest hospital can be operationally slower than a farther hospital.

In the reproducible fracture demo:

| Facility | Travel | ED delay | X-ray + orthopaedics | Expected TTC |
|---|---:|---:|---:|---:|
| Hospital A | 8 min | 38 min | 140 min | **186 min** |
| Hospital B | 18 min | 15 min | 20 min | **53 min** |
| Hospital C | 27 min | 12 min | 25 min | **64 min** |

Fifteen synthetic minutes later, the operational signals change and **Hospital C becomes the fastest option at 48 min**. Lynx path explains the switch instead of showing a static distance list.

## The technical hook: an open capacity-signal schema

Adapters from different systems should map into one small vendor-neutral representation:

```text
FHIR / ROR-style / local feeds / synthetic simulator
                        │
                        ▼
            LynxPath capacity snapshot
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
        eligibility          time-to-care
             │                     │
             └──────────┬──────────┘
                        ▼
          explainable ranked options
```

See [`schema/`](schema/) for JSON Schema 2020-12 definitions and [`scenarios/`](scenarios/) for deterministic fixtures.

## One-command demo

Requires Docker + Docker Compose:

```bash
docker compose up --build
```

Open `http://localhost:8501`.

The default scenario is fully synthetic and reproducible. Use **Next →** to advance the network and watch the ranking change.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Tests

```bash
pytest -q
```

The tests verify:

- a farther hospital can rank ahead of the nearest hospital;
- a deterministic capacity change flips the winner;
- a temporary closure changes eligibility;
- all checked-in scenarios validate against the schema and remain rankable.

## What v0.1 contains

- `schema/capacity-snapshot.schema.json` — open operational signal format;
- `schema/scenario.schema.json` — deterministic demo/benchmark timeline format;
- `lynxpath/engine.py` — eligibility + time-to-care + uncertainty;
- `lynxpath/scenarios.py` — offline schema validation and scenario loading;
- `scenarios/` — reproducible fracture, stroke and trauma examples;
- `app.py` — Streamlit reference interface;
- `tests/` — regression tests;
- `docker-compose.yml` — one-command demo;
- GitHub Actions CI, Apache-2.0 license and contributor documentation.

## Safety boundary

Lynx path v0.1 deliberately avoids clinical inference.

The user or an authorized pathway supplies the required capabilities. The software does **not**:

- diagnose a patient;
- infer what treatment a patient needs;
- autonomously choose a destination;
- use real patient data in the included demo.

The current repository is for open-source engineering, simulation and research discussion only.

## Community roadmap

The next useful contributions are intentionally narrow:

1. review and challenge the capacity-signal schema;
2. add adapters that translate example FHIR/ROR-style/local data into the schema;
3. contribute reproducible synthetic scenarios;
4. improve uncertainty and stale-data handling;
5. benchmark the estimator against discrete-event simulation approaches.

See [`docs/GOOD_FIRST_ISSUES.md`](docs/GOOD_FIRST_ISSUES.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

Apache License 2.0.
