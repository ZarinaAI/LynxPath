# OpenCareFlow — Project Description

**OpenCareFlow is an open-source interoperability and simulation project for explainable operational time-to-care estimation.**

A clinician or operational pathway declares the resources a patient requires. OpenCareFlow filters facilities that cannot provide those resources, estimates the time to reach the required care at each eligible facility, and explains why the order changes when capacity changes.

The v0.1 reference estimator uses:

**travel time + ED operational delay + required-resource delays**

and reports a range whose width increases when data is less reliable or older.

## Core contribution

The project is centered on an **open capacity-signal schema**, not on a proprietary hospital dashboard. Different sources — synthetic simulators, FHIR-like feeds, ROR-style data, local capacity systems or research datasets — can be normalized into the same small representation before entering the eligibility and estimation logic.

The v0.1 repository includes:

- JSON Schema definitions for capacity snapshots and reproducible scenarios;
- deterministic synthetic multi-hospital scenarios;
- an eligibility engine;
- an explainable time-to-care estimator;
- uncertainty informed by confidence and data freshness;
- ranking-change explanations;
- a Streamlit reference demo;
- tests, CI, Docker Compose and contributor documentation.

## Demo story

A synthetic fracture pathway requires X-ray and orthopaedics.

At **T = 0**, Hospital A is only 8 minutes away but has a severe imaging queue. Hospital B is farther away and ranks first at 53 minutes estimated time-to-care.

At **T = 15**, Hospital B becomes busier while Hospital C clears its imaging and orthopaedics queues. Hospital C moves from second to first at 48 minutes. OpenCareFlow explains which delay components caused the ranking change.

At **T = 30**, Hospital C reports a temporary orthopaedics closure and becomes ineligible for that pathway.

## Boundary

OpenCareFlow v0.1 uses synthetic data only and is not for clinical use. It does not diagnose, infer patient needs or autonomously select a hospital. The project is intended to make the interoperability model, assumptions, uncertainty and ranking logic inspectable and reproducible.

## FOSS direction

The most valuable community work is schema review, adapters, benchmark scenarios and comparison with existing simulation/patient-flow projects. The long-term goal is not to replace national or hospital systems, but to provide a small open layer that can consume normalized operational signals and make time-to-care estimates testable.
