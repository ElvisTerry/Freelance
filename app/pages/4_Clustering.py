# app/pages/4_Clustering.py

import sys
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).parents[2]
APP_DIR = Path(__file__).parents[1]  # dossier contenant Home.py et ui_helpers.py

sys.path.append(str(ROOT))
sys.path.append(str(APP_DIR))

from src.clustering.freelancer_clustering import FreelancerClustering
from ui_helpers import apply_base_style, hero_card, section_header, kpi_row, style_chart


# ------------------------
# CONFIG
# ------------------------
st.set_page_config(
    page_title="Clustering Freelancers",
    page_icon="🧠",
    layout="wide"
)

apply_base_style()


# ------------------------
# DATA
# ------------------------
DATA_PATH = ROOT / "data" / "freelancers.csv"

if not DATA_PATH.exists():
    st.error("Le fichier data/freelancers.csv est introuvable.")
    st.stop()

df = pd.read_csv(DATA_PATH)

model = FreelancerClustering(df)

df_clustered = model.fit(k=3)
df_clustered = model.reduce_pca()


# ------------------------
# HERO
# ------------------------
hero_card(
    " Question 3",
    "Clustering des Freelances",
    "Détection automatique de groupes naturels dans les données, "
    "sans labels prédéfinis, à partir des variables de performance et d'activité."
)


# ------------------------
# KPI
# ------------------------
kpi_row([
    ("👥", len(df_clustered), "Freelances"),
    ("🧩", df_clustered["cluster"].nunique(), "Clusters détectés"),
])




# ------------------------
# PCA VISUALISATION
# ------------------------
section_header("", "Visualisation", "Projection PCA des clusters", "Réduction à 2 dimensions pour visualiser la séparation des groupes.")

fig = px.scatter(
    df_clustered,
    x="pca_x",
    y="pca_y",
    color="cluster",
    title="Projection PCA des clusters"
)

st.plotly_chart(style_chart(fig), use_container_width=True)


# ------------------------
# PROFIL CLUSTERS
# ------------------------
section_header("", "Détail", "Profil des clusters")

st.dataframe(model.profile_clusters(), use_container_width=True)


# ------------------------
# INTERPRETATION
# ------------------------
section_header("", "Synthèse", "Interprétation métier")

st.text(model.interpret_clusters())


# ------------------------
# DISTRIBUTION
# ------------------------
section_header("", "Visualisation", "Répartition des clusters")

fig2 = px.histogram(
    df_clustered,
    x="cluster",
    color="cluster"
)

st.plotly_chart(style_chart(fig2), use_container_width=True)


# ------------------------
# ELBOW + SILHOUETTE INFO
# ------------------------
section_header("", "Diagnostic", "Analyse du nombre optimal de clusters")

col1, col2 = st.columns(2)
col1.write("**Méthode du coude :**")
col1.write(model.compute_elbow())
st.markdown(
    "<div class='section-desc'>"
    "L'inertie mesure la compacité des clusters : elle diminue mécaniquement "
    "quand k augmente. On cherche le <b>point de coude</b>, là où ajouter un "
    "cluster supplémentaire n'apporte plus qu'un gain marginal — c'est ce "
    "compromis entre simplicité et précision qui indique le k le plus pertinent."
    "</div>",
    unsafe_allow_html=True
)

col2.write("**Silhouette :**")
col2.write(model.best_k_silhouette())
st.markdown(
    "<div class='section-desc' style='margin-top:12px;'>"
    "Le score de silhouette évalue, pour chaque point, à quel point il est "
    "proche de son propre cluster comparé aux clusters voisins (échelle de "
    "-1 à 1). Plus il est élevé, mieux les groupes sont séparés. Le k "
    "affiché ci-dessus est celui qui maximise ce score sur le jeu de données."
    "</div>",
    unsafe_allow_html=True
)

# ------------------------
# RÉPONSE POUR LES INVESTISSEURS (langage simple, sans jargon)
# ------------------------
def _build_investor_message_clustering(df_clustered):
    total = len(df_clustered)
    n_clusters = df_clustered["cluster"].nunique()

    if "performance_score" not in df_clustered.columns:
        return (
            "**En résumé, pour un lecteur non spécialiste :**\n\n"
            f"L'algorithme a automatiquement réparti les {total} freelances en {n_clusters} groupes "
            "de profils qui se ressemblent, sans qu'on lui ait indiqué de catégories à l'avance."
        )

    agg_cols = [c for c in ["performance_score", "activity_score"] if c in df_clustered.columns]
    summary = (
        df_clustered.groupby("cluster")[agg_cols]
        .mean()
        .round(1)
        .join(df_clustered.groupby("cluster").size().rename("effectif"))
        .sort_values("performance_score", ascending=False)
    )

    lignes = []
    for rang, (cluster_id, row) in enumerate(summary.iterrows(), start=1):
        pct = round(row["effectif"] / total * 100, 1)
        lignes.append(
            f"- **Groupe {rang}** ({int(row['effectif'])} freelances, {pct} %) : performance moyenne "
            f"de **{row['performance_score']}/100**."
        )

    best_pct = round(summary.iloc[0]['effectif'] / total * 100, 1)
    worst_pct = round(summary.iloc[-1]['effectif'] / total * 100, 1)

    return f"""
**En résumé, pour un lecteur non spécialiste :**

Sans leur donner aucune étiquette de départ, l'algorithme a automatiquement repéré **{n_clusters} groupes**
de freelances qui se ressemblent entre eux, à partir de leur activité, leur tarif, leur satisfaction client
et leur performance :

{chr(10).join(lignes)}

**Ce que ça veut dire pour un investisseur :** il existe une frange de freelances ({best_pct} % du total)
nettement plus performante que le reste, qui mérite d'être mise en avant et fidélisée en priorité, et à
l'inverse un groupe ({worst_pct} % du total) qui aurait besoin d'accompagnement pour progresser. Ce
découpage reflète une photographie des données actuelles ; il devra être revérifié si la plateforme évolue.
"""


if "show_investor_msg_clustering" not in st.session_state:
    st.session_state.show_investor_msg_clustering = False

if st.button("💬 Réponse pour les investisseurs", use_container_width=True):
    st.session_state.show_investor_msg_clustering = not st.session_state.show_investor_msg_clustering

if st.session_state.show_investor_msg_clustering:
    st.info(_build_investor_message_clustering(df_clustered))
