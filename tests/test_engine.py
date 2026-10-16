from pathlib import Path

from lynxpath.engine import explain_ranking_change, rank_hospitals
from lynxpath.scenarios import load_scenario, validate_scenario_document


ROOT = Path(__file__).resolve().parents[1]


def test_fracture_baseline_prefers_farther_hospital_b():
    scenario = load_scenario(ROOT / "scenarios" / "fracture-capacity-shift.json")
    step = scenario.steps[0]
    estimates = rank_hospitals(step.hospitals, step.patient_need)
    eligible = [e for e in estimates if e.eligible]

    assert eligible[0].hospital_id == "B"
    assert eligible[0].expected_minutes == 53
    assert eligible[0].travel_minutes == 18

    hospital_a = next(e for e in eligible if e.hospital_id == "A")
    assert hospital_a.travel_minutes == 8
    assert hospital_a.expected_minutes == 186


def test_fracture_step_one_changes_winner_to_c():
    scenario = load_scenario(ROOT / "scenarios" / "fracture-capacity-shift.json")
    before = rank_hospitals(scenario.steps[0].hospitals, scenario.steps[0].patient_need)
    after = rank_hospitals(scenario.steps[1].hospitals, scenario.steps[1].patient_need)

    assert [e for e in after if e.eligible][0].hospital_id == "C"
    explanation = explain_ranking_change(before, after)
    assert "Winner changed" in explanation
    assert "Hospital C" in explanation
    assert "Hospital B" in explanation


def test_temporary_closure_changes_eligibility():
    scenario = load_scenario(ROOT / "scenarios" / "fracture-capacity-shift.json")
    step = scenario.steps[2]
    estimates = rank_hospitals(step.hospitals, step.patient_need)
    hospital_c = next(e for e in estimates if e.hospital_id == "C")

    assert not hospital_c.eligible
    assert "orthopedics" in hospital_c.missing_capabilities


def test_all_scenarios_validate_and_rank():
    for scenario_file in (ROOT / "scenarios").glob("*.json"):
        scenario = load_scenario(scenario_file)
        assert scenario.steps
        for step in scenario.steps:
            estimates = rank_hospitals(step.hospitals, step.patient_need)
            assert len(estimates) == len(step.hospitals)


def test_schema_rejects_missing_required_data():
    bad_document = {
        "scenario_version": "0.1.0",
        "id": "bad",
        "title": "Bad",
        "description": "Missing snapshot fields",
        "steps": [{"label": "T0", "snapshot": {}}],
    }
    try:
        validate_scenario_document(bad_document)
    except Exception:
        pass
    else:
        raise AssertionError("Invalid scenario unexpectedly passed schema validation")
