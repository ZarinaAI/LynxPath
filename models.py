from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class PatientNeed:
    """Operational capability requirements supplied by a clinician or pathway."""

    name: str
    required_capabilities: frozenset[str]

    @classmethod
    def from_iterable(cls, name: str, capabilities: Iterable[str]) -> "PatientNeed":
        return cls(name=name, required_capabilities=frozenset(capabilities))


@dataclass
class HospitalState:
    """Normalized capacity snapshot consumed by the reference estimator."""

    hospital_id: str
    name: str
    travel_minutes: int
    ed_delay_minutes: int
    capabilities: set[str] = field(default_factory=set)
    resource_delays: dict[str, int] = field(default_factory=dict)
    temporary_closures: set[str] = field(default_factory=set)
    source: str = "synthetic://unknown"
    freshness_minutes: int = 0
    confidence: float = 0.75

    def missing_capabilities(self, need: PatientNeed) -> set[str]:
        available = self.capabilities - self.temporary_closures
        return set(need.required_capabilities) - available
