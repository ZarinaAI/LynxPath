from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from opencareflow.data import CAPABILITIES
from opencareflow.engine import explain_ranking_change, rank_hospitals
from opencareflow.models import PatientNeed
from opencareflow.scenarios import list_scenarios, load_scenario

st.set_page_config(page_title="LynxPath v0.1", page_icon="site/assets/app-icon.png", layout="wide")

st.image("site/assets/logo.jpg", width=360)
st.title("LynxPath")
st.caption("Open capacity signals + explainable time-to-care • v0.1 synthetic demo")

st.warning(
    "Synthetic data only. Not a medical device and not for clinical or dispatch use. "
    "The clinician/pathway supplies required capabilities; the demo only estimates operational time-to-care."
)

scenario_paths = list_scenarios()
scenario_by_title = {load_scenario(path).title: path for path in scenario_paths}

with st.sidebar:
    st.header("Reproducible scenario")
    scenario_title = st.selectbox("Scenario", list(scenario_by_title))
    scenario_path: Path = scenario_by_title[scenario_title]
    scenario = load_scenario(scenario_path)

    if "scenario_id" not in st.session_state or st.session_state.scenario_id != scenario.scenario_id:
        st.session_state.scenario_id = scenario.scenario_id
        st.session_state.step_index = 0

    step_index = int(st.session_state.get("step_index", 0))
    step_index = max(0, min(step_index, len(scenario.steps) - 1))
    step = scenario.steps[step_index]

    st.caption(scenario.description)
    st.divider()
    st.subheader("Timeline")
    st.write(f"**{step.label}**")
    st.caption(step.event or "Synthetic snapshot")
    cprev, cnext = st.columns(2)
    if cprev.button("← Previous", use_container_width=True, disabled=step_index == 0):
        st.session_state.step_index = step_index - 1
        st.rerun()
    if cnext.button("Next →", use_container_width=True, disabled=step_index >= len(scenario.steps) - 1):
        st.session_state.step_index = step_index + 1
        st.rerun()

    st.divider()
    st.subheader("Declared patient requirements")
    selected = st.multiselect(
        "Required capabilities",
        options=list(CAPABILITIES),
        default=sorted(step.patient_need.required_capabilities),
        format_func=lambda x: CAPABILITIES.get(x, x),
        help="The demo never infers diagnosis or capabilities. The user/pathway declares them.",
    )
    need = PatientNeed.from_iterable(step.patient_need.name, selected)

    st.divider()
    st.caption(f"Source: `{scenario_path.name}`")
    st.caption(f"Snapshot time: {step.observed_at}")

current_estimates = rank_hospitals(step.hospitals, need)
previous_estimates = None
if step_index > 0:
    previous_step = scenario.steps[step_index - 1]
    previous_estimates = rank_hospitals(previous_step.hospitals, need)

eligible = [e for e in current_estimates if e.eligible]

if not selected:
    st.info("Select at least one capability to produce an operational ranking.")
elif eligible:
    winner = eligible[0]
    nearest = min(
        (e for e in eligible),
        key=lambda e: e.travel_minutes,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Fastest eligible option", winner.hospital_name)
    c2.metric("Expected time-to-care", f"{winner.expected_minutes} min")
    c3.metric("Uncertainty range", f"{winner.low_minutes}–{winner.high_minutes} min")
    c4.metric("Signal freshness", f"{winner.freshness_minutes} min old")

    if nearest.hospital_id != winner.hospital_id:
        st.success(
            f"The nearest eligible hospital is {nearest.hospital_name} ({nearest.travel_minutes} min travel), "
            f"but the current operational estimate ranks {winner.hospital_name} first."
        )
else:
    st.error("No hospital in this synthetic snapshot satisfies every declared capability.")

st.subheader("Why the ranking changed")
st.info(explain_ranking_change(previous_estimates, current_estimates))

rows = []
rank_number = 0
for e in current_estimates:
    if e.eligible:
        rank_number += 1
    rows.append(
        {
            "Rank": rank_number if e.eligible else "—",
            "Hospital": e.hospital_name,
            "Eligible": "Yes" if e.eligible else "No",
            "Travel": f"{e.travel_minutes} min",
            "ED delay": f"{e.ed_delay_minutes} min",
            "Resource delay": f"{e.resource_delay_minutes} min" if e.eligible else "—",
            "Expected TTC": f"{e.expected_minutes} min" if e.eligible else "—",
            "Range": f"{e.low_minutes}–{e.high_minutes} min" if e.eligible else "—",
            "Freshness": f"{e.freshness_minutes} min",
            "Confidence": f"{e.confidence:.0%}",
            "Reason": e.reason,
        }
    )

st.subheader("Ranked options")
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.subheader("Inspectable estimate")
for e in current_estimates:
    title = f"{e.hospital_name} — {'eligible' if e.eligible else 'excluded'}"
    with st.expander(title, expanded=bool(eligible and e.hospital_id == eligible[0].hospital_id)):
        if not e.eligible:
            st.write(e.reason)
            continue
        st.write(
            f"**Expected:** {e.expected_minutes} min · **Range:** {e.low_minutes}–{e.high_minutes} min · "
            f"**Confidence:** {e.confidence:.0%} · **Freshness:** {e.freshness_minutes} min"
        )
        st.caption(f"Signal source: {e.source}")
        component_df = pd.DataFrame(e.components, columns=["Component", "Minutes"])
        st.bar_chart(component_df.set_index("Component"))

st.divider()
st.markdown(
    "**Open schema → eligibility → estimator → explainable ranking.** "
    "See `schema/` and `scenarios/` in the repository."
)
st.caption("LynxPath v0.1 • Apache-2.0 • synthetic data only • not for clinical use")
