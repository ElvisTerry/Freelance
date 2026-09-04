import json
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).parents[2]
APP_DIR = Path(__file__).parents[1]  # dossier contenant Home.py et ui_helpers.py

sys.path.append(str(ROOT))
sys.path.append(str(APP_DIR))


from src.generator.seed_generator import SeedGenerator
from src.generator.freelance_generator import FreelanceGenerator
from ui_helpers import apply_base_style, hero_card, section_header, kpi_row, style_chart


# =====================
# CONFIG
# =====================

st.set_page_config(
    page_title="Data Generation",
    page_icon="⚙️",
    layout="wide"
)

apply_base_style()


# =====================
# HERO
# =====================

hero_card(
    " Pipeline de génération",
    "Génération des données",
    "INF232 - Thème B · Plateforme Freelance / Client &amp; Génération déterministe et reproductible"
)


# =====================
# NOM CHEF
# =====================

section_header( "Étape 1", "Chef de groupe", "Identifie la seed déterministe du dataset.")

chief_name = st.text_input(
    "Nom complet du chef de groupe",
    placeholder="Ex: Terry Ndzié"
)


if chief_name:

    normalized = SeedGenerator.normalize_name(
        chief_name
    )

    seed = SeedGenerator.generate_seed(
        chief_name
    )

    st.success(
        f"Nom normalisé : {normalized}"
    )

    st.info(
        f"Seed générée : {seed}"
    )

    # =====================
    # TAILLE
    # =====================

    section_header( "Étape 2", "Taille du dataset", "Choisis un preset ou un mode personnalisé.")

    col1, col2, col3 = st.columns(3)

    if col1.button("1000 freelances"):
        n = 1000

    elif col2.button("1200 freelances (recommandé)"):
        n = 1200

    elif col3.button("2000 freelances"):
        n = 2000

    else:
        n = st.slider(
            "Mode personnalisé",
            500,
            5000,
            1200,
            100
        )

    # =====================
    # GENERATION
    # =====================

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    if st.button(
        "🔁 Générer les données",
        use_container_width=True
    ):

        generator = FreelanceGenerator(
            chief_name
        )

        df = generator.generate_dataset(
            n
        )

        generator.save_csv(df)
        generator.save_excel(df)
        generator.save_json(df)

        st.session_state["df"] = df

        st.success("Dataset généré avec succès !")


# =====================
# AFFICHAGE
# =====================

if "df" in st.session_state:

    df = st.session_state["df"]

    # =====================
    # KPI
    # =====================

    total = len(df)
    premium = (df.profile_type == "Premium").sum()
    standard = (df.profile_type == "Standard").sum()
    mean_perf = round(df.performance_score.mean(), 2)
    satisfaction = round(df.client_satisfaction.mean(), 2)

    kpi_row([
        ("👥", total, "Freelances"),
        ("👑", premium, "Premium"),
        ("📋", standard, "Standard"),
        ("⚡", mean_perf, "Performance"),
        ("❤️", satisfaction, "Satisfaction"),
    ])

    # =====================
    # TABLE
    # =====================

    section_header( "Étape 3", "Aperçu des données", "Les premières lignes du dataset généré.")

    st.dataframe(
        df,
        use_container_width=True
    )

    # =====================
    # EXPORTS
    # =====================

    section_header( "Étape 4", "Export", "Télécharge le dataset dans le format de ton choix.")

    csv = df.to_csv(index=False).encode()

    excel_path = ROOT / "data" / "freelancers.xlsx"
    json_path = ROOT / "data" / "freelancers.json"

    col1, col2, col3 = st.columns(3)

    col1.download_button(
        "CSV",
        csv,
        "freelancers.csv",
        "text/csv"
    )

    with open(excel_path, "rb") as f:
        col2.download_button(
            "Excel",
            f,
            "freelancers.xlsx"
        )

    with open(json_path) as f:
        col3.download_button(
            "JSON",
            f.read(),
            "freelancers.json"
        )

    # =====================
    # GRAPHIQUES
    # =====================

    section_header( "Étape 5", "Visualisations", "Distribution, valeurs atypiques et répartition métiers.")

    fig1 = px.histogram(df, x="performance_score", nbins=30, title="Distribution des performances")
    fig2 = px.box(df, y="performance_score", title="Détection des valeurs atypiques")
    fig3 = px.pie(df, names="category", title="Répartition des métiers")
    fig4 = px.histogram(df, x="activity_score", title="Distribution de l'activité")

    st.plotly_chart(style_chart(fig1), use_container_width=True)
    st.plotly_chart(style_chart(fig2), use_container_width=True)
    st.plotly_chart(style_chart(fig3), use_container_width=True)
    st.plotly_chart(style_chart(fig4), use_container_width=True)

    # =====================
    # DOCUMENTATION
    # =====================

    section_header( "Annexe", "Documentation scientifique", "Méthodologie et propriétés du générateur.")

    st.markdown("""

### Algorithme de génération de la seed

1. Suppression des accents.
2. Suppression des espaces.
3. Conversion en majuscules.
4. Calcul :

seed = Σ(position × ASCII²)

5. Réduction modulo 1 000 000.

---

### Variables générées

| Variable | Description |
|---|---|
| performance_score | Performance globale du freelance |
| activity_score | Niveau d'activité |
| hourly_rate | Tarif horaire |
| client_satisfaction | Satisfaction client |
| response_time | Temps de réponse |
| profile_type | Premium / Standard |

---

### Justification de l'échantillon

1200 observations ont été retenues :

- statistiques descriptives robustes ;
- corrélations fiables ;
- clustering pertinent ;
- classification supervisée stable.

---

### Propriété fondamentale

Le générateur est :

- déterministe
- reproductible
- conforme à l'annexe du TP
- dépendant uniquement du nom du chef de groupe

""")