"""
Petits helpers d'habillage partagés entre les pages Streamlit.

Contrairement à la version précédente, ce module est autonome :
- pas de fichier style.css externe à charger (donc pas de chemin cassé) ;
- pas de script de détection de thème (theme_sync.py) ;
- le style s'appuie directement sur les variables CSS que Streamlit
  gère lui-même en natif (--background-color, --text-color...), qui se
  mettent à jour automatiquement quand l'utilisateur bascule clair/sombre.
- on ne touche à AUCUN élément natif de Streamlit (sidebar, boutons,
  widgets...) : seules nos propres classes (hero-card, kpi-card,
  section-card, module-pill) sont stylées, donc aucun risque d'interférer
  avec le DOM de Streamlit.

Chaque page doit appeler apply_base_style() une fois, avant d'utiliser
hero_card() / section_header() / kpi_row().
"""

import streamlit as st


_BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=JetBrains+Mono:wght@500&display=swap');

:root {
    --inf232-accent-a: #14b8a6;  /* teal */
    --inf232-accent-b: #8b7cf6;  /* violet */
    --inf232-r-lg: 26px;
    --inf232-r-md: 18px;
    --inf232-r-sm: 12px;
}

/* -------------------------------------------------------------
   HERO
------------------------------------------------------------- */
.hero-card {
    position: relative;
    background: color-mix(in srgb, var(--text-color) 5%, var(--background-color));
    border: 1px solid color-mix(in srgb, var(--text-color) 12%, transparent);
    border-radius: var(--inf232-r-lg);
    padding: 38px 42px;
    margin-bottom: 30px;
    box-shadow: 0 16px 40px color-mix(in srgb, var(--text-color) 10%, transparent);
    overflow: hidden;
}
.hero-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--inf232-accent-a), var(--inf232-accent-b), var(--inf232-accent-a));
    background-size: 200% 100%;
    animation: inf232-shimmer 6s linear infinite;
}
@keyframes inf232-shimmer {
    0% { background-position: 0% 0%; }
    100% { background-position: 200% 0%; }
}
@media (prefers-reduced-motion: reduce) {
    .hero-card::before { animation: none; }
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: "JetBrains Mono", monospace;
    font-size: 12px;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: var(--inf232-accent-a);
    background: color-mix(in srgb, var(--inf232-accent-a) 14%, transparent);
    border: 1px solid color-mix(in srgb, var(--inf232-accent-a) 30%, transparent);
    padding: 6px 12px;
    border-radius: 999px;
    margin-bottom: 16px;
}
.hero-title {
    font-family: "Sora", sans-serif;
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -.02em;
    line-height: 1.15;
    color: var(--text-color);
}
.hero-subtitle {
    color: color-mix(in srgb, var(--text-color) 78%, var(--background-color));
    font-size: 16px;
    margin-top: 12px;
    line-height: 1.6;
    max-width: 700px;
}

