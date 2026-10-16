# LynxPath — Project Description

## The problem

Emergency patients are often sent to the **nearest suitable hospital**, but the nearest hospital is not always the one that can provide the required care fastest.

A hospital may have the right specialty and available beds, but still have:

- a long X-ray or CT queue;
- an overloaded emergency department;
- a temporary specialist shortage;
- unavailable or delayed equipment;
- another operational bottleneck.

This can create avoidable waiting and delay treatment.

## The project

**LynxPath is an open-source project that estimates how quickly a patient could reach the care they need at different hospitals.**

A clinician or operational pathway defines the required resources, for example:

- X-ray;
- CT;
- orthopaedics;
- a specialist team.

LynxPath first filters out hospitals that cannot provide those resources.

For the remaining hospitals, it estimates:

**travel time + emergency department delay + required-resource delay**

It also reports uncertainty. When capacity information is older or less reliable, the estimated time range becomes wider.

LynxPath then shows which suitable hospitals are likely to provide the required care sooner and explains why the ranking changes.

## Example

A patient needs **X-ray + orthopaedics**.

At **T = 0**, Hospital A is only 8 minutes away but has a severe imaging queue. Hospital B is farther away but has much better availability, so Hospital B ranks first.

At **T = 15**, Hospital B becomes busier while Hospital C clears its imaging and orthopaedics queues. Hospital C moves into first place.

At **T = 30**, Hospital C reports a temporary orthopaedics closure and becomes ineligible for the pathway.

The final decision always remains with the clinician.

## What v0.1 includes

The first version includes:

- an open format for hospital-capacity data;
- JSON Schema definitions for capacity snapshots and reproducible scenarios;
- deterministic synthetic multi-hospital scenarios;
- a hospital eligibility engine;
- an explainable time-to-care estimator;
- uncertainty based on confidence and data freshness;
- explanations for ranking changes;
- a Streamlit reference demo;
- tests and CI;
- Docker Compose;
- contributor documentation.

## Core open-source contribution

LynxPath is not intended to become another closed hospital dashboard.

Its main contribution is an **open capacity-signal schema and simulation framework** that can eventually connect different operational data sources.

Possible sources include:

```text
Synthetic simulators
        ↓
Hospital systems
        ↓
FHIR-compatible feeds
        ↓
Regional / national capacity systems
        ↓
LynxPath
