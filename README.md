# LynxPath v0.1

> **The nearest suitable hospital is not always the hospital that can provide the required care fastest.**

LynxPath is an open-source interoperability and simulation project for **explainable operational time-to-care estimation**.

A clinician or operational pathway declares the resources a patient requires — for example **X-ray + orthopaedics**. LynxPath filters out facilities that cannot provide those resources, estimates the time required to reach the needed care at each eligible facility, and explains why the ranking changes as hospital conditions change.

The final decision always remains with the clinician.

**Synthetic data only. Not a medical device. Not for clinical or dispatch use.**

## The problem

Emergency routing cannot be reduced to distance or bed availability alone.

A nearby hospital may have the correct specialty and available beds but still have:

- a long X-ray or CT queue;
- an overloaded emergency department;
- a temporary specialist shortage;
- a required resource temporarily unavailable;
- another operational bottleneck that delays actual care.

LynxPath explores a simple question:

> **Given the resources a patient needs, which eligible facility currently offers the shortest estimated time-to-care — and why?**

## How the reference estimator works

The v0.1 estimator uses:

```text
travel time
+ ED operational delay
+ required-resource delays
= estimated time-to-care
```

The result is reported as an **estimated range**, not false precision. The range widens when capacity signals are older or less reliable.

## Example

A synthetic fracture pathway requires **X-ray + orthopaedics**.

| Facility | Travel | ED delay | X-ray + orthopaedics | Expected TTC |
|---|---:|---:|---:|---:|
| Hospital A | 8 min | 38 min | 140 min | **186 min** |
| Hospital B | 18 min | 15 min | 20 min | **53 min** |
| Hospital C | 27 min | 12 min | 25 min | **64 min** |

Hospital A is nearest, but Hospital B initially offers the shortest estimated time-to-care.

At the next synthetic snapshot, Hospital B becomes busier while Hospital C clears its imaging and orthopaedics queues. Hospital C becomes the fastest option. Later, if Hospital C reports a temporary orthopaedics closure, LynxPath marks it ineligible for that pathway.

The project explains **what changed and which delay component caused the ranking to change**.

## Core open-source contribution

The central contribution is an **open capacity-signal schema**, not a proprietary hospital dashboard.

Different sources can eventually map into a common representation:

```text
Synthetic simulators / FHIR-like feeds / ROR-style data / local systems
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

This makes it possible to test interoperability, uncertainty handling, routing logic and reproducible multi-hospital scenarios without requiring real patient data.

## What v0.1 includes

- `schema/capacity-snapshot.schema.json` — open operational capacity-signal format;
- `schema/scenario.schema.json` — deterministic scenario/timeline format;
- `lynxpath/engine.py` — eligibility, time-to-care and uncertainty estimator;
- `lynxpath/scenarios.py` — offline schema validation and scenario loading;
- `scenarios/` — reproducible fracture, stroke and trauma scenarios;
- `app.py` — Streamlit reference demo;
- `site/` — public interactive presentation website;
- `tests/` — regression tests;
- `docker-compose.yml` — one-command local demo;
- GitHub Actions CI and GitHub Pages deployment;
- Apache-2.0 license and contributor documentation.

## Public website

The `site/` directory contains a self-contained interactive presentation website. It includes the synthetic scenarios, timeline controls, uncertainty ranges and presentation mode.

### Publish with GitHub Pages

1. Push the repository to the `main` branch on GitHub.
2. Open **Settings → Pages → Build and deployment → Source → GitHub Actions**.
3. Open **Actions → Publish LynxPath website → Run workflow**, or push a new commit.
4. GitHub will provide the public website URL after deployment.

For a local preview, serve the `site/` directory with any static web server or open `site/index.html` directly.

## Run the Streamlit demo

With Docker:

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8501
```

Or run locally:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
streamlit run app.py
```

## Tests

```bash
pytest -q
```

The tests verify that:

- a farther hospital can rank ahead of the nearest hospital;
- a deterministic capacity change can change the fastest option;
- a temporary resource closure changes eligibility;
- included scenarios remain valid and rankable.

## Safety boundary

LynxPath v0.1 deliberately avoids clinical inference.

The software does **not**:

- diagnose a patient;
- decide what treatment or resources a patient needs;
- autonomously select a hospital;
- replace clinicians or emergency dispatchers;
- use real patient data in the included demo.

A clinician or authorized pathway defines the required capabilities. LynxPath only estimates operational time-to-care for eligible facilities and explains the estimate.

## FOSS direction

The most useful community contributions are:

1. review and improve the capacity-signal schema;
2. build example adapters for FHIR/ROR-style/local data;
3. contribute reproducible synthetic scenarios;
4. improve uncertainty and stale-data handling;
5. compare the estimator with patient-flow and discrete-event simulation approaches.

See [`docs/GOOD_FIRST_ISSUES.md`](docs/GOOD_FIRST_ISSUES.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Long-term goal

LynxPath aims to become an **open interoperability and simulation framework for real-time healthcare capacity and time-to-care estimation**.

The goal is not to replace national emergency systems or hospital software. It is to provide a transparent layer for representing operational capacity consistently and studying how real-world resource conditions change the time required to reach appropriate care.

## License

Apache License 2.0.
