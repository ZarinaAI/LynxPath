from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from lynxpath.data import CAPABILITIES
from lynxpath.engine import explain_ranking_change, rank_hospitals
from lynxpath.models import PatientNeed
from lynxpath.scenarios import list_scenarios, load_scenario


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="LynxPath",
    page_icon="site/assets/app-icon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------
# CUSTOM STYLE
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* ---------- Main page ---------- */

    .stApp {
        background-color: #f7faf8;
        color: #123b35;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 5rem;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    /* ---------- Typography ---------- */

    h1, h2, h3 {
        color: #0b4037;
    }

    p {
        color: #55716b;
    }

    /* ---------- Navigation ---------- */

    .lynx-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 1.1rem;
        border-bottom: 1px solid #dce7e3;
        margin-bottom: 5rem;
    }

    .lynx-brand {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0b4037;
        letter-spacing: -0.04em;
    }

    .lynx-brand span {
        color: #008c70;
    }

    .lynx-nav-links {
        color: #0b4037;
        font-size: 1rem;
    }

    /* ---------- Hero ---------- */

    .eyebrow {
        color: #008c70;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.22em;
        margin-top: 1rem;
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: clamp(3rem, 5vw, 5rem);
        line-height: 0.98;
        font-weight: 800;
        letter-spacing: -0.05em;
        color: #0b4037;
        margin-bottom: 0.3rem;
    }

    .hero-script {
        font-family: Georgia, "Times New Roman", serif;
        font-style: italic;
        font-weight: 400;
        font-size: clamp(2.5rem, 4.5vw, 4.5rem);
        line-height: 1.1;
        color: #0b4037;
        margin-bottom: 2.2rem;
    }

    .hero-copy {
        font-size: 1.25rem;
        line-height: 1.75;
        color: #58726c;
        max-width: 680px;
        margin-bottom: 2rem;
    }

    .hero-note {
        color: #708983;
        margin-top: 1.5rem;
        font-size: 0.95rem;
    }

    /* ---------- Links / buttons ---------- */

    .hero-button {
        display: inline-block;
        background: #0b4d43;
        color: #ffffff !important;
        text-decoration: none;
        padding: 0.9rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        margin-right: 1.2rem;
    }

    .hero-button:hover {
        background: #08705f;
    }

    .secondary-link {
        color: #0b4037 !important;
        text-decoration: none;
        font-weight: 500;
    }

    .stButton > button {
        border-radius: 8px;
        border: 1px solid #c7d8d2;
        background: #ffffff;
        color: #0b4037;
        min-height: 2.8rem;
    }

    .stButton > button:hover {
        border-color: #008c70;
        color: #008c70;
    }

    /* ---------- Demo cards ---------- */

    .demo-intro {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    .demo-eyebrow {
        color: #008c70;
        font-weight: 700;
        letter-spacing: 0.14em;
        font-size: 0.8rem;
    }

    .demo-title {
        font-size: 2.7rem;
        font-weight: 750;
        color: #0b4037;
        margin-top: 0.5rem;
        margin-bottom: 0.6rem;
    }

    /* ---------- Streamlit widgets ---------- */

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e1ebe7;
        border-radius: 12px;
        padding: 1.1rem;
    }

    [data-testid="stMetricLabel"] {
        color: #617a74;
    }

    div[data-baseweb="select"] > div {
        border-radius: 8px;
        border-color: #d3e1dc;
    }

    /* ---------- Alerts ---------- */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* ---------- Tables ---------- */

    [data-testid="stDataFrame"] {
        border: 1px solid #e1ebe7;
        border-radius: 10px;
        overflow: hidden;
    }

    /* ---------- Hide sidebar ---------- */

    [data-testid="stSidebar"] {
        display: none;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------

st.markdown(
    """<div class="lynx-nav">
<div class="lynx-brand">Lynx<span>Path</span></div>
<div class="lynx-nav-links">The approach &nbsp;&nbsp;&nbsp;&nbsp; Interactive demo</div>
</div>""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

hero_left, hero_right = st.columns([1.05, 1], gap="large")

with hero_left:

    st.markdown(
        """<div class="eyebrow">OPEN SOURCE · RESEARCH DEMO · V0.1</div>
<div class="hero-title">The nearest hospital.</div>
<div class="hero-script">Or the fastest care?</div>
<div class="hero-copy">
The closest suitable hospital is not always the fastest route
to the care a patient needs. LynxPath compares travel time,
emergency-department delay and required-resource delays
to make that operational difference visible.
</div>
<a class="hero-button" href="#interactive-demo">Explore the live demo ↗</a>
<a class="secondary-link" href="#how-it-works">How it works ↓</a>
<div class="hero-note">● &nbsp; Transparent estimates. Reproducible scenarios.</div>""",
        unsafe_allow_html=True,
    )

with hero_right:
    st.image(
        "site/assets/logo.jpg",
        use_container_width=True,
    )


st.write("")
st.write("")
st.divider()


# ---------------------------------------------------------
# HOW IT WORKS
# ---------------------------------------------------------

st.markdown(
    """<div id="how-it-works"></div>
<div class="demo-intro">
<div class="demo-eyebrow">HOW IT WORKS</div>
<div class="demo-title">Compare operational time-to-care.</div>
<p>
The clinician or pathway declares the resources required.
LynxPath excludes facilities that cannot provide them and
compares the remaining options using travel time, ED delay
and required-resource delays.
</p>
</div>""",
    unsafe_allow_html=True,
)


how1, how2, how3 = st.columns(3)

with how1:
    st.markdown("### 01 · Declare")
    st.write(
        "Specify the capabilities required by the pathway, such as X-ray "
        "and orthopaedics."
    )

with how2:
    st.markdown("### 02 · Compare")
    st.write(
        "Estimate operational time-to-care for every eligible hospital."
    )

with how3:
    st.markdown("### 03 · Explain")
    st.write(
        "Show why one option ranks above another and why the ranking changes."
    )


st.write("")
st.write("")
st.divider()


# ---------------------------------------------------------
# INTERACTIVE DEMO
# ---------------------------------------------------------

st.markdown(
    """<div id="interactive-demo"></div>
<div class="demo-intro">
<div class="demo-eyebrow">INTERACTIVE DEMO</div>
<div class="demo-title">Reproducible hospital scenario</div>
<p>
Explore a synthetic hospital network and see how changing
operational conditions affect the ranking.
</p>
</div>""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# LOAD SCENARIO
# ---------------------------------------------------------

scenario_paths = list_scenarios()

scenario_by_title = {
    load_scenario(path).title: path
    for path in scenario_paths
}


control1, control2 = st.columns([1.3, 1])

with control1:

    scenario_title = st.selectbox(
        "Scenario",
        list(scenario_by_title),
    )

scenario_path: Path = scenario_by_title[scenario_title]
scenario = load_scenario(scenario_path)


if (
    "scenario_id" not in st.session_state
    or st.session_state.scenario_id != scenario.scenario_id
):
    st.session_state.scenario_id = scenario.scenario_id
    st.session_state.step_index = 0


step_index = int(
    st.session_state.get("step_index", 0)
)

step_index = max(
    0,
    min(
        step_index,
        len(scenario.steps) - 1,
    ),
)

step = scenario.steps[step_index]


with control2:

    st.markdown("**Current timeline**")
    st.write(step.label)
    st.caption(step.event or "Synthetic snapshot")


st.caption(scenario.description)


# ---------------------------------------------------------
# TIMELINE
# ---------------------------------------------------------

st.write("")

timeline1, timeline2, timeline3 = st.columns(
    [1, 1, 5]
)

with timeline1:

    if st.button(
        "← Previous",
        width="stretch",
        disabled=step_index == 0,
    ):
        st.session_state.step_index = step_index - 1
        st.rerun()


with timeline2:

    if st.button(
        "Next →",
        width="stretch",
        disabled=step_index >= len(scenario.steps) - 1,
    ):
        st.session_state.step_index = step_index + 1
        st.rerun()


with timeline3:

    st.caption(
        f"Snapshot: {step.observed_at}"
    )


# ---------------------------------------------------------
# PATIENT REQUIREMENTS
# ---------------------------------------------------------

st.write("")
st.markdown("### Declared patient requirements")

selected = st.multiselect(
    "Required capabilities",
    options=list(CAPABILITIES),
    default=sorted(
        step.patient_need.required_capabilities
    ),
    format_func=lambda x: CAPABILITIES.get(x, x),
    help=(
        "The demo never infers diagnosis or required capabilities. "
        "The user or pathway declares them."
    ),
)

need = PatientNeed.from_iterable(
    step.patient_need.name,
    selected,
)


# ---------------------------------------------------------
# RUN ESTIMATOR
# ---------------------------------------------------------

current_estimates = rank_hospitals(
    step.hospitals,
    need,
)

previous_estimates = None

if step_index > 0:

    previous_step = scenario.steps[
        step_index - 1
    ]

    previous_estimates = rank_hospitals(
        previous_step.hospitals,
        need,
    )


eligible = [
    estimate
    for estimate in current_estimates
    if estimate.eligible
]


# ---------------------------------------------------------
# SAFETY NOTICE
# ---------------------------------------------------------

st.warning(
    "Synthetic data only. Not a medical device and not for clinical "
    "or dispatch use. The clinician/pathway supplies required capabilities; "
    "the demo only estimates operational time-to-care."
)


# ---------------------------------------------------------
# RESULT SUMMARY
# ---------------------------------------------------------

if not selected:

    st.info(
        "Select at least one capability to produce an operational ranking."
    )

elif eligible:

    winner = eligible[0]

    nearest = min(
        eligible,
        key=lambda estimate: estimate.travel_minutes,
    )

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Fastest eligible option",
        winner.hospital_name,
    )

    metric2.metric(
        "Expected time-to-care",
        f"{winner.expected_minutes} min",
    )

    metric3.metric(
        "Uncertainty range",
        f"{winner.low_minutes}–{winner.high_minutes} min",
    )

    metric4.metric(
        "Signal freshness",
        f"{winner.freshness_minutes} min old",
    )

    if nearest.hospital_id != winner.hospital_id:

        st.success(
            f"The nearest eligible hospital is "
            f"{nearest.hospital_name} "
            f"({nearest.travel_minutes} min travel), "
            f"but the current operational estimate ranks "
            f"{winner.hospital_name} first."
        )

else:

    st.error(
        "No hospital in this synthetic snapshot satisfies "
        "every declared capability."
    )


# ---------------------------------------------------------
# RANKING CHANGE EXPLANATION
# ---------------------------------------------------------

st.write("")
st.markdown("## Why the ranking changed")

st.info(
    explain_ranking_change(
        previous_estimates,
        current_estimates,
    )
)


# ---------------------------------------------------------
# RANKED OPTIONS
# ---------------------------------------------------------

rows = []

rank_number = 0

for estimate in current_estimates:

    if estimate.eligible:
        rank_number += 1

    rows.append(
        {
            "Rank": (
                str(rank_number)
                if estimate.eligible
                else "—"
            ),
            "Hospital": estimate.hospital_name,
            "Eligible": (
                "Yes"
                if estimate.eligible
                else "No"
            ),
            "Travel": (
                f"{estimate.travel_minutes} min"
            ),
            "ED delay": (
                f"{estimate.ed_delay_minutes} min"
            ),
            "Resource delay": (
                f"{estimate.resource_delay_minutes} min"
                if estimate.eligible
                else "—"
            ),
            "Expected TTC": (
                f"{estimate.expected_minutes} min"
                if estimate.eligible
                else "—"
            ),
            "Range": (
                f"{estimate.low_minutes}–"
                f"{estimate.high_minutes} min"
                if estimate.eligible
                else "—"
            ),
            "Freshness": (
                f"{estimate.freshness_minutes} min"
            ),
            "Confidence": (
                f"{estimate.confidence:.0%}"
            ),
            "Reason": estimate.reason,
        }
    )


st.write("")
st.markdown("## Ranked options")

st.dataframe(
    pd.DataFrame(rows),
    width="stretch",
    hide_index=True,
)


# ---------------------------------------------------------
# INSPECTABLE ESTIMATES
# ---------------------------------------------------------

st.write("")
st.markdown("## Inspectable estimate")

for estimate in current_estimates:

    title = (
        f"{estimate.hospital_name} — "
        f"{'eligible' if estimate.eligible else 'excluded'}"
    )

    with st.expander(
        title,
        expanded=bool(
            eligible
            and estimate.hospital_id
            == eligible[0].hospital_id
        ),
    ):

        if not estimate.eligible:

            st.write(
                estimate.reason
            )

            continue

        st.write(
            f"**Expected:** {estimate.expected_minutes} min · "
            f"**Range:** {estimate.low_minutes}–"
            f"{estimate.high_minutes} min · "
            f"**Confidence:** {estimate.confidence:.0%} · "
            f"**Freshness:** {estimate.freshness_minutes} min"
        )

        st.caption(
            f"Signal source: {estimate.source}"
        )

        component_df = pd.DataFrame(
            estimate.components,
            columns=[
                "Component",
                "Minutes",
            ],
        )

        st.bar_chart(
            component_df.set_index(
                "Component"
            )
        )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.write("")
st.divider()

st.markdown(
    "**Open schema → eligibility → estimator → explainable ranking.** "
    "See `schema/` and `scenarios/` in the repository."
)

st.caption(
    "LynxPath v0.1 • Apache-2.0 • "
    "synthetic data only • not for clinical use"
)
