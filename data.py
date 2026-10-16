from __future__ import annotations

from .models import PatientNeed


CAPABILITIES = {
    "xray": "X-ray",
    "ct": "CT",
    "orthopedics": "Orthopaedics",
    "stroke": "Stroke unit",
    "trauma": "Trauma capability",
    "or": "Operating room",
}

PATIENT_PRESETS = {
    "Suspected leg fracture": PatientNeed.from_iterable(
        "Suspected leg fracture", ["xray", "orthopedics"]
    ),
    "Possible major trauma": PatientNeed.from_iterable(
        "Possible major trauma", ["ct", "trauma", "or"]
    ),
    "Possible stroke": PatientNeed.from_iterable("Possible stroke", ["ct", "stroke"]),
}