/* -------------------------------------------------------------
   KPI
------------------------------------------------------------- */
.kpi-card {
    background: color-mix(in srgb, var(--text-color) 5%, var(--background-color));
    border: 1px solid color-mix(in srgb, var(--text-color) 12%, transparent);
    border-radius: var(--inf232-r-md);
    padding: 20px 16px;
    text-align: center;
    transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
}
.kpi-card:hover {
    transform: translateY(-4px);
    border-color: color-mix(in srgb, var(--inf232-accent-a) 40%, transparent);
    box-shadow: 0 14px 30px color-mix(in srgb, var(--inf232-accent-a) 16%, transparent);
}
.kpi-icon { font-size: 20px; opacity: .9; margin-bottom: 6px; }
.kpi-value {
    font-family: "Sora", sans-serif;
    font-size: 27px;
    font-weight: 800;
    background: linear-gradient(90deg, var(--inf232-accent-a), var(--inf232-accent-b));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.kpi-label {
    color: color-mix(in srgb, var(--text-color) 62%, var(--background-color));
    font-size: 12px;
    letter-spacing: .04em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* -------------------------------------------------------------
   SECTIONS
------------------------------------------------------------- */
.section-card {
    background: color-mix(in srgb, var(--text-color) 4%, var(--background-color));
    border: 1px solid color-mix(in srgb, var(--text-color) 10%, transparent);
    border-left: 3px solid var(--inf232-accent-a);
    border-radius: var(--inf232-r-md);
    padding: 20px 24px;
    margin: 26px 0 16px 0;
}
.section-eyebrow {
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: var(--inf232-accent-b);
    margin-bottom: 6px;
}
.section-title {
    font-family: "Sora", sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--text-color);
}
.section-desc {
    color: color-mix(in srgb, var(--text-color) 60%, var(--background-color));
    font-size: 13.5px;
    margin-top: 6px;
}

/* -------------------------------------------------------------
   MODULES (page d'accueil)
------------------------------------------------------------- */
.module-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
    margin-top: 18px;
}
.module-pill {
    display: flex;
    align-items: center;
    gap: 10px;
    background: color-mix(in srgb, var(--text-color) 4%, var(--background-color));
    border: 1px solid color-mix(in srgb, var(--text-color) 10%, transparent);
    border-radius: var(--inf232-r-sm);
    padding: 14px 16px;
    font-size: 14.5px;
    color: color-mix(in srgb, var(--text-color) 80%, var(--background-color));
    transition: border-color .2s ease, transform .2s ease;
}
.module-pill.live {
    border-color: color-mix(in srgb, #22c55e 40%, transparent);
    color: var(--text-color);
}
.module-pill:hover { transform: translateX(3px); }
.module-status {
    margin-left: auto;
    font-family: "JetBrains Mono", monospace;
    font-size: 10.5px;
    letter-spacing: .08em;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 999px;
}
.module-status.on { background: rgba(34,197,94,.16); color: #16a34a; }
.module-status.soon { background: rgba(245,158,11,.16); color: #b45309; }
</style>
"""


def apply_base_style():
    """À appeler une fois en haut de chaque page, avant hero_card/section_header/kpi_row."""
    st.markdown(_BASE_CSS, unsafe_allow_html=True)


def hero_card(eyebrow: str, title: str, subtitle_html: str):
    st.markdown(
        f'<div class="hero-card">'
        f'<div class="hero-eyebrow">{eyebrow}</div>'
        f'<div class="hero-title">{title}</div>'
        f'<div class="hero-subtitle">{subtitle_html}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def section_header(icon: str, eyebrow: str, title: str, desc: str = ""):
    desc_html = f'<div class="section-desc">{desc}</div>' if desc else ""
    st.markdown(
        f'<div class="section-card">'
        f'<div class="section-eyebrow">{icon} {eyebrow}</div>'
        f'<div class="section-title">{title}</div>'
        f'{desc_html}'
        f'</div>',
        unsafe_allow_html=True
    )


def kpi_row(items):
    """
    items: liste de tuples.
    Formats acceptés :
      - (icon, value, label)  → recommandé
      - (label, value)        → un icône neutre "•" est utilisé
    """
    cols = st.columns(len(items))
    for c, item in zip(cols, items):
        if len(item) == 3:
            icon, value, label = item
        elif len(item) == 2:
            label, value = item
            icon = "•"
        else:
            raise ValueError(
                f"kpi_row: tuple invalide {item!r} — attendu (icon, value, label) ou (label, value)"
            )
        c.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-icon">{icon}</div>'
            f'<div class="kpi-value">{value}</div>'
            f'<div class="kpi-label">{label}</div>'
            f'</div>',
            unsafe_allow_html=True
        )


def chart_theme_colors():
    """
    Renvoie (font_color, title_color, grid_color) adaptés au thème actif.
    st.context.theme n'existe que sur les versions récentes de Streamlit :
    on retombe sur des couleurs neutres (lisibles dans les deux thèmes)
    si l'API est indisponible.
    """
    try:
        is_light = st.context.theme.type == "light"
    except Exception:
        is_light = False

    if is_light:
        return "#3b4a63", "#0f1e33", "rgba(15,35,65,0.10)"
    return "#c3d0e0", "#f4f7fb", "rgba(255,255,255,0.12)"


def style_chart(fig):
    """Applique un habillage transparent + couleurs adaptées au thème."""
    font_color, title_color, grid_color = chart_theme_colors()
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=font_color,
        title_font_color=title_color,
        margin=dict(t=50, b=20, l=10, r=10),
    )
    fig.update_xaxes(gridcolor=grid_color, zerolinecolor=grid_color)
    fig.update_yaxes(gridcolor=grid_color, zerolinecolor=grid_color)
    return fig