from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
ASSETS = SITE / "assets"

st.set_page_config(
    page_title="LynxPath — Every minute has a path",
    page_icon=str(ASSETS / "app-icon.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Remove Streamlit's own visual chrome so the deployed app looks like the
# project's static website rather than a separate Streamlit dashboard.
st.markdown(
    """
<style>
html, body, [data-testid="stAppViewContainer"], .stApp {
    margin: 0 !important;
    padding: 0 !important;
    background: #f8fbf8 !important;
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu,
footer {
    display: none !important;
}
[data-testid="stSidebar"] {
    display: none !important;
}
.block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: none !important;
    width: 100% !important;
}
iframe {
    border: 0 !important;
    display: block !important;
}
</style>
""",
    unsafe_allow_html=True,
)


def data_uri(path: Path, mime: str) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


html = (SITE / "index.html").read_text(encoding="utf-8")
css = (SITE / "style.css").read_text(encoding="utf-8")
data_js = (SITE / "data.js").read_text(encoding="utf-8")
app_js = (SITE / "app.js").read_text(encoding="utf-8")

logo_uri = data_uri(ASSETS / "logo.jpg", "image/jpeg")
icon_uri = data_uri(ASSETS / "app-icon.png", "image/png")
pitch_uri = data_uri(SITE / "LynxPath-pitch.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation")

# Make the static site self-contained inside the Streamlit component iframe.
html = html.replace('<link rel="icon" href="assets/app-icon.png">', f'<link rel="icon" href="{icon_uri}">')
html = html.replace('<link rel="stylesheet" href="style.css">', f'<style>{css}</style>')
html = html.replace('src="assets/app-icon.png"', f'src="{icon_uri}"')
html = html.replace('src="assets/logo.jpg"', f'src="{logo_uri}"')
html = html.replace('href="LynxPath-pitch.pptx"', f'href="{pitch_uri}"')
html = html.replace('<script src="data.js"></script>', f'<script>{data_js}</script>')
html = html.replace('<script src="app.js"></script>', f'<script>{app_js}</script>')

# The site is rendered as-is, including its own navigation, responsive CSS,
# interactive scenarios, charts, timeline controls and presentation mode.
components.html(
    html,
    height=4300,
    scrolling=False,
)
