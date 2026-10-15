# OpenCareFlow capacity-signal schema v0.1

The schema is the main interoperability hook in OpenCareFlow.

A **capacity snapshot** describes only the operational signals needed by the reference estimator:

- travel time to each candidate facility;
- estimated ED operational delay;
- declared capabilities and temporary closures;
- resource-specific delays such as X-ray, CT, orthopaedics or operating room;
- source, freshness and confidence metadata.

The schema deliberately does **not** contain diagnosis, patient identifiers or an autonomous destination decision.

## Why this matters

Hospital and regional systems expose capacity in different formats. OpenCareFlow keeps adapters at the edge and makes the estimator consume one small, testable representation.

```text
FHIR / ROR-style / local feed / synthetic simulator
                      │
                      ▼
          OpenCareFlow capacity snapshot
                      │
           ┌──────────┴──────────┐
           ▼                     ▼
      eligibility          time-to-care
           │                     │
           └──────────┬──────────┘
                      ▼
       explainable ranked options
```

`capacity-snapshot.schema.json` is JSON Schema 2020-12. `scenario.schema.json` wraps snapshots into deterministic timelines for demos and regression tests.

**v0.1 is a research/demo schema, not a clinical interoperability standard.**
