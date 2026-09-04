# app/pages/5_Classification.py

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

from src.classification.premium_classifier import PremiumClassifier
from ui_helpers import apply_base_style, hero_card, section_header, kpi_row, style_chart


# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Classification Supervisée",
    page_icon="🤖",
    layout="wide"
)

apply_base_style()


# =====================================================
# DONNÉES
# =====================================================

DATA_PATH = ROOT / "data" / "freelancers.csv"

if not DATA_PATH.exists():
    st.error("Le fichier data/freelancers.csv est introuvable.")
    st.stop()

df = pd.read_csv(DATA_PATH)

classifier = PremiumClassifier(df)

logistic = classifier.logistic_model()
rf = classifier.random_forest_model()

models = [logistic, rf]
best_model = rf if rf["accuracy"] >= logistic["accuracy"] else logistic


# =====================================================
# HERO
# =====================================================

hero_card(
    " Question 4",
    "Classification Supervisée",
    "Peut-on orienter automatiquement un nouveau freelance vers un profil "
    f'Premium ou Standard ? Meilleur modèle retenu : <b>{best_model["name"]}</b>.'
)


# =====================================================
# KPI — MEILLEUR MODÈLE
# =====================================================

section_header("", "Résultat", "Meilleur modèle", f'{best_model["name"]} sélectionné sur la base de son accuracy.')

kpi_row([
    ("📈", best_model["accuracy"], "Accuracy"),
    ("⚔️", best_model["precision"], "Precision"),
    ("🔎", best_model["recall"], "Recall"),
    ("⚖️", best_model["f1"], "F1"),
    ("🧠", best_model["auc"], "AUC"),
])





# =====================================================
# COMPARAISON DES MODÈLES
# =====================================================

section_header("", "Comparaison", "Régression logistique vs Random Forest")

comparison_df = pd.DataFrame({
    "Model": [logistic["name"], rf["name"]],
    "Accuracy": [logistic["accuracy"], rf["accuracy"]],
    "Precision": [logistic["precision"], rf["precision"]],
    "Recall": [logistic["recall"], rf["recall"]],
    "F1": [logistic["f1"], rf["f1"]],
})

st.dataframe(comparison_df, use_container_width=True)

fig = px.bar(
    comparison_df,
    x="Model",
    y=["Accuracy", "Precision", "Recall", "F1"],
    barmode="group",
    title="Comparaison des performances"
)

st.plotly_chart(style_chart(fig), use_container_width=True)


# =====================================================
# MATRICES DE CONFUSION
# =====================================================

section_header("", "Diagnostic", "Matrices de confusion")

tab1, tab2 = st.tabs(["Logistic Regression", "Random Forest"])

with tab1:
    cm = logistic["confusion_matrix"]
    fig = px.imshow(
        cm,
        text_auto=True,
        labels=dict(x="Prédit", y="Réel"),
        title="Matrice de confusion - Logistic Regression"
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

with tab2:
    cm = rf["confusion_matrix"]
    fig = px.imshow(
        cm,
        text_auto=True,
        labels=dict(x="Prédit", y="Réel"),
        title="Matrice de confusion - Random Forest"
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)


# =====================================================
# IMPORTANCE DES VARIABLES
# =====================================================

section_header("", "Explicabilité", "Importance des variables")

importance_df = pd.DataFrame({
    "Feature": list(rf["feature_importance"].keys()),
    "Importance": list(rf["feature_importance"].values()),
})

fig = px.bar(importance_df, x="Feature", y="Importance", title="Importance des indicateurs")
st.plotly_chart(style_chart(fig), use_container_width=True)


# =====================================================
# VALIDATION CROISÉE
# =====================================================

section_header("", "Robustesse", "Validation croisée")

st.success(f"Accuracy moyenne : **{best_model['cv_mean']}** · Écart-type : **{best_model['cv_std']}**")


# =====================================================
# SIMULATEUR
# =====================================================

section_header("", "Interactif", "Simuler un nouveau freelance")

col1, col2 = st.columns(2)

with col1:
    activity = st.slider("Niveau d'activité", 0, 100, 60)

with col2:
    rate = st.slider("Tarif horaire", 5, 150, 40)

prediction = classifier.predict_profile(best_model["model"], activity, rate)

if prediction == "Premium":
    st.success(f"⭐ **Profil prédit : PREMIUM** — Activité : {activity} · Tarif : {rate} €")
else:
    st.warning(f"⚪ **Profil prédit : STANDARD** — Activité : {activity} · Tarif : {rate} €")


# =====================================================
# ANALYSE MÉTIER
# =====================================================

section_header("", "Synthèse", "Analyse des risques commerciaux")

analysis = classifier.business_risk_analysis(best_model["accuracy"])
st.info(analysis)

st.markdown("""

### Risques 

- Mauvaise orientation d'un excellent freelance.
- Surévaluation d'un profil standard.
- Décisions commerciales biaisées.
- Nécessité d'une validation humaine.

### Recommandation

Le système doit être utilisé comme :

> **un outil d'aide à la décision et non une autorité absolue.**

""")


# =====================================================
# CONCLUSION
# =====================================================

section_header(
     "Conclusion", "Aide à la décision, pas remplacement du jugement",
    "Les données permettent raisonnablement d'automatiser une première orientation Premium / Standard."
)

st.markdown("""
- une erreur commerciale reste possible car perfectible ;
- la supervision humaine demeure indispensable.

Le modèle retenu constitue donc une aide à la décision et non un remplacement du jugement commercial.
""")


# =====================================================
# RÉPONSE POUR LES INVESTISSEURS (langage simple, sans jargon)
# =====================================================

def _build_investor_message_classification(best_model):
    acc_pct = round(best_model["accuracy"] * 100, 1)
    erreurs_pct = round(100 - acc_pct, 1)

    cm = best_model.get("confusion_matrix")
    detail_erreurs = ""
    try:
        # matrice de confusion attendue au format [[VN, FP], [FN, VP]]
        fp = int(cm[0][1])
        fn = int(cm[1][0])
        detail_erreurs = (
            f" Concrètement, sur l'ensemble testé, le modèle a classé à tort {fp} freelance(s) "
            f"Standard comme Premium, et {fn} freelance(s) Premium comme Standard."
        )
    except Exception:
        pass

    if acc_pct >= 90:
        qualif = "très fiable"
    elif acc_pct >= 75:
        qualif = "globalement fiable"
    else:
        qualif = "à utiliser avec prudence"

    return f"""
**En résumé, pour un lecteur non spécialiste :**

- Sur 100 nouveaux freelances évalués, le modèle ({best_model["name"]}) devine correctement le profil
  (Premium ou Standard) d'environ **{acc_pct} d'entre eux**, et se trompe sur environ **{erreurs_pct}**.{detail_erreurs}
- Ce niveau de performance est jugé **{qualif}** pour orienter automatiquement un nouveau profil.

**Ce que ça veut dire pour un investisseur :** ce modèle peut faire gagner du temps en pré-triant les
nouveaux freelances, mais il n'est pas parfait. Les quelques erreurs possibles (un excellent profil mal
classé, ou l'inverse) justifient qu'une personne valide la décision avant tout impact commercial
important - le modèle est une aide, pas un remplacement du jugement humain.
"""


if "show_investor_msg_classification" not in st.session_state:
    st.session_state.show_investor_msg_classification = False

if st.button("💬 Réponse pour les investisseurs", use_container_width=True):
    st.session_state.show_investor_msg_classification = not st.session_state.show_investor_msg_classification

if st.session_state.show_investor_msg_classification:
    st.info(_build_investor_message_classification(best_model))