# Ready-to-open `good first issue` ideas

These are deliberately scoped so a new contributor can complete one without understanding the entire project.

## 1. Add a fourth reproducible scenario

**Label:** `good first issue`, `scenario`

Create one synthetic scenario that demonstrates a different resource bottleneck, validate it against `schema/scenario.schema.json`, and add one regression assertion.

## 2. Add a capacity-snapshot CLI validator

**Label:** `good first issue`, `tooling`

Add `python -m lynxpath.validate path/to/file.json` that prints either `valid` or a readable schema error. Include tests.

## 3. Add a minimal FHIR-shaped example adapter

**Label:** `good first issue`, `adapter`, `interoperability`

Use a **synthetic** JSON fixture shaped like a FHIR feed and map it into the LynxPath capacity snapshot. Do not connect to a real endpoint.

## 4. Improve stale-signal visualization

**Label:** `good first issue`, `frontend`

In the Streamlit table, visually flag freshness > 15 minutes and explain that stale signals widen uncertainty.

## 5. Add a benchmark notebook or script

**Label:** `good first issue`, `research`

Run all checked-in scenarios, export ranked results to CSV and make it easy to compare estimator revisions over time.
