# app/pages/6_Centre_IA.py

import sys
from pathlib import Path
from io import StringIO

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).parents[2]
APP_DIR = Path(__file__).parents[1]  # dossier contenant Home.py et ui_helpers.py

sys.path.append(str(ROOT))
sys.path.append(str(APP_DIR))

from src.prediction.global_predictor import GlobalPredictor
from ui_helpers import apply_base_style, hero_card, section_header, kpi_row, style_chart, chart_theme_colors


# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Centre IA",
    page_icon="🤖",
    layout="wide"
)

apply_base_style()


# =====================================================
# CHARGEMENT DES DONNÉES
# =====================================================

DATA_PATH = ROOT / "data" / "freelancers.csv"

if not DATA_PATH.exists():
    st.error("Le fichier data/freelancers.csv est introuvable.")
    st.stop()

df = pd.read_csv(DATA_PATH)
predictor = GlobalPredictor(df)


# =====================================================
# HERO
# =====================================================

hero_card(
    " Synthèse IA",
    "Centre Intelligent de Prédiction",
    "Cette interface fusionne les résultats des Questions 2, 3 et 4 : "
    "prédiction de la performance future, classification Premium / Standard, "
    "détection du cluster naturel et analyse métier automatique."
)


# =====================================================
# PARAMÈTRES UTILISATEUR
# =====================================================

section_header("", "Paramètres", "Nouveau freelance à évaluer")

col1, col2 = st.columns(2)

with col1:
    activity_score = st.slider("📈 Niveau d'activité", min_value=0, max_value=100, value=60)

with col2:
    hourly_rate = st.slider("💰 Tarif horaire (€)", min_value=5, max_value=150, value=40)


# =====================================================
# PRÉDICTION GLOBALE
# =====================================================

result = predictor.full_prediction(activity_score, hourly_rate)

performance = result["predicted_performance"]
profile = result["predicted_profile"]
confidence = result["confidence"]
cluster = result["cluster"]
comment = result["business_comment"]


# =====================================================
# KPI
# =====================================================

section_header("", "Résultats", "Sortie du moteur IA")

kpi_row([
    ("📈", performance, "Performance estimée"),
    ("📶", f"{confidence * 100:.1f}%", "Niveau de confiance"),
    ("🧩", cluster, "Groupe naturel"),
])





# =====================================================
# JAUGE DE CONFIANCE
# =====================================================

section_header("", "Fiabilité", "Confiance du modèle")

font_color, title_color, grid_color = chart_theme_colors()

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=confidence * 100,
        title={"text": "Confiance (%)", "font": {"color": title_color}},
        number={"font": {"color": title_color}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": font_color},
            "bar": {"color": "#14b8a6"},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 1,
            "bordercolor": grid_color,
            "steps": [
                {"range": [0, 50], "color": "rgba(245,158,11,0.20)"},
                {"range": [50, 80], "color": "rgba(20,184,166,0.15)"},
                {"range": [80, 100], "color": "rgba(34,197,94,0.20)"},
            ],
        },
    )
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color=font_color,
    margin=dict(t=50, b=20, l=10, r=10),
)

st.plotly_chart(fig, use_container_width=True)


# =====================================================
# PROFIL PRÉDIT
# =====================================================

section_header("", "Décision", "Classification automatique")

if profile == "Premium":
    st.success(
        "⭐ **Profil prédit : PREMIUM** — ce freelance peut être priorisé "
        "pour des opportunités stratégiques."
    )
else:
    st.warning(
        "⚪ **Profil prédit : STANDARD** — un accompagnement progressif "
        "est recommandé."
    )


# =====================================================
# COMMENTAIRE MÉTIER
# =====================================================

section_header("", "Recommandation", "Analyse métier")
st.info(comment)


# =====================================================
# EXPORT CSV
# =====================================================

section_header("", "Export", "Exporter la prédiction")

export_df = pd.DataFrame([{
    "activity_score": activity_score,
    "hourly_rate": hourly_rate,
    "predicted_performance": performance,
    "predicted_profile": profile,
    "confidence": confidence,
    "cluster": cluster,
}])

csv_buffer = StringIO()
export_df.to_csv(csv_buffer, index=False)

st.download_button(
    label="📄 Télécharger le rapport CSV",
    data=csv_buffer.getvalue(),
    file_name="prediction_freelance.csv",
    mime="text/csv",
    use_container_width=True
)


# =====================================================
# CONCLUSION
# =====================================================

section_header(
    "Conclusion", "Un moteur d'aide à la décision",
    "Le moteur combine la régression (Q2), le clustering (Q3) et la classification supervisée (Q4)."
)

st.markdown("""
Il fournit une aide à la décision rapide et cohérente. Cependant, conformément aux
recommandations du rapport :

> **la décision finale doit toujours être validée par une intervention humaine afin de limiter
> les risques commerciaux liés aux erreurs de prédiction.**
""")

# =====================================================
# RÉPONSE POUR LES INVESTISSEURS (langage simple, sans jargon)
# =====================================================

def _build_investor_message_centre_ia(activity_score, hourly_rate, performance, profile, confidence, cluster):
    conf_pct = round(confidence * 100, 1)

    if conf_pct >= 80:
        conf_txt = "un niveau de confiance élevé"
    elif conf_pct >= 50:
        conf_txt = "un niveau de confiance correct, mais pas absolu"
    else:
        conf_txt = "un niveau de confiance faible : ce résultat est à prendre avec beaucoup de prudence"

    if profile == "Premium":
        profil_txt = (
            "ce profil ressemble à celui de nos meilleurs freelances (Premium) : il pourrait être "
            "priorisé pour des missions stratégiques."
        )
    else:
        profil_txt = (
            "ce profil ressemble à celui d'un freelance Standard : un accompagnement progressif "
            "est recommandé plutôt qu'une priorisation immédiate."
        )

    return f"""
**En résumé, pour un lecteur non spécialiste :**

Pour un freelance fictif avec un niveau d'activité de **{activity_score}/100** et un tarif horaire de
**{hourly_rate} €**, notre moteur d'intelligence artificielle estime :

- une performance d'environ **{performance}/100** ;
- un profil probable **{profile}** — {profil_txt}
- un groupe naturel de référence : **cluster {cluster}** (voir la Question 3 pour son profil détaillé) ;
- ce résultat est assorti de **{conf_pct} % de confiance**, soit {conf_txt}.

**Ce que ça veut dire pour un investisseur :** ce centre IA permet de tester rapidement le profil probable
d'un nouveau freelance avant même qu'il n'ait fait ses preuves sur la plateforme. C'est un outil d'aide à
la décision qui accélère un premier tri, mais qui ne remplace pas une validation humaine avant toute
décision commerciale importante.
"""


if "show_investor_msg_centre_ia" not in st.session_state:
    st.session_state.show_investor_msg_centre_ia = False

if st.button("💬 Réponse pour les investisseurs", use_container_width=True):
    st.session_state.show_investor_msg_centre_ia = not st.session_state.show_investor_msg_centre_ia

if st.session_state.show_investor_msg_centre_ia:
    st.info(_build_investor_message_centre_ia(
        activity_score, hourly_rate, performance, profile, confidence, cluster
    ))