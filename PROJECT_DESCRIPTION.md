# LynxPath — Project Description

## Main problem

Emergency patients are often routed to the nearest suitable hospital, but **nearest does not always mean fastest access to the required care**.

A hospital may have the right specialty and available beds while still experiencing a long imaging queue, emergency-department congestion, temporary specialist unavailability, or another operational bottleneck. These conditions can create avoidable waiting after the patient reaches the hospital.

## Main goal

**LynxPath estimates how quickly a patient could reach the care they need at different eligible hospitals, using transparent operational signals.**

A clinician or operational pathway first defines the resources that are required, such as X-ray, CT, orthopaedics or a specialist team. LynxPath then:

1. filters out facilities that cannot provide the required resources;
2. estimates time-to-care for the remaining facilities;
3. shows uncertainty when the data is old or less reliable;
4. explains why one facility ranks ahead of another and why that ranking changes over time.

The v0.1 estimator is deliberately simple:

**travel time + ED operational delay + required-resource delays**

The final decision always remains with the clinician.

## Example

A synthetic fracture case requires **X-ray + orthopaedics**.

Hospital A is only 8 minutes away, but its imaging queue is very long. Hospital B is farther away but has shorter operational delays, so its estimated time-to-care is lower.

Later, conditions change: Hospital C clears its imaging queue and becomes the fastest eligible option. If Hospital C then reports a temporary orthopaedics closure, it becomes ineligible for that pathway.

LynxPath makes these changes visible and explainable.

## Core open-source idea

LynxPath is centered on an **open capacity-signal schema and reproducible simulation framework**, not on a closed hospital dashboard.

The project is designed so that synthetic simulators and, eventually, adapters for FHIR-like, regional, national or local hospital feeds can map operational capacity signals into one common structure.

This allows developers, researchers and healthcare organizations to test time-to-care models, uncertainty handling and interoperability using transparent, reproducible scenarios.

## v0.1 boundary

LynxPath v0.1 uses synthetic data only and is not intended for clinical or dispatch use. It does not diagnose patients, infer what treatment they need or autonomously choose a hospital.

## Long-term direction

The long-term goal is to provide an **open interoperability and simulation layer for real-time healthcare capacity and explainable time-to-care estimation**, complementing existing hospital and emergency systems rather than replacing them.
