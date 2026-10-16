from __future__ import annotations

import random

from .models import HospitalState


def advance_capacity(hospitals: list[HospitalState], seed: int | None = None) -> list[HospitalState]:
    """Optional exploratory simulator.

    The FOSDEM demo uses deterministic files from ``scenarios/`` for reproducibility.
    This helper remains available for experiments that want small random perturbations.
    """
    rng = random.Random(seed)
    updated: list[HospitalState] = []
    for h in hospitals:
        resource_delays = {
            key: max(0, value + rng.randint(-12, 18))
            for key, value in h.resource_delays.items()
        }
        ed_delay = max(3, h.ed_delay_minutes + rng.randint(-8, 12))
        confidence = max(0.55, min(0.95, h.confidence + rng.uniform(-0.04, 0.04)))
        updated.append(
            HospitalState(
                hospital_id=h.hospital_id,
                name=h.name,
                travel_minutes=h.travel_minutes,
                ed_delay_minutes=ed_delay,
                capabilities=set(h.capabilities),
                resource_delays=resource_delays,
                temporary_closures=set(h.temporary_closures),
                source=h.source,
                freshness_minutes=h.freshness_minutes + 15,
                confidence=confidence,
            )
        )
    return updated
