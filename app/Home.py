from pathlib import Path

import streamlit as st

from ui_helpers import apply_base_style, hero_card

ROOT = Path(__file__).parent

st.set_page_config(
    page_title="INF232",
    page_icon="🚀",
    layout="wide"
)

apply_base_style()

# =====================
# HERO
# =====================

hero_card(
    " INF232 — Thème B",
    "Plateforme Freelance / Client",
    "Analyse statistique et Machine Learning appliqués à un dataset "
    "de freelances généré de manière déterministe et reproductible."
)

# =====================
# MODULES
# =====================

st.markdown(
    '<div class="section-card">'
    '<div class="section-eyebrow">Sommaire</div>'
    '<div class="section-title">Modules disponibles</div>'
    '<div class="section-desc">Progression du pipeline d\'analyse, étape par étape.</div>'
    '</div>',
    unsafe_allow_html=True
)

modules = [
    ("⚙️", "Génération des données", True),
    ("📈", "Statistique descriptive", True),
    ("🔗", "Corrélation & Régression", True),
    ("🧩", "Clustering", True),
    ("🧠", "Classification supervisée", True),
    ("⏱️", "Prédiction temps réel", True),
]

pills = ""
for icon, label, live in modules:
    status_class = "on" if live else "soon"
    status_text = "Disponible" if live else "Bientôt"
    live_class = "live" if live else ""
    pills += (
        f'<div class="module-pill {live_class}">'
        f'<span>{icon}</span>'
        f'<span>{label}</span>'
        f'<span class="module-status {status_class}">{status_text}</span>'
        f'</div>'
    )

st.markdown(f'<div class="module-grid">{pills}</div>', unsafe_allow_html=True)