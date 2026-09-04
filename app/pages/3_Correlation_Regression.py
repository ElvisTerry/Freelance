# app/pages/3_Correlation_Regression.py

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).parents[2]
APP_DIR = Path(__file__).parents[1]  # dossier contenant Home.py et ui_helpers.py

sys.path.append(str(ROOT))
sys.path.append(str(APP_DIR))

from src.analysis.correlation_analysis import CorrelationAnalysis
from ui_helpers import apply_base_style, hero_card, section_header, kpi_row, style_chart


# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Corrélation & Régression",
    page_icon="📈",
    layout="wide"
)

apply_base_style()


# =====================================================
# DATA
# =====================================================

DATA_PATH = ROOT / "data" / "freelancers.csv"

if not DATA_PATH.exists():
    st.error("Le fichier data/freelancers.csv est introuvable.")
    st.stop()

df = pd.read_csv(DATA_PATH)

activity = CorrelationAnalysis.performance_vs_activity(df)
hourly = CorrelationAnalysis.performance_vs_hourly_rate(df)
reg = CorrelationAnalysis.regression_model(df)


# =====================================================
# HERO
# =====================================================

hero_card(
    " Question 2",
    "Corrélation & Régression",
    "Analyse du lien entre performance, activité et tarification, "
    "et capacité de prédiction des freelances à partir d'un modèle appris."
)


# =====================================================
# KPI
# =====================================================

kpi_row([
    ("🔗", activity["correlation"], "Corrélation Activité"),
    ("💶", hourly["correlation"], "Corrélation Tarif"),
    ("🧠", reg["r2"], "R² du modèle"),
    ("📏", reg["mae"], "MAE"),
])




# =====================================================
# VISUALISATION : SCATTER + RÉGRESSION
# =====================================================

section_header("", "Visualisation", "Relation activité vs performance")

fig = px.scatter(
    df,
    x="activity_score",
    y="performance_score",
    trendline="ols",
    opacity=0.6
)

st.plotly_chart(style_chart(fig), use_container_width=True)


# =====================================================
# HEATMAP CORRELATION
# =====================================================

section_header("", "Visualisation", "Matrice de corrélation")

corr = df[[
    "performance_score",
    "activity_score",
    "hourly_rate"
]].corr()

fig2 = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="Blues"
)

st.plotly_chart(style_chart(fig2), use_container_width=True)


# =====================================================
# RÉSIDUS
# =====================================================

section_header("", "Diagnostic", "Analyse des résidus")

X = df[["activity_score"]]
y = df["performance_score"]

model = reg["model"]
pred = model.predict(X)
residuals = y - pred

fig3 = px.histogram(
    residuals,
    nbins=30,
    title="Distribution des erreurs (résidus)"
)

st.plotly_chart(style_chart(fig3), use_container_width=True)


# =====================================================
# PRÉDICTION INTERACTIVE
# =====================================================

section_header("", "Interactif", "Prédiction en temps réel")

activity_input = st.slider(
    "Niveau d'activité",
    0, 100, 50
)

pred_value = CorrelationAnalysis.predict_performance(
    model,
    activity_input
)

st.success(f" Performance prédite : **{pred_value}/100**")

st.info(
    f" Interprétation : une activité de {activity_input} donne une estimation "
    "de performance basée sur le modèle appris."
)


# =====================================================
# INTERPRÉTATION MÉTIER
# =====================================================

section_header("", "Synthèse", "Analyse métier")

interpretation = CorrelationAnalysis.business_interpretation(
    activity,
    reg
)

st.write(interpretation)


# =====================================================
# LIMITES
# =====================================================

with st.expander("⚠️ Limites du modèle"):

    st.markdown("""

- Corrélation ≠ causalité
- Modèle linéaire simplifié
- Variables non observées ignorées
- Sensible aux valeurs extrêmes
- Données synthétiques (simulation)
- Risque d'extrapolation hors domaine

👉 Conclusion : outil d'aide à la décision, pas de substitution humaine.
""")

# =====================================================
# RÉPONSE POUR LES INVESTISSEURS (langage simple, sans jargon)
# =====================================================

def _corr_words(r):
    a = abs(r)
    if a >= 0.8:
        return "très fort"
    elif a >= 0.6:
        return "fort"
    elif a >= 0.4:
        return "modéré"
    elif a >= 0.2:
        return "faible"
    else:
        return "quasi nul"


def _build_investor_message_regression(activity, hourly, reg):
    r_act = activity["correlation"]
    r_rate = hourly["correlation"]
    r2 = reg["r2"]
    mae = reg["mae"]

    sens_act = "à la hausse" if r_act >= 0 else "à la baisse"
    sens_rate = "à la hausse" if r_rate >= 0 else "à la baisse"

    r2_pct = round(r2 * 100, 1)

    if r2 >= 0.7:
        qualite = "un modèle assez fiable"
    elif r2 >= 0.4:
        qualite = "un modèle qui donne une indication utile, mais imparfaite"
    else:
        qualite = "un modèle qui ne doit être vu que comme une première indication, peu précise"

    return f"""
**En résumé, pour un lecteur non spécialiste :**

- Plus un freelance est **actif** sur la plateforme, plus sa performance a tendance à évoluer
  {sens_act} — le lien est **{_corr_words(r_act)}**.
- Plus le **tarif horaire** d'un freelance est élevé, plus sa performance a tendance à évoluer
  {sens_rate} — le lien est **{_corr_words(r_rate)}**.
- En ne regardant que le niveau d'activité, on peut expliquer environ **{r2_pct} %** des différences
  de performance observées entre freelances. Le reste dépend d'autres facteurs (tarif, satisfaction
  client, réactivité...).
- En pratique, l'estimation de performance donnée par ce modèle se trompe en moyenne de
  **{mae} points sur 100** : {qualite} pour orienter une décision, mais pas pour trancher seul.

**Ce que ça veut dire pour un investisseur :** encourager l'activité des freelances sur la plateforme
est associé à de meilleures performances, mais ce lien statistique ne prouve pas qu'agir sur l'un
change automatiquement l'autre. C'est un signal utile pour prioriser des actions, pas une garantie
de résultat.
"""


if "show_investor_msg_regression" not in st.session_state:
    st.session_state.show_investor_msg_regression = False

if st.button("💬 Réponse pour les investisseurs", use_container_width=True):
    st.session_state.show_investor_msg_regression = not st.session_state.show_investor_msg_regression

if st.session_state.show_investor_msg_regression:
    st.info(_build_investor_message_regression(activity, hourly, reg))
