# app/pages/2_Descriptive_Analysis.py

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).parents[2]
APP_DIR = Path(__file__).parents[1]  # dossier contenant Home.py et ui_helpers.py

sys.path.append(str(ROOT))
sys.path.append(str(APP_DIR))

from src.statistics.descriptive_analysis import DescriptiveAnalysis
from ui_helpers import apply_base_style, hero_card, section_header, kpi_row, style_chart


# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Analyse Descriptive",
    page_icon="📊",
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

stats = DescriptiveAnalysis.compute_statistics(df)
summary = DescriptiveAnalysis.investor_summary(stats)


# =====================================================
# HERO
# =====================================================

hero_card(
    " Question 1",
    "Analyse descriptive des performances",
    "Comprendre la répartition des performances, identifier les valeurs "
    "atypiques et produire une synthèse compréhensible pour les investisseurs."
)


# =====================================================
# KPI
# =====================================================

kpi_row([
    ("📐", stats["mean"], "Moyenne"),
    ("🔍", stats["median"], "Médiane"),
    ("📏", stats["std"], "Écart-type"),
    ("📈", f'{stats["cv"]}%', "CV"),
    ("🚨", stats["outliers_count"], "Outliers"),
    ("⬆️", stats["max"], "Maximum"),
])



# =====================================================
# TABLEAU STATISTIQUE
# =====================================================

section_header( "","Détail", "Statistiques descriptives complètes")

table_df = pd.DataFrame({
    "Mesure": [
        "Effectif", "Moyenne", "Médiane", "Mode", "Variance", "Écart-type",
        "Minimum", "Maximum", "Étendue", "Coefficient de variation",
        "Q1", "Q2", "Q3", "IQR", "Borne inférieure", "Borne supérieure",
        "Asymétrie", "Kurtosis"
    ],
    "Valeur": [
        stats["count"], stats["mean"], stats["median"], stats["mode"],
        stats["variance"], stats["std"], stats["min"], stats["max"],
        stats["range"], f'{stats["cv"]}%', stats["q1"], stats["q2"],
        stats["q3"], stats["iqr"], stats["lower_bound"], stats["upper_bound"],
        stats["skewness"], stats["kurtosis"]
    ]
})

st.dataframe(table_df, use_container_width=True)


# =====================================================
# GRAPHIQUES
# =====================================================

section_header( "Visualisations", "Forme de la distribution", "Histogramme, boxplot, violin plot, ECDF et répartition des profils.")

fig = px.histogram(df, x="performance_score", nbins=30, title="Distribution des performances")
st.plotly_chart(style_chart(fig), use_container_width=True)

box = px.box(df, y="performance_score", points="outliers", title="Détection des valeurs atypiques")
st.plotly_chart(style_chart(box), use_container_width=True)

violin = px.violin(df, y="performance_score", box=True, title="Violin Plot des performances")
st.plotly_chart(style_chart(violin), use_container_width=True)

ecdf = px.ecdf(df, x="performance_score", title="Fonction de répartition empirique (ECDF)")
st.plotly_chart(style_chart(ecdf), use_container_width=True)

pie = px.pie(df, names="profile_type", hole=0.55, title="Répartition Premium / Standard")
st.plotly_chart(style_chart(pie), use_container_width=True)


# =====================================================
# INTERPRÉTATION MÉTIER
# =====================================================

section_header("", "Synthèse", "Destinée au comité d'investisseurs")
st.success(summary)


# =====================================================
# OUTLIERS
# =====================================================

section_header( "","Détails", "Valeurs atypiques détectées")

if stats["outliers_count"] == 0:
    st.info("Aucune valeur atypique détectée.")
else:
    outliers_df = pd.DataFrame({"Performance atypique": stats["outliers"]})
    st.dataframe(outliers_df, use_container_width=True)


# =====================================================
# EXPLICATION SCIENTIFIQUE
# =====================================================

with st.expander("📚 Explications mathématiques"):
    st.markdown(r"""

### Étendue

\[
E = x_{max} - x_{min}
\]

---

### Variance

\[
s^2=
\frac{
\sum_{i=1}^{n}
(x_i-\bar{x})^2
}
{n-1}
\]

---

### Écart-type

\[
s=\sqrt{s^2}
\]

---

### Coefficient de variation

\[
CV=
\frac{s}{\bar{x}}
\times100
\]

---

### Intervalle interquartile

\[
IQR = Q_3 - Q_1
\]

---

### Bornes de Tukey

\[
B_{inf}=Q_1-1.5IQR
\]

\[
B_{sup}=Q_3+1.5IQR
\]

---

### Asymétrie

\[
Skewness=
\frac{
E[(X-\mu)^3]
}
{\sigma^3}
\]

---

### Kurtosis

\[
K=
\frac{
E[(X-\mu)^4]
}
{\sigma^4}
-3
\]

""")


# =====================================================
# EXPORT
# =====================================================

st.download_button(
    label="📥 Télécharger les statistiques (CSV)",
    data=table_df.to_csv(index=False),
    file_name="descriptive_statistics.csv",
    mime="text/csv",
    use_container_width=True
)

# =====================================================
# RÉPONSE POUR LES INVESTISSEURS (langage simple, sans jargon)
# =====================================================

def _build_investor_message_descriptive(df, stats):
    total = len(df)
    premium_n = int((df["profile_type"] == "Premium").sum())
    standard_n = total - premium_n
    premium_pct = round(premium_n / total * 100, 1) if total else 0

    mean = stats["mean"]
    if mean >= 70:
        niveau = "un très bon niveau"
    elif mean >= 55:
        niveau = "un niveau correct"
    else:
        niveau = "un niveau qui laisse de la marge de progression"

    cv = stats["cv"]
    if cv < 15:
        dispersion = "les performances sont très homogènes : la grande majorité des freelances se ressemblent."
    elif cv < 30:
        dispersion = "les performances varient de façon modérée d'un freelance à l'autre, sans excès."
    else:
        dispersion = "les performances varient beaucoup d'un freelance à l'autre : il y a un vrai écart entre les meilleurs et les autres."

    n_out = stats["outliers_count"]
    if n_out == 0:
        outlier_txt = "Aucun cas extrême n'a été détecté : pas de freelance anormalement en dehors du lot, ni en bien ni en mal."
    else:
        outlier_txt = (
            f"{n_out} freelance(s) se démarquent nettement du reste (en très bien ou en très mal) "
            "et méritent un regard particulier."
        )

    return f"""
**En résumé, pour un lecteur non spécialiste :**

- La plateforme compte **{total} freelances**, dont **{premium_n} Premium** ({premium_pct} %) et **{standard_n} Standard**.
- Le score de performance moyen est de **{mean}/100**, ce qui correspond à {niveau}.
- Concrètement, {dispersion}
- {outlier_txt}

**Ce que ça veut dire pour un investisseur :** la plateforme a une base de freelances dans l'ensemble
solide, avec une frange de profils Premium qui tire la qualité de service vers le haut. Ces chiffres
décrivent l'état actuel des données observées ; ils ne garantissent pas une évolution future.
"""


if "show_investor_msg_descriptive" not in st.session_state:
    st.session_state.show_investor_msg_descriptive = False

if st.button("💬 Réponse pour les investisseurs", use_container_width=True):
    st.session_state.show_investor_msg_descriptive = not st.session_state.show_investor_msg_descriptive

if st.session_state.show_investor_msg_descriptive:
    st.info(_build_investor_message_descriptive(df, stats))
