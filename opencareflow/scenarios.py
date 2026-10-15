from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .models import HospitalState, PatientNeed


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = ROOT / "scenarios"
SCHEMA_DIR = ROOT / "schema"


@dataclass(frozen=True)
class ScenarioStep:
    label: str
    event: str
    patient_need: PatientNeed
    hospitals: list[HospitalState]
    observed_at: str


@dataclass(frozen=True)
class DemoScenario:
    scenario_id: str
    title: str
    description: str
    steps: tuple[ScenarioStep, ...]


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_scenario_document(document: dict[str, Any]) -> None:
    # Inline the snapshot schema so validation is fully offline and reproducible.
    schema = _load_json(SCHEMA_DIR / "scenario.schema.json")
    capacity_schema = _load_json(SCHEMA_DIR / "capacity-snapshot.schema.json")
    schema["properties"]["steps"]["items"]["properties"]["snapshot"] = capacity_schema
    Draft202012Validator(schema).validate(document)


def _hospital_from_dict(item: dict[str, Any]) -> HospitalState:
    return HospitalState(
        hospital_id=item["hospital_id"],
        name=item["name"],
        travel_minutes=int(item["travel_minutes"]),
        ed_delay_minutes=int(item["ed_delay_minutes"]),
        capabilities=set(item["capabilities"]),
        resource_delays={k: int(v) for k, v in item["resource_delays"].items()},
        temporary_closures=set(item.get("temporary_closures", [])),
        source=item["source"],
        freshness_minutes=int(item["freshness_minutes"]),
        confidence=float(item["confidence"]),
    )


def load_scenario(path: str | Path) -> DemoScenario:
    path = Path(path)
    document = _load_json(path)
    validate_scenario_document(document)
    steps: list[ScenarioStep] = []
    for item in document["steps"]:
        snapshot = item["snapshot"]
        need_doc = snapshot["patient_need"]
        steps.append(
            ScenarioStep(
                label=item["label"],
                event=item.get("event", ""),
                patient_need=PatientNeed.from_iterable(
                    need_doc["name"], need_doc["required_capabilities"]
                ),
                hospitals=[_hospital_from_dict(h) for h in snapshot["hospitals"]],
                observed_at=snapshot["observed_at"],
            )
        )
    return DemoScenario(
        scenario_id=document["id"],
        title=document["title"],
        description=document["description"],
        steps=tuple(steps),
    )


def list_scenarios() -> list[Path]:
    return sorted(SCENARIO_DIR.glob("*.json"))
