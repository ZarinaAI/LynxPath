from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import HospitalState, PatientNeed


@dataclass(frozen=True)
class CareEstimate:
    hospital_id: str
    hospital_name: str
    eligible: bool
    reason: str
    travel_minutes: int
    ed_delay_minutes: int
    resource_delay_minutes: int
    expected_minutes: int | None
    low_minutes: int | None
    high_minutes: int | None
    confidence: float
    freshness_minutes: int
    source: str
    missing_capabilities: tuple[str, ...]
    components: tuple[tuple[str, int], ...]


def _uncertainty_margin(expected: int, confidence: float, freshness_minutes: int) -> int:
    """Simple demo heuristic: widen intervals as confidence falls or data gets stale."""
    confidence = max(0.05, min(0.99, confidence))
    freshness_minutes = max(0, freshness_minutes)
    relative = 0.08 + (1.0 - confidence) * 0.32 + min(freshness_minutes, 60) / 60 * 0.16
    return max(5, round(expected * relative))


def estimate_time_to_care(hospital: HospitalState, need: PatientNeed) -> CareEstimate:
    missing = hospital.missing_capabilities(need)
    if missing:
        return CareEstimate(
            hospital_id=hospital.hospital_id,
            hospital_name=hospital.name,
            eligible=False,
            reason="Missing or temporarily unavailable: " + ", ".join(sorted(missing)),
            travel_minutes=hospital.travel_minutes,
            ed_delay_minutes=hospital.ed_delay_minutes,
            resource_delay_minutes=0,
            expected_minutes=None,
            low_minutes=None,
            high_minutes=None,
            confidence=hospital.confidence,
            freshness_minutes=hospital.freshness_minutes,
            source=hospital.source,
            missing_capabilities=tuple(sorted(missing)),
            components=(),
        )

    components: list[tuple[str, int]] = [
        ("Travel", hospital.travel_minutes),
        ("ED operational delay", hospital.ed_delay_minutes),
    ]
    resource_delay = 0
    for capability in sorted(need.required_capabilities):
        delay = max(0, int(hospital.resource_delays.get(capability, 0)))
        resource_delay += delay
        components.append((f"{capability} delay", delay))

    expected = hospital.travel_minutes + hospital.ed_delay_minutes + resource_delay
    margin = _uncertainty_margin(expected, hospital.confidence, hospital.freshness_minutes)
    low = max(hospital.travel_minutes, expected - margin)
    high = expected + margin

    return CareEstimate(
        hospital_id=hospital.hospital_id,
        hospital_name=hospital.name,
        eligible=True,
        reason=(
            "Eligible for all declared capabilities; "
            f"signal is {hospital.freshness_minutes} min old from {hospital.source}."
        ),
        travel_minutes=hospital.travel_minutes,
        ed_delay_minutes=hospital.ed_delay_minutes,
        resource_delay_minutes=resource_delay,
        expected_minutes=expected,
        low_minutes=low,
        high_minutes=high,
        confidence=hospital.confidence,
        freshness_minutes=hospital.freshness_minutes,
        source=hospital.source,
        missing_capabilities=(),
        components=tuple(components),
    )


def rank_hospitals(hospitals: Iterable[HospitalState], need: PatientNeed) -> list[CareEstimate]:
    estimates = [estimate_time_to_care(h, need) for h in hospitals]
    estimates.sort(
        key=lambda e: (
            not e.eligible,
            e.expected_minutes if e.expected_minutes is not None else 10**9,
            -e.confidence,
            e.hospital_name,
        )
    )
    return estimates


def _component_map(estimate: CareEstimate) -> dict[str, int]:
    return {name: minutes for name, minutes in estimate.components}


def explain_ranking_change(
    previous: list[CareEstimate] | None,
    current: list[CareEstimate],
) -> str:
    """Explain the largest operational changes between two ranked snapshots."""
    eligible_now = [e for e in current if e.eligible]
    if not eligible_now:
        return "No hospital currently satisfies every declared capability."
    if not previous:
        winner = eligible_now[0]
        return (
            f"Baseline: {winner.hospital_name} ranks first at about "
            f"{winner.expected_minutes} min because it has the lowest current total among eligible hospitals."
        )

    eligible_before = [e for e in previous if e.eligible]
    if not eligible_before:
        winner = eligible_now[0]
        return f"{winner.hospital_name} is now the first eligible option."

    prev_winner = eligible_before[0]
    curr_winner = eligible_now[0]
    previous_by_id = {e.hospital_id: e for e in previous}
    current_by_id = {e.hospital_id: e for e in current}

    if prev_winner.hospital_id != curr_winner.hospital_id:
        pieces: list[str] = [f"Winner changed: {prev_winner.hospital_name} → {curr_winner.hospital_name}."]
        for hospital_id in (curr_winner.hospital_id, prev_winner.hospital_id):
            estimate = current_by_id.get(hospital_id)
            prior = previous_by_id.get(hospital_id)
            if not estimate or not prior:
                continue
            if prior.eligible and not estimate.eligible:
                pieces.append(f"{estimate.hospital_name} became ineligible: {estimate.reason}.")
                continue
            if (
                not estimate.eligible
                or not prior.eligible
                or prior.expected_minutes is None
                or estimate.expected_minutes is None
            ):
                continue
            total_delta = estimate.expected_minutes - prior.expected_minutes
            now_components = _component_map(estimate)
            old_components = _component_map(prior)
            deltas = [
                (name, now_components.get(name, 0) - old_components.get(name, 0))
                for name in set(now_components) | set(old_components)
            ]
            deltas = sorted((d for d in deltas if d[1] != 0), key=lambda x: abs(x[1]), reverse=True)
            details = ", ".join(f"{name} {delta:+d} min" for name, delta in deltas[:2])
            if total_delta == 0:
                direction_text = "was unchanged overall"
            else:
                direction = "improved" if total_delta < 0 else "worsened"
                direction_text = f"{direction} by {abs(total_delta)} min"
            pieces.append(
                f"{estimate.hospital_name} {direction_text}"
                + (f" ({details})" if details else "")
                + "."
            )
        return " ".join(pieces)

    prior = previous_by_id.get(curr_winner.hospital_id)
    if prior and prior.expected_minutes is not None and curr_winner.expected_minutes is not None:
        delta = curr_winner.expected_minutes - prior.expected_minutes
        if delta:
            return (
                f"Winner unchanged: {curr_winner.hospital_name}. Its estimate moved "
                f"{delta:+d} min as the operational signals changed."
            )
    return f"Winner unchanged: {curr_winner.hospital_name}."
