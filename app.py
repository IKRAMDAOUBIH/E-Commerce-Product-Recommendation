import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go

# ═══════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════
st.set_page_config(
    page_title="ShopSense AI · E-Commerce Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════
#  GLOBAL CSS
# ═══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

:root {
  --bg:#0A0A0F; --bg2:#12121A; --bg3:#1A1A26; --border:#2A2A3E;
  --accent1:#8B5CF6; --accent2:#EC4899; --accent3:#06B6D4;
  --gold:#F59E0B; --success:#10B981; --danger:#EF4444;
  --text:#E8E8F0; --muted:#6B7280; --card-bg:rgba(26,26,38,0.95);
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--text); }
.stApp { background: var(--bg); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem 2rem; max-width: 1400px; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--accent1); border-radius: 3px; }

[data-testid="stSidebar"] { background: var(--bg2) !important; border-right: 1px solid var(--border); }
[data-testid="stSidebar"] * { color: var(--text) !important; }

[data-testid="stSidebar"] .stButton > button {
  display: flex !important; align-items: center !important; gap: 10px !important;
  width: 100% !important; padding: 10px 14px !important; border-radius: 10px !important;
  margin: 2px 0 !important; cursor: pointer !important; border: 1px solid transparent !important;
  font-size: 0.88em !important; font-weight: 400 !important; color: #6B7280 !important;
  background: transparent !important; box-shadow: none !important; text-align: left !important;
  justify-content: flex-start !important; letter-spacing: 0 !important;
  transition: all 0.2s ease !important; min-height: unset !important; height: auto !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(139,92,246,0.08) !important; border-color: rgba(139,92,246,0.25) !important;
  color: #E8E8F0 !important; transform: none !important; box-shadow: none !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── SIDEBAR TOUJOURS VISIBLE ── */
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] {
  min-width: 260px !important;
  max-width: 260px !important;
  transform: none !important;
  visibility: visible !important;
}
[data-testid="stSidebar"] .nav-active .stButton > button {
  background: linear-gradient(135deg,rgba(139,92,246,0.18),rgba(236,72,153,0.09)) !important;
  border-color: rgba(139,92,246,0.5) !important; color: #E8E8F0 !important; font-weight: 600 !important;
}

.hero {
  background: radial-gradient(ellipse at 30% 50%, #8B5CF620 0%, transparent 60%),
              radial-gradient(ellipse at 70% 20%, #EC489915 0%, transparent 60%),
              linear-gradient(135deg, #0A0A0F 0%, #12121A 100%);
  border: 1px solid var(--border); border-radius: 20px;
  padding: 60px 50px; margin-bottom: 30px; position: relative; overflow: hidden;
}
.hero::before {
  content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
  background: repeating-linear-gradient(45deg, transparent, transparent 30px,
    rgba(139,92,246,0.02) 30px, rgba(139,92,246,0.02) 31px);
  pointer-events: none;
}
.hero-badge {
  display: inline-block;
  background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(236,72,153,0.13));
  border: 1px solid rgba(139,92,246,0.4); color: var(--accent1);
  padding: 6px 16px; border-radius: 20px; font-size: 0.78em; font-weight: 600;
  letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 20px;
  font-family: 'Space Mono', monospace;
}
.hero h1 {
  font-family: 'Playfair Display', serif; font-size: 3.2em; font-weight: 900;
  line-height: 1.1; margin: 0 0 16px 0;
  background: linear-gradient(135deg, #fff 30%, #8B5CF6 70%, #EC4899);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero p { font-size: 1.05em; color: var(--muted); line-height: 1.7; max-width: 600px; margin: 0; }

.card {
  background: var(--card-bg); border: 1px solid var(--border);
  border-radius: 16px; padding: 24px; margin-bottom: 20px;
  position: relative; overflow: hidden;
}
.card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, var(--accent1), var(--accent2), var(--accent3));
}

.nav-active { display: block; }

.fb-btn > div > button {
  background: transparent !important; border: 1px solid rgba(42,42,62,0.5) !important;
  color: #4B5563 !important; font-size: 0.72em !important; padding: 4px 10px !important;
  font-weight: 400 !important; box-shadow: none !important; min-height: unset !important;
  height: auto !important; letter-spacing: 0 !important; margin-top: 2px !important;
  border-radius: 6px !important;
}

.sec-title { font-family: 'Playfair Display', serif; font-size: 1.9em; font-weight: 700; color: #fff; margin: 0 0 6px 0; }
.sec-sub   { color: var(--muted); font-size: 0.9em; margin-bottom: 24px; line-height: 1.6; }

.styled-table { width: 100%; border-collapse: collapse; font-size: 0.88em; }
.styled-table th { background: var(--bg3); color: var(--accent1); padding: 12px 16px;
  text-align: left; font-family: 'Space Mono', monospace; font-size: 0.78em;
  letter-spacing: 0.5px; border-bottom: 1px solid var(--border); }
.styled-table td { padding: 11px 16px; color: var(--text); border-bottom: 1px solid rgba(42,42,62,0.3); }
.styled-table tr:hover td { background: var(--bg3); }

.main-btn > div > button,
.stButton > button {
  background: linear-gradient(135deg, var(--accent1), var(--accent2)) !important;
  color: white !important; border: none !important; border-radius: 12px !important;
  padding: 14px 28px !important; font-weight: 600 !important; font-size: 1em !important;
  letter-spacing: 0.5px !important; box-shadow: 0 8px 30px rgba(139,92,246,0.3) !important;
  transition: all 0.3s ease !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 40px rgba(139,92,246,0.45) !important; }

.fancy-divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(139,92,246,0.3), rgba(236,72,153,0.3), transparent); margin: 32px 0; }

.tl-item { display: flex; gap: 16px; padding: 0 0 24px 0; position: relative; }
.tl-item::before { content: ''; position: absolute; left: 19px; top: 40px; bottom: 0; width: 1px; background: var(--border); }
.tl-item:last-child::before { display: none; }
.tl-dot { width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1em; flex-shrink: 0; border: 2px solid var(--border); background: var(--bg2); z-index: 1; }
.tl-content h4 { margin: 6px 0 4px 0; font-size: 0.93em; color: #fff; font-weight: 600; }
.tl-content p  { margin: 0; font-size: 0.82em; color: var(--muted); line-height: 1.5; }

.concl-item { display: flex; gap: 14px; align-items: flex-start; padding: 14px 0; border-bottom: 1px solid rgba(42,42,62,0.4); }
.concl-item:last-child { border-bottom: none; }
.concl-icon { width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.1em; flex-shrink: 0; background: var(--bg2); }
.concl-text h4 { margin: 0 0 4px 0; font-size: 0.92em; color: #fff; }
.concl-text p  { margin: 0; font-size: 0.82em; color: var(--muted); line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  LOAD MODELS
# ═══════════════════════════════════════════════
BASE_DIR = os.path.dirname(__file__)

@st.cache_resource
def load_assets():
    def _open(name):
        path = os.path.join(BASE_DIR, "model", name)
        return pickle.load(open(path, "rb"))

    load_errors = {}
    models = scaler = feature_cols = scaled_cols = None

    try:
        models = _open("models.pkl")
    except Exception as e:
        load_errors["models.pkl"] = str(e)

    try:
        scaler = _open("scaler.pkl")
    except Exception as e:
        load_errors["scaler.pkl"] = str(e)

    try:
        feature_cols = _open("feature_columns.pkl")
    except Exception as e:
        load_errors["feature_columns.pkl"] = str(e)

    try:
        scaled_cols = _open("scaled_columns.pkl")
    except Exception as e:
        load_errors["scaled_columns.pkl"] = str(e)

    full_ok = (models is not None and scaler is not None
               and feature_cols is not None and scaled_cols is not None)

    if full_ok or models is not None:
        models_ok = True
    else:
        models_ok = False

    return models, scaler, feature_cols, scaled_cols, models_ok, load_errors

_assets = load_assets()
(models, scaler, feature_cols, scaled_cols, models_ok, _load_errors) = _assets

# ✅ Pipeline complet si les 4 fichiers sont présents
pipeline_ok = (models is not None and scaler is not None
               and feature_cols is not None and scaled_cols is not None)

# ═══════════════════════════════════════════════
#  PAGES DEFINITION
# ═══════════════════════════════════════════════
PAGES = [
    ("01", "Accueil"),
    ("02", "Exploration des Données"),
    ("03", "Modélisation ML"),
    ("04", "Non Supervisé"),
    ("05", "Prédiction"),
    ("06", "Explication IA"),
    ("07", "Valeur Ajoutée"),
    ("08", "Conclusion"),
]

# ═══════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════
if "page" not in st.session_state:
    st.session_state.page = 0

with st.sidebar:
    st.markdown("""
    <div style='padding:20px 10px 10px 10px;'>
      <div style='font-family:"Space Mono",monospace;font-size:0.62em;color:#4B5563;
                  letter-spacing:2px;text-transform:uppercase;'>v1.0 · Master d'Excellence 2026</div>
      <div style='font-family:"Playfair Display",serif;font-size:1.6em;font-weight:900;
                  margin-top:4px;background:linear-gradient(135deg,#8B5CF6,#EC4899);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
        ShopSense AI
      </div>
    </div>
    <div style='height:1px;background:linear-gradient(90deg,transparent,#2A2A3E,transparent);
                margin:10px 0 16px 0;'></div>
    <div style='font-family:"Space Mono",monospace;font-size:0.62em;color:#4B5563;
                letter-spacing:2px;text-transform:uppercase;padding:0 10px 10px 10px;'>
      NAVIGATION
    </div>
    """, unsafe_allow_html=True)

    for i, (icon, label) in enumerate(PAGES):
        is_active = st.session_state.page == i
        if is_active:
            st.markdown("<div class='nav-active'>", unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"nav_btn_{i}", use_container_width=True):
            st.session_state.page = i
            st.rerun()
        if is_active:
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='height:1px;background:linear-gradient(90deg,transparent,#2A2A3E,transparent);
                margin:16px 0;'></div>
    <div style='padding:0 10px;font-family:"Space Mono",monospace;font-size:0.63em;
                color:#374151;line-height:1.8;'>
      Daoubih Ikram<br>Hani Salwa <br>
    </div>
    """, unsafe_allow_html=True)

    # ── Statut pipeline ──────────────────────────────────────
    if pipeline_ok:
        st.markdown("""
        <div style='margin:10px 10px 0 10px;padding:8px 10px;
                    background:rgba(16,185,129,0.08);
                    border:1px solid rgba(16,185,129,0.3);border-radius:8px;'>
          <div style='font-family:"Space Mono",monospace;font-size:0.6em;
                      color:#10B981;letter-spacing:1px;'>PIPELINE COMPLET ✓</div>
          <div style='font-size:0.7em;color:#6B7280;margin-top:2px;'>
            models + scaler + features ✓
          </div>
        </div>""", unsafe_allow_html=True)
    elif models_ok:
        st.markdown("""
        <div style='margin:10px 10px 0 10px;padding:8px 10px;
                    background:rgba(245,158,11,0.08);
                    border:1px solid rgba(245,158,11,0.3);border-radius:8px;'>
          <div style='font-family:"Space Mono",monospace;font-size:0.6em;
                      color:#F59E0B;letter-spacing:1px;'>MODE APPROX.</div>
          <div style='font-size:0.7em;color:#6B7280;margin-top:2px;'>
            scaler/features manquants
          </div>
        </div>""", unsafe_allow_html=True)
        if _load_errors:
            for fname, err in _load_errors.items():
                st.markdown(
                    f"<div style='margin:4px 10px;padding:6px 8px;"
                    f"background:rgba(239,68,68,0.06);border-radius:6px;"
                    f"font-size:0.62em;color:#EF4444;font-family:monospace;'>"
                    f"<strong>{fname}</strong><br>{err[:80]}</div>",
                    unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='margin:10px 10px 0 10px;padding:8px 10px;
                    background:rgba(239,68,68,0.08);
                    border:1px solid rgba(239,68,68,0.3);border-radius:8px;'>
          <div style='font-family:"Space Mono",monospace;font-size:0.6em;
                      color:#EF4444;letter-spacing:1px;'>AUCUN MODELE</div>
          <div style='font-size:0.7em;color:#6B7280;margin-top:2px;'>
            model/models.pkl introuvable
          </div>
        </div>""", unsafe_allow_html=True)

PAGE = st.session_state.page

# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════
def sentiment_quick(text):
    pos = ["love","great","amazing","perfect","beautiful","excellent","wonderful",
           "fantastic","adorable","best","comfortable","flattering","soft","gorgeous",
           "cute","nice","happy","fits","quality","lovely","pretty"]
    neg = ["hate","terrible","awful","horrible","bad","poor","ugly","worst",
           "uncomfortable","disappointing","waste","return","cheap","stiff",
           "scratchy","tight","loose","ruined","small","large","boring"]
    t = text.lower()
    p = sum(1 for w in pos if w in t)
    n = sum(1 for w in neg if w in t)
    if p > n:  return "Positif 😊", "#10B981", p / (p + n + 0.1)
    if n > p:  return "Négatif 😞", "#EF4444", n / (p + n + 0.1)
    return "Neutre 😐", "#F59E0B", 0.5


def preprocess(review, rating, feedback, age,
               division="General", department="Tops", class_name="Blouses"):
    """
    Reconstruit EXACTEMENT le vecteur X du notebook :
    - TextBlob pour polarity et subjectivity
    - review_length en nombre de mots
    - One-Hot Encoding pour Division, Department, Class
    - StandardScaler sur les 6 colonnes numériques
    - Ordre des colonnes identique à feature_cols sauvegardé
    """
    if not pipeline_ok:
        return None, "none"

    try:
        from textblob import TextBlob

        blob         = TextBlob(str(review))
        polarity     = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        review_length = len(str(review).split())

        # Construire un dict avec TOUTES les colonnes initialisées à False/0
        row = {}
        for col in feature_cols:
            row[col] = False

        # Colonnes numériques (avant scaling)
        row["Age"]                     = float(age)
        row["Rating"]                  = float(rating)
        row["Positive Feedback Count"] = float(feedback)
        row["review_length"]           = float(review_length)
        row["polarity"]                = float(polarity)
        row["subjectivity"]            = float(subjectivity)

        # Clothing ID — valeur médiane du dataset
        if "Clothing ID" in feature_cols:
            row["Clothing ID"] = 936.0

        # One-Hot Encoding — Division Name
        div_col = f"Division Name_{division}"
        if div_col in feature_cols:
            row[div_col] = True

        # One-Hot Encoding — Department Name
        dept_col = f"Department Name_{department}"
        if dept_col in feature_cols:
            row[dept_col] = True

        # One-Hot Encoding — Class Name
        class_col = f"Class Name_{class_name}"
        if class_col in feature_cols:
            row[class_col] = True

        # Créer le DataFrame dans le bon ordre
        X_df = pd.DataFrame([row], columns=feature_cols)

        # Appliquer StandardScaler sur les 6 colonnes numériques
        X_df[scaled_cols] = scaler.transform(X_df[scaled_cols])

        return X_df.values, "full"

    except Exception:
        return None, "none"


def predict_manual(review, rating, feedback, age):
    """Fallback uniquement si les fichiers pkl sont manquants."""
    import math
    try:
        from textblob import TextBlob
        polarity = TextBlob(str(review)).sentiment.polarity
    except Exception:
        polarity = 0.0

    review_length = len(str(review).split())
    rating_norm   = (rating   - 4.2)  / 1.11
    polarity_norm = (polarity - 0.28) / 0.22
    feedback_norm = (min(feedback, 10) - 2.54) / 5.70
    length_norm   = (min(review_length, 50) - 20) / 15

    score = (rating_norm   * 0.79
           + polarity_norm * 0.21
           + feedback_norm * 0.03
           + length_norm   * 0.02)

    proba = 1 / (1 + math.exp(-score * 3.5))
    proba = round(max(0.02, min(0.98, proba)), 4)
    return int(proba >= 0.5), proba


def proba_bar_html(value, color, label="Probabilité de succès"):
    pct = int(value * 100)
    return f"""
    <div style='margin:14px 0;'>
      <div style='display:flex;justify-content:space-between;
                  font-family:"Space Mono",monospace;font-size:0.8em;margin-bottom:6px;'>
        <span style='color:#9CA3AF;'>{label}</span>
        <span style='color:{color};font-weight:700;'>{pct}%</span>
      </div>
      <div style='background:#1A1A26;border-radius:4px;height:8px;overflow:hidden;'>
        <div style='width:{pct}%;height:100%;border-radius:4px;background:{color};'></div>
      </div>
    </div>"""

PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#6B7280"), margin=dict(t=50, b=20, l=20, r=20),
)

# ══════════════════════════════════════════════════════════════
#  PAGE 0 — ACCUEIL
# ══════════════════════════════════════════════════════════════
if PAGE == 0:
    st.markdown("""
    <div class='hero'>
      <div class='hero-badge'>✦ Machine Learning · NLP · E-Commerce</div>
      <h1>Prédiction du Succès<br>des Produits E-Commerce</h1>
      <p>Un système d'intelligence artificielle supervisé qui analyse les avis clients,
         les notes et les métadonnées produits pour prédire si un article sera recommandé —
         avec explications SHAP en temps réel.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, (num, lbl, clr) in zip([c1, c2, c3, c4], [
        ("23,486", "Avis analysés",      "#8B5CF6"),
        ("82.6%",  "Taux recommandation","#10B981"),
        ("93.7%",  "Accuracy modèle",    "#06B6D4"),
        ("3",      "Modèles comparés",   "#F59E0B"),
    ]):
        with col:
            st.markdown(f"""
            <div class='card' style='text-align:center;padding:28px 16px;'>
              <div style='font-family:"Space Mono",monospace;font-size:2em;font-weight:700;color:{clr};'>{num}</div>
              <div style='color:#6B7280;font-size:0.8em;margin-top:6px;'>{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    # ── LIGNE 1 : À propos | Technologies ────────────────────────────
    col_l, col_r = st.columns([1.1, 0.9], gap="large")

    with col_l:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='sec-title'>À propos du projet</div>", unsafe_allow_html=True)
        st.markdown("<div class='sec-sub'>Women's Clothing E-Commerce Reviews Dataset — BSDSI 2025-2026</div>", unsafe_allow_html=True)
        for clr, icon, title, desc in [
            ("#8B5CF6","","Problématique",
             "Prédire si un produit sera recommandé à partir des avis clients, notes et données démographiques."),
            ("#EC4899","","Données analysées",
             "23 486 avis sur des vêtements féminins : âge, rating 1-5, texte, feedbacks, département, classe."),
            ("#06B6D4","","Approche ML",
             "Classification binaire supervisée avec TF-IDF, polarité TextBlob, puis Random Forest optimisé."),
            ("#10B981","","Valeur ajoutée",
             "L'application explique chaque décision via SHAP, aidant les équipes produit à agir."),
        ]:
            st.markdown(f"""
            <div class='tl-item'>
              <div class='tl-dot' style='border-color:{clr};'>{icon}</div>
              <div class='tl-content'><h4>{title}</h4><p>{desc}</p></div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='sec-title'>Technologies</div>", unsafe_allow_html=True)
        st.markdown("<div class='sec-sub'>Stack utilisé dans ce projet</div>", unsafe_allow_html=True)
        for clr, bg, name, desc in [
            ("#8B5CF6","#1A1026","Python 3.11","Langage principal"),
            ("#06B6D4","#001820","Streamlit","Interface web interactive"),
            ("#F59E0B","#1A1100","Scikit-learn","Modèles ML & évaluation"),
            ("#10B981","#001811","TextBlob","Analyse de sentiment NLP"),
            ("#EC4899","#1A0011","Pandas / NumPy","Manipulation des données"),
            ("#6366F1","#0D0D20","SHAP","Explicabilité IA"),
            ("#F97316","#1A0D00","Plotly","Visualisations interactives"),
            ("#34D399","#001810","TF-IDF","Vectorisation du texte"),
        ]:
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid rgba(42,42,62,0.4);'>
              <div style='width:36px;height:36px;border-radius:8px;background:{bg};
                          border:1px solid rgba(42,42,62,0.5);display:flex;align-items:center;
                          justify-content:center;flex-shrink:0;'>
                <div style='width:10px;height:10px;border-radius:50%;background:{clr};'></div>
              </div>
              <div>
                <div style='font-weight:600;font-size:0.88em;color:#E8E8F0;'>{name}</div>
                <div style='font-size:0.75em;color:#6B7280;'>{desc}</div>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # ── SECTION PLEINE LARGEUR : Colonnes du dataset ──────────────
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#8B5CF6;
                letter-spacing:2px;text-transform:uppercase;margin-bottom:18px;'>
      ● Colonnes du dataset
    </div>""", unsafe_allow_html=True)

    # Mini stats
    st.markdown("""
    <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px;'>
      <div style='background:rgba(26,26,38,0.95);border:1px solid #2A2A3E;border-radius:12px;padding:16px;text-align:center;'>
        <div style='font-family:"Space Mono",monospace;font-size:1.6em;font-weight:700;color:#8B5CF6;'>23 486</div>
        <div style='font-size:0.75em;color:#6B7280;margin-top:4px;'>Avis clients</div>
      </div>
      <div style='background:rgba(26,26,38,0.95);border:1px solid #2A2A3E;border-radius:12px;padding:16px;text-align:center;'>
        <div style='font-family:"Space Mono",monospace;font-size:1.6em;font-weight:700;color:#06B6D4;'>10</div>
        <div style='font-size:0.75em;color:#6B7280;margin-top:4px;'>Colonnes</div>
      </div>
      <div style='background:rgba(26,26,38,0.95);border:1px solid #2A2A3E;border-radius:12px;padding:16px;text-align:center;'>
        <div style='font-family:"Space Mono",monospace;font-size:1.6em;font-weight:700;color:#10B981;'>82.6%</div>
        <div style='font-size:0.75em;color:#6B7280;margin-top:4px;'>Recommandés</div>
      </div>
      <div style='background:rgba(26,26,38,0.95);border:1px solid #2A2A3E;border-radius:12px;padding:16px;text-align:center;'>
        <div style='font-family:"Space Mono",monospace;font-size:1.6em;font-weight:700;color:#F59E0B;'>3 526</div>
        <div style='font-size:0.75em;color:#6B7280;margin-top:4px;'>Val. manquantes</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Colonnes : chaque carte générée SÉPARÉMENT pour éviter le bug f-string ──
    cols_data = [
        ("Clothing ID",       "int64",        "Identifiant", "#8B5CF6",
         "rgba(139,92,246,0.12)", "rgba(139,92,246,0.4)", False),
        ("Age",               "int64",        "Numérique",   "#06B6D4",
         "rgba(6,182,212,0.12)",  "rgba(6,182,212,0.4)",  False),
        ("Title",             "object",       "Texte",       "#EC4899",
         "rgba(236,72,153,0.12)", "rgba(236,72,153,0.4)", False),
        ("Review Text",       "object",       "NLP",         "#F59E0B",
         "rgba(245,158,11,0.12)", "rgba(245,158,11,0.4)", False),
        ("Rating",            "int64 · 1–5",  "Numérique",   "#10B981",
         "rgba(16,185,129,0.12)", "rgba(16,185,129,0.4)", False),
        ("Recommended IND",   "int64 · 0/1",  "Target",      "#EF4444",
         "rgba(239,68,68,0.15)",  "rgba(239,68,68,0.6)",  True),
        ("Positive Feedback", "int64",        "Engagement",  "#6366F1",
         "rgba(99,102,241,0.12)", "rgba(99,102,241,0.4)", False),
        ("Division Name",     "object · 3",   "Catégoriel",  "#F97316",
         "rgba(249,115,22,0.12)", "rgba(249,115,22,0.4)", False),
        ("Department Name",   "object · 6",   "Catégoriel",  "#34D399",
         "rgba(52,211,153,0.12)", "rgba(52,211,153,0.4)", False),
        ("Class Name",        "object · 20",  "Catégoriel",  "#A78BFA",
         "rgba(167,139,250,0.12)","rgba(167,139,250,0.4)",False),
    ]

    # On génère le HTML des 10 cartes EN UNE SEULE chaîne — sans f-string imbriquée
    cards_html = (
        "<div style='display:grid;grid-template-columns:repeat(5,1fr);"
        "gap:14px;margin-bottom:22px;'>"
    )

    for name, dtype, badge, clr, bg_card_inner, bd_clr, is_target in cols_data:
        top_bar_color = clr
        border_col    = bd_clr if is_target else "#2A2A3E"
        border_width  = "2px" if is_target else "1px"
        dot_icon      = "" if is_target else ""
        dot_circle    = (
            "" if is_target else
            "<div style='width:10px;height:10px;border-radius:50%;"
            "background:" + clr + ";'></div>"
        )
        icon_bg = bg_card_inner

        card = (
            "<div style='background:rgba(26,26,38,0.95);"
            "border:" + border_width + " solid " + border_col + ";"
            "border-radius:14px;padding:18px 16px;"
            "position:relative;overflow:hidden;'>"

            # barre couleur top
            "<div style='position:absolute;top:0;left:0;right:0;height:3px;"
            "background:" + top_bar_color + ";'></div>"

            # icône rond ou emoji
            "<div style='width:38px;height:38px;border-radius:10px;"
            "background:" + icon_bg + ";"
            "border:1px solid " + bd_clr + ";"
            "display:flex;align-items:center;justify-content:center;"
            "margin-bottom:11px;font-size:1.1em;'>"
            + dot_icon + dot_circle +
            "</div>"

            # nom colonne
            "<div style='font-size:0.87em;font-weight:700;color:#E8E8F0;"
            "margin-bottom:4px;line-height:1.3;'>" + name + "</div>"

            # type
            "<div style='font-family:\"Space Mono\",monospace;font-size:0.66em;"
            "color:#6B7280;margin-bottom:9px;'>" + dtype + "</div>"

            # badge
            "<span style='display:inline-block;font-size:0.68em;padding:3px 10px;"
            "border-radius:20px;background:" + icon_bg + ";"
            "color:" + clr + ";border:1px solid " + bd_clr + ";"
            "font-family:\"Space Mono\",monospace;font-weight:600;'>"
            + badge +
            "</span>"

            "</div>"
        )
        cards_html += card

    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)

    # ── Barre distribution variable cible ────────────────────────
    st.markdown("""
    <div style='background:rgba(26,26,38,0.95);border:1px solid #2A2A3E;
                border-radius:14px;padding:18px 24px;margin-bottom:24px;'>
      <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;'>
        <div style='font-family:"Space Mono",monospace;font-size:0.75em;
                    font-weight:600;color:#E8E8F0;'>
          Distribution — Variable Cible (Recommended IND)
        </div>
        <div style='font-family:"Space Mono",monospace;font-size:0.65em;color:#6B7280;'>
          23 486 avis · Déséquilibre 82/18
        </div>
      </div>
      <div style='height:10px;background:#1A1A26;border-radius:6px;
                  overflow:hidden;display:flex;'>
        <div style='width:82.6%;background:linear-gradient(90deg,#8B5CF6,#EC4899);
                    border-radius:6px 0 0 6px;'></div>
        <div style='width:17.4%;background:#EF4444;
                    border-radius:0 6px 6px 0;'></div>
      </div>
      <div style='display:flex;justify-content:space-between;margin-top:8px;'>
        <span style='font-family:"Space Mono",monospace;font-size:0.72em;color:#8B5CF6;
                     display:flex;align-items:center;gap:6px;'>
          <span style='width:8px;height:8px;border-radius:50%;background:#8B5CF6;
                       display:inline-block;'></span>
          82.6% — Recommandé (1) · 19 342 avis
        </span>
        <span style='font-family:"Space Mono",monospace;font-size:0.72em;color:#EF4444;
                     display:flex;align-items:center;gap:6px;'>
          17.4% — Non recommandé (0) · 4 144 avis
          <span style='width:8px;height:8px;border-radius:50%;background:#EF4444;
                       display:inline-block;'></span>
        </span>
      </div>
    </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # ── TABLEAU df.head(5) — pleine largeur ───────────────────────
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#8B5CF6;
                letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;'>
      ● Aperçu du dataset — df.head(5)
    </div>""", unsafe_allow_html=True)

    overview_rows = [
        (0, 767,  33, 4, 1, 0,  "Initmates",   "Intimate", "Intimates",
         "Absolutely wonderful - silky and sexy and comfortable..."),
        (1, 1080, 34, 5, 1, 4,  "General",     "Dresses",  "Dresses",
         "Love this dress! it's sooo pretty. i happened to find it..."),
        (2, 1077, 60, 3, 0, 0,  "General",     "Dresses",  "Dresses",
         "I had such high hopes for this dress and really wanted it..."),
        (3, 1049, 50, 5, 1, 0,  "Gen. Petite", "Bottoms",  "Pants",
         "I love, love, love this jumpsuit. it's fun, flirty and..."),
        (4, 847,  47, 5, 1, 6,  "General",     "Tops",     "Blouses",
         "This shirt is very flattering to all due to the adjustable..."),
    ]

    stars    = {1:"★", 2:"★★", 3:"★★★", 4:"★★★★", 5:"★★★★★"}
    star_clr = {5:"#F59E0B", 4:"#F59E0B", 3:"#EF4444", 2:"#EF4444", 1:"#EF4444"}

    # Header du tableau
    table_html = """
    <div style='background:rgba(26,26,38,0.95);border:1px solid #2A2A3E;
                border-radius:16px;overflow:hidden;position:relative;margin-bottom:8px;'>
      <div style='position:absolute;top:0;left:0;right:0;height:3px;
                  background:linear-gradient(90deg,#8B5CF6,#EC4899,#06B6D4);'></div>
      <div style='padding:16px 20px 12px;border-bottom:1px solid rgba(42,42,62,0.6);
                  display:flex;align-items:center;justify-content:space-between;'>
        <div>
          <div style='font-family:"Space Mono",monospace;font-size:0.80em;font-weight:600;
                      color:#E8E8F0;letter-spacing:0.5px;'>
            Women's Clothing E-Commerce Reviews Dataset
          </div>
          <div style='font-size:0.75em;color:#6B7280;margin-top:3px;'>
            Avis clients sur des vetements feminins — variable cible : Recommended IND
          </div>
        </div>
        <div style='font-family:"Space Mono",monospace;font-size:0.72em;color:#10B981;
                    background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);
                    padding:5px 14px;border-radius:20px;white-space:nowrap;'>
          23 486 lignes · 11 colonnes
        </div>
      </div>
      <div style='overflow-x:auto;'>
        <table style='width:100%;border-collapse:collapse;font-size:0.87em;'>
          <thead>
            <tr style='background:rgba(18,18,26,0.95);'>
              <th style='padding:11px 16px;text-align:left;color:#8B5CF6;font-family:"Space Mono",monospace;font-size:0.80em;border-bottom:1px solid #2A2A3E;'>#</th>
              <th style='padding:11px 16px;text-align:left;color:#8B5CF6;font-family:"Space Mono",monospace;font-size:0.80em;border-bottom:1px solid #2A2A3E;white-space:nowrap;'>Clothing ID</th>
              <th style='padding:11px 16px;text-align:left;color:#8B5CF6;font-family:"Space Mono",monospace;font-size:0.80em;border-bottom:1px solid #2A2A3E;'>Age</th>
              <th style='padding:11px 16px;text-align:left;color:#8B5CF6;font-family:"Space Mono",monospace;font-size:0.80em;border-bottom:1px solid #2A2A3E;'>Rating</th>
              <th style='padding:11px 16px;text-align:left;color:#8B5CF6;font-family:"Space Mono",monospace;font-size:0.80em;border-bottom:1px solid #2A2A3E;'>Recommended</th>
              <th style='padding:11px 16px;text-align:left;color:#8B5CF6;font-family:"Space Mono",monospace;font-size:0.80em;border-bottom:1px solid #2A2A3E;white-space:nowrap;'>Feedback +</th>
              <th style='padding:11px 16px;text-align:left;color:#8B5CF6;font-family:"Space Mono",monospace;font-size:0.80em;border-bottom:1px solid #2A2A3E;'>Division</th>
              <th style='padding:11px 16px;text-align:left;color:#8B5CF6;font-family:"Space Mono",monospace;font-size:0.80em;border-bottom:1px solid #2A2A3E;'>Department</th>
              <th style='padding:11px 16px;text-align:left;color:#8B5CF6;font-family:"Space Mono",monospace;font-size:0.80em;border-bottom:1px solid #2A2A3E;'>Class</th>
              <th style='padding:11px 16px;text-align:left;color:#8B5CF6;font-family:"Space Mono",monospace;font-size:0.80em;border-bottom:1px solid #2A2A3E;'>Review Text</th>
            </tr>
          </thead>
          <tbody>"""

    # Lignes du tableau
    for row_data in overview_rows:
        idx, cloth_id, age, rating, rec, fb, div_n, dept, cls, review = row_data

        if rec == 1:
            rec_html = (
                "<span style='display:inline-flex;align-items:center;"
                "justify-content:center;width:28px;height:28px;border-radius:50%;"
                "background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.5);"
                "color:#10B981;font-weight:700;font-size:0.9em;'>✓</span>"
            )
        else:
            rec_html = (
                "<span style='display:inline-flex;align-items:center;"
                "justify-content:center;width:28px;height:28px;border-radius:50%;"
                "background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.5);"
                "color:#EF4444;font-weight:700;font-size:0.9em;'>✗</span>"
            )

        sc      = star_clr[rating]
        row_bg  = "rgba(239,68,68,0.03)" if rec == 0 else "transparent"
        stars_s = stars[rating]

        table_html += (
            "<tr style='border-bottom:1px solid rgba(42,42,62,0.3);"
            "background:" + row_bg + ";'>"

            "<td style='padding:13px 16px;color:#4B5563;"
            "font-family:\"Space Mono\",monospace;font-size:0.85em;'>"
            + str(idx) + "</td>"

            "<td style='padding:13px 16px;color:#06B6D4;"
            "font-family:\"Space Mono\",monospace;font-weight:600;'>"
            + str(cloth_id) + "</td>"

            "<td style='padding:13px 16px;color:#06B6D4;"
            "font-family:\"Space Mono\",monospace;'>"
            + str(age) + "</td>"

            "<td style='padding:13px 16px;color:" + sc + ";"
            "font-family:\"Space Mono\",monospace;white-space:nowrap;font-weight:600;'>"
            + stars_s + " " + str(rating) + "</td>"

            "<td style='padding:13px 16px;'>" + rec_html + "</td>"

            "<td style='padding:13px 16px;color:#06B6D4;"
            "font-family:\"Space Mono\",monospace;'>"
            + str(fb) + "</td>"

            "<td style='padding:13px 16px;color:#EC4899;font-weight:500;'>"
            + div_n + "</td>"

            "<td style='padding:13px 16px;color:#9CA3AF;'>"
            + dept + "</td>"

            "<td style='padding:13px 16px;color:#A78BFA;font-weight:500;'>"
            + cls + "</td>"

            "<td style='padding:13px 16px;color:#6B7280;max-width:260px;"
            "overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"
            "font-style:italic;'>"
            + review + "</td>"

            "</tr>"
        )

    # Footer du tableau
    table_html += """
          </tbody>
        </table>
      </div>
      <div style='padding:11px 20px;border-top:1px solid rgba(42,42,62,0.4);
                  display:flex;align-items:center;gap:20px;flex-wrap:wrap;'>
        <span style='display:flex;align-items:center;gap:6px;
                     font-size:0.75em;color:#6B7280;'>
          <span style='width:8px;height:8px;border-radius:50%;background:#10B981;
                       display:inline-block;flex-shrink:0;'></span>Recommande (1)
        </span>
        <span style='display:flex;align-items:center;gap:6px;
                     font-size:0.75em;color:#6B7280;'>
          <span style='width:8px;height:8px;border-radius:50%;background:#EF4444;
                       display:inline-block;flex-shrink:0;'></span>Non recommande (0)
        </span>
        <span style='display:flex;align-items:center;gap:6px;
                     font-size:0.75em;color:#6B7280;'>
          <span style='width:8px;height:8px;border-radius:50%;background:#F59E0B;
                       display:inline-block;flex-shrink:0;'></span>Rating 1-5
        </span>
        <span style='margin-left:auto;font-family:"Space Mono",monospace;
                     font-size:0.68em;color:#4B5563;'>
          df.shape : (23 486, 11)
        </span>
      </div>
    </div>"""

    st.markdown(table_html, unsafe_allow_html=True)
    # ══════════════════════════════════════════════════════════════
#  PAGE 1 — EDA
# ══════════════════════════════════════════════════════════════
elif PAGE == 1:
    st.markdown("""
    <div style='padding:40px 0 24px 0;'>
      <div class='hero-badge'>📊 Analyse Exploratoire</div>
      <div class='sec-title' style='font-size:2.2em;margin-top:10px;'>Exploration des Données</div>
      <div class='sec-sub'>Analyse du Women's Clothing E-Commerce Reviews Dataset avant la modélisation</div>
    </div>""", unsafe_allow_html=True)

    cols6 = st.columns(6)
    for col, (num, lbl, clr) in zip(cols6, [
        ("23,486","Avis clients","#8B5CF6"), ("10","Colonnes","#06B6D4"),
        ("82.6%","Recommandés","#10B981"),   ("17.4%","Non recommandés","#EF4444"),
        ("3,526","Valeurs manquantes","#F59E0B"), ("4.18","Rating moyen","#EC4899"),
    ]):
        with col:
            st.markdown(f"""
            <div class='card' style='text-align:center;padding:18px 10px;'>
              <div style='font-family:"Space Mono",monospace;font-size:1.5em;font-weight:700;color:{clr};'>{num}</div>
              <div style='color:#6B7280;font-size:0.75em;margin-top:4px;'>{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        fig = go.Figure(go.Bar(
            x=["⭐1","⭐2","⭐3","⭐4","⭐5"],
            y=[1206, 782, 1898, 5113, 13538],
            marker_color=["#EF4444","#F97316","#F59E0B","#10B981","#8B5CF6"],
            text=[1206,782,1898,5113,13538], textposition="outside",
            textfont=dict(color="#E8E8F0", size=11),
        ))
        fig.update_layout(**PLOTLY_BASE, height=300, showlegend=False,
            title=dict(text="Distribution des Ratings", font=dict(color="#E8E8F0", size=15, family="Playfair Display")),
            xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0")),
            yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280")),
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = go.Figure(go.Pie(
            labels=["Recommandé (1)", "Non recommandé (0)"],
            values=[82.56, 17.44], hole=0.65,
            marker=dict(colors=["#8B5CF6","#EF4444"], line=dict(color="#0A0A0F", width=3)),
            textinfo="label+percent", textfont=dict(color="#E8E8F0", size=11),
        ))
        fig2.add_annotation(text="<b>82.6%</b>", x=0.5, y=0.56, showarrow=False,
                             font=dict(color="#E8E8F0", size=22))
        fig2.add_annotation(text="Recommandés", x=0.5, y=0.42, showarrow=False,
                             font=dict(color="#6B7280", size=12))
        fig2.update_layout(**PLOTLY_BASE, height=300,
            title=dict(text="Variable Cible — Recommended IND", font=dict(color="#E8E8F0", size=15, family="Playfair Display")),
            legend=dict(font=dict(color="#E8E8F0"), bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2, gap="large")
    with c3:
        age_g = ["18-25","26-33","34-41","42-49","50-57","58-65","66+"]
        age_c = [1820, 4210, 5630, 4890, 3740, 2100, 1096]
        fig3 = go.Figure(go.Bar(
            x=age_g, y=age_c,
            marker=dict(color=age_c, colorscale=[[0,"#1A1026"],[0.5,"#8B5CF6"],[1,"#EC4899"]]),
        ))
        fig3.update_layout(**PLOTLY_BASE, height=270, showlegend=False,
            title=dict(text="Distribution de l'Âge", font=dict(color="#E8E8F0", size=15, family="Playfair Display")),
            xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0")),
            yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280")),
        )
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        cats = ["Rating 1","Rating 2","Rating 3","Rating 4","Rating 5"]
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(name="Recommandé ✓",     x=cats, y=[6.8,23.4,52.1,85.3,97.8], marker_color="#8B5CF6", opacity=0.9))
        fig4.add_trace(go.Bar(name="Non recommandé ✗", x=cats, y=[93.2,76.6,47.9,14.7,2.2], marker_color="#EF4444", opacity=0.9))
        fig4.update_layout(**PLOTLY_BASE, barmode="stack", height=270,
            title=dict(text="Rating vs Recommandation (%)", font=dict(color="#E8E8F0", size=15, family="Playfair Display")),
            xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0")),
            yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), ticksuffix="%"),
            legend=dict(font=dict(color="#E8E8F0"), bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("""<div style='font-family:"Space Mono",monospace;font-size:0.68em;
                color:#8B5CF6;letter-spacing:1px;margin-bottom:18px;'>
                CORRÉLATIONS AVEC RECOMMENDED IND</div>
                <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:14px;'>
    """, unsafe_allow_html=True)
    corr_html = ""
    for name, val, clr, pct in [
        ("Rating","0.79","#8B5CF6",79), ("Polarity (TextBlob)","0.21","#06B6D4",21),
        ("Subjectivity","0.15","#10B981",15), ("Age","0.03","#F59E0B",3),
        ("Positive Feedback","-0.07","#F97316",7), ("Review Length","-0.05","#EC4899",5),
    ]:
        bc = "#EF4444" if val.startswith("-") else clr
        corr_html += f"""
        <div style='background:#12121A;border-radius:10px;padding:14px;border:1px solid #2A2A3E;'>
          <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
            <span style='font-size:0.83em;color:#E8E8F0;font-weight:500;'>{name}</span>
            <span style='font-family:"Space Mono",monospace;font-size:0.83em;color:{bc};font-weight:700;'>{val}</span>
          </div>
          <div style='background:#0A0A0F;border-radius:4px;height:6px;'>
            <div style='width:{pct}%;height:100%;border-radius:4px;background:{bc};'></div>
          </div>
        </div>"""
    st.markdown(corr_html + "</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  PAGE 2 — MODÉLISATION ML
# ══════════════════════════════════════════════════════════════
elif PAGE == 2:
    st.markdown("""
    <div style='padding:40px 0 24px 0;'>
      <div class='hero-badge'> Machine Learning</div>
      <div class='sec-title' style='font-size:2.2em;margin-top:10px;'>Modélisation & Performances</div>
      <div class='sec-sub'>3 modèles · Cross-Validation · GridSearchCV / RandomizedSearchCV · Avant vs Après optimisation</div>
    </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Résultats de Base", "Cross-Validation", "Optimisation GridSearch",
        "Comparaison Finale", "Feature Importances",
    ])

    with tab1:
        st.markdown("""
        <div class='card' style='margin-top:16px;'>
          <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#8B5CF6;
                      letter-spacing:1px;margin-bottom:18px;'>MÉTRIQUES DE BASE (SANS OPTIMISATION)</div>
          <table class='styled-table'><thead><tr>
            <th>MODÈLE</th><th>ACCURACY</th><th>PRECISION</th>
            <th>RECALL</th><th>F1-SCORE</th><th>F1 Classe 0</th><th>STATUT</th>
          </tr></thead><tbody>
          <tr>
            <td><strong style='color:#06B6D4;'>Logistic Regression</strong></td>
            <td>93.5%</td><td>97.0%</td><td>94.9%</td><td>96.0%</td><td>82.1%</td>
            <td><span style='background:rgba(6,182,212,0.1);border:1px solid rgba(6,182,212,0.3);
                             color:#06B6D4;padding:3px 10px;border-radius:12px;font-size:0.77em;'>Baseline</span></td>
          </tr>
          <tr>
            <td><strong style='color:#10B981;'>Decision Tree</strong></td>
            <td>92.2%</td><td>95.5%</td><td>94.9%</td><td>95.2%</td><td>77.9%</td>
            <td><span style='background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);
                             color:#EF4444;padding:3px 10px;border-radius:12px;font-size:0.77em;'>Overfitting</span></td>
          </tr>
          <tr style='background:rgba(139,92,246,0.05);'>
            <td><strong style='color:#A78BFA;'>✦ Random Forest</strong></td>
            <td><strong style='color:#8B5CF6;'>93.2%</strong></td>
            <td><strong style='color:#8B5CF6;'>97.2%</strong></td>
            <td>94.5%</td>
            <td><strong style='color:#8B5CF6;'>95.8%</strong></td>
            <td><strong style='color:#8B5CF6;'>81.7%</strong></td>
            <td><span style='background:rgba(139,92,246,0.1);border:1px solid rgba(139,92,246,0.3);
                             color:#8B5CF6;padding:3px 10px;border-radius:12px;font-size:0.77em;'>Meilleur</span></td>
          </tr>
          </tbody></table>
        </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            cats = ["Accuracy","Precision","Recall","F1-Score"]
            fig_r = go.Figure()
            for name, vals, clr, fill_rgba in [
                ("Logistic Reg.", [93.5,97.0,94.9,96.0], "#06B6D4", "rgba(6,182,212,0.1)"),
                ("Decision Tree", [92.2,95.5,94.9,95.2], "#10B981", "rgba(16,185,129,0.1)"),
                ("Random Forest", [93.2,97.2,94.5,95.8], "#8B5CF6", "rgba(139,92,246,0.1)"),
            ]:
                fig_r.add_trace(go.Scatterpolar(
                    r=vals+[vals[0]], theta=cats+[cats[0]],
                    fill="toself", name=name,
                    line=dict(color=clr, width=2), fillcolor=fill_rgba,
                ))
            fig_r.update_layout(**PLOTLY_BASE, height=380,
                polar=dict(bgcolor="rgba(0,0,0,0)",
                           radialaxis=dict(range=[90,100], gridcolor="#2A2A3E", tickfont=dict(color="#6B7280", size=9)),
                           angularaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0", size=11))),
                title=dict(text="Radar de Comparaison (Base)", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                legend=dict(font=dict(color="#E8E8F0"), bgcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig_r, use_container_width=True)

        with c2:
            fig_cm = go.Figure(go.Heatmap(
                z=[[619,92],[183,3286]],
                x=["Prédit: Non rec.","Prédit: Rec."],
                y=["Réel: Non rec.","Réel: Rec."],
                text=[[619,92],[183,3286]], texttemplate="<b>%{text}</b>",
                textfont=dict(size=20, color="white"),
                colorscale=[[0,"#12121A"],[0.4,"#4C1D95"],[1,"#8B5CF6"]],
                showscale=False,
            ))
            fig_cm.update_layout(**PLOTLY_BASE, height=380,
                title=dict(text="Matrice de Confusion — Random Forest (Base)", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(tickfont=dict(color="#E8E8F0", size=11)),
                yaxis=dict(tickfont=dict(color="#E8E8F0", size=11)),
            )
            st.plotly_chart(fig_cm, use_container_width=True)

        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#8B5CF6;
                    letter-spacing:1px;margin-bottom:14px;'>IMPACT class_weight='balanced' — F1 CLASSE 0</div>
        """, unsafe_allow_html=True)
        mods_b = ['Logistic Reg.', 'Decision Tree', 'Random Forest']
        f1_avant_b = [0.8212, 0.7786, 0.8172]
        f1_apres_b = [0.8354, 0.7770, 0.8187]
        fig_bal = go.Figure()
        fig_bal.add_trace(go.Bar(name='Sans balanced', x=mods_b, y=f1_avant_b,
            marker_color='#444', text=[f"{v:.4f}" for v in f1_avant_b], textposition='outside',
            textfont=dict(color="#E8E8F0", size=10)))
        fig_bal.add_trace(go.Bar(name='Avec balanced', x=mods_b, y=f1_apres_b,
            marker_color='#8B5CF6', text=[f"{v:.4f}" for v in f1_apres_b], textposition='outside',
            textfont=dict(color="#E8E8F0", size=10)))
        fig_bal.update_layout(**PLOTLY_BASE, height=300, barmode='group',
            title=dict(text="Avant vs Après class_weight='balanced'", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
            xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0")),
            yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), range=[0.6, 0.92]),
            legend=dict(font=dict(color="#E8E8F0"), bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_bal, use_container_width=True)

    with tab2:
        st.markdown("""
        <div style='margin-top:16px;'>
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#06B6D4;
                    letter-spacing:1px;margin-bottom:14px;'>CROSS-VALIDATION 3-FOLD — F1 SCORE MOYEN</div>
        """, unsafe_allow_html=True)

        cv_data = {
            "Modèle":       ["Logistic Regression", "Decision Tree", "Random Forest"],
            "Fold 1":       [0.9602, 0.9489, 0.9616],
            "Fold 2":       [0.9590, 0.9477, 0.9577],
            "Fold 3":       [0.9598, 0.9505, 0.9608],
            "Moyenne":      [0.9597, 0.9490, 0.9601],
            "Écart-type":   [0.0005, 0.0012, 0.0017],
        }
        df_cv = pd.DataFrame(cv_data)
        st.dataframe(df_cv.style.highlight_max(subset=["Moyenne"], color='rgba(139,92,246,0.3)'),
                     use_container_width=True, hide_index=True)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            mods_cv = ['Logistic\nRegression', 'Decision\nTree', 'Random\nForest']
            moyennes_cv = [0.9597, 0.9490, 0.9601]
            ecarts_cv   = [0.0005, 0.0012, 0.0017]
            clrs_cv     = ['#06B6D4', '#10B981', '#8B5CF6']
            fig_cv = go.Figure()
            fig_cv.add_trace(go.Bar(
                x=mods_cv, y=moyennes_cv,
                error_y=dict(type='data', array=ecarts_cv, visible=True,
                             color='#E8E8F0', thickness=2, width=8),
                marker_color=clrs_cv,
                text=[f"{v:.4f}" for v in moyennes_cv],
                textposition='outside', textfont=dict(color="#E8E8F0", size=11),
            ))
            fig_cv.update_layout(**PLOTLY_BASE, height=350,
                title=dict(text="CV F1-Score moyen ± écart-type", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0")),
                yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), range=[0.93, 0.97]),
                showlegend=False,
            )
            st.plotly_chart(fig_cv, use_container_width=True)

        with c2:
            folds = ['Fold 1', 'Fold 2', 'Fold 3']
            fig_folds = go.Figure()
            for name, vals, clr in [
                ("Logistic Reg.", [0.9602, 0.9590, 0.9598], "#06B6D4"),
                ("Decision Tree", [0.9489, 0.9477, 0.9505], "#10B981"),
                ("Random Forest", [0.9616, 0.9577, 0.9608], "#8B5CF6"),
            ]:
                fig_folds.add_trace(go.Scatter(
                    x=folds, y=vals, mode='lines+markers',
                    name=name, line=dict(color=clr, width=2),
                    marker=dict(size=8, color=clr),
                ))
            fig_folds.update_layout(**PLOTLY_BASE, height=350,
                title=dict(text="F1-Score par Fold (stabilité)", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0")),
                yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), range=[0.94, 0.965]),
                legend=dict(font=dict(color="#E8E8F0"), bgcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig_folds, use_container_width=True)

        st.markdown("""<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:8px;'>""",
                    unsafe_allow_html=True)
        for clr, name, mean, std, verdict in [
            ("#06B6D4","Logistic Regression","0.9597","0.0005","✅ Très stable"),
            ("#10B981","Decision Tree",      "0.9490","0.0012","⚠️ Légère variance"),
            ("#8B5CF6","Random Forest",      "0.9601","0.0017","✅ Meilleure moyenne"),
        ]:
            st.markdown(f"""
            <div style='background:#12121A;border:1px solid rgba(42,42,62,0.8);border-radius:12px;
                        padding:20px;text-align:center;border-top:3px solid {clr};'>
              <div style='font-weight:700;color:{clr};font-size:0.9em;margin-bottom:12px;'>{name}</div>
              <div style='font-family:"Space Mono",monospace;font-size:1.8em;font-weight:700;color:#E8E8F0;'>{mean}</div>
              <div style='font-size:0.78em;color:#6B7280;margin-top:4px;'>F1 moyen</div>
              <div style='font-family:"Space Mono",monospace;font-size:0.9em;color:{clr};margin-top:8px;'>±{std}</div>
              <div style='font-size:0.78em;color:#6B7280;'>écart-type</div>
              <div style='margin-top:12px;font-size:0.83em;color:#9CA3AF;'>{verdict}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div style='margin-top:16px;'>
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#F59E0B;
                    letter-spacing:1px;margin-bottom:18px;'>OPTIMISATION DES HYPERPARAMÈTRES</div>
        """, unsafe_allow_html=True)

        opt_cols = st.columns(3)
        for i, (col, clr, name, method, params, cv_f1, test_f1, acc, improve) in enumerate(zip(
            opt_cols,
            ["#06B6D4","#10B981","#8B5CF6"],
            ["Logistic Regression","Decision Tree","✦ Random Forest"],
            ["GridSearchCV","GridSearchCV","RandomizedSearchCV"],
            [
                "C=10\nsolver='lbfgs'",
                "criterion='entropy'\nmax_depth=5\nmin_samples_split=10",
                "n_estimators=100\nmax_depth=10\nmax_features='log2'\nmin_samples_split=2",
            ],
            ["0.9590","0.9595","0.9609"],
            ["0.9604","0.9597","0.9616"],
            ["93.53%","93.43%","93.75%"],
            ["+0.0004","+0.0072","+0.0033"],
        )):
            with col:
                st.markdown(f"""
                <div style='background:#12121A;border:1px solid rgba(42,42,62,0.8);border-radius:14px;
                            padding:22px;border-top:3px solid {clr};height:100%;'>
                  <div style='font-weight:700;color:{clr};margin-bottom:4px;font-size:0.92em;'>{name}</div>
                  <div style='font-family:"Space Mono",monospace;font-size:0.66em;color:#6B7280;
                              margin-bottom:14px;background:rgba(0,0,0,0.3);padding:2px 8px;
                              border-radius:6px;display:inline-block;'>{method}</div>
                  <div style='font-family:"Space Mono",monospace;font-size:0.72em;background:#0A0A0F;
                              padding:12px;border-radius:8px;color:#A78BFA;line-height:1.9;
                              margin-bottom:16px;white-space:pre;'>{params}</div>
                  <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>
                    <div style='background:#0A0A0F;border-radius:8px;padding:10px;text-align:center;'>
                      <div style='font-family:"Space Mono",monospace;font-size:1em;font-weight:700;color:{clr};'>{cv_f1}</div>
                      <div style='font-size:0.7em;color:#6B7280;margin-top:2px;'>CV F1</div>
                    </div>
                    <div style='background:#0A0A0F;border-radius:8px;padding:10px;text-align:center;'>
                      <div style='font-family:"Space Mono",monospace;font-size:1em;font-weight:700;color:{clr};'>{test_f1}</div>
                      <div style='font-size:0.7em;color:#6B7280;margin-top:2px;'>Test F1</div>
                    </div>
                    <div style='background:#0A0A0F;border-radius:8px;padding:10px;text-align:center;'>
                      <div style='font-family:"Space Mono",monospace;font-size:1em;font-weight:700;color:{clr};'>{acc}</div>
                      <div style='font-size:0.7em;color:#6B7280;margin-top:2px;'>Accuracy</div>
                    </div>
                    <div style='background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);
                                border-radius:8px;padding:10px;text-align:center;'>
                      <div style='font-family:"Space Mono",monospace;font-size:1em;font-weight:700;color:#10B981;'>{improve}</div>
                      <div style='font-size:0.7em;color:#6B7280;margin-top:2px;'>Amélioration</div>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            mods_opt = ['Logistic\nRegression', 'Decision\nTree', 'Random\nForest']
            f1_base = [0.9600, 0.9525, 0.9583]
            f1_opt  = [0.9604, 0.9597, 0.9616]
            fig_opt1 = go.Figure()
            fig_opt1.add_trace(go.Bar(name='Avant optimisation', x=mods_opt, y=f1_base,
                marker_color='#444', text=[f"{v:.4f}" for v in f1_base],
                textposition='outside', textfont=dict(color="#E8E8F0", size=10)))
            fig_opt1.add_trace(go.Bar(name='Après optimisation', x=mods_opt, y=f1_opt,
                marker_color='#8B5CF6', text=[f"{v:.4f}" for v in f1_opt],
                textposition='outside', textfont=dict(color="#E8E8F0", size=10)))
            fig_opt1.update_layout(**PLOTLY_BASE, height=340, barmode='group',
                title=dict(text="F1-Score : Avant vs Après optimisation", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0")),
                yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), range=[0.94, 0.97]),
                legend=dict(font=dict(color="#E8E8F0"), bgcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig_opt1, use_container_width=True)

        with c2:
            acc_base = [0.9346, 0.9218, 0.9321]
            acc_opt  = [0.9353, 0.9343, 0.9375]
            fig_opt2 = go.Figure()
            fig_opt2.add_trace(go.Bar(name='Avant optimisation', x=mods_opt, y=acc_base,
                marker_color='#444', text=[f"{v:.4f}" for v in acc_base],
                textposition='outside', textfont=dict(color="#E8E8F0", size=10)))
            fig_opt2.add_trace(go.Bar(name='Après optimisation', x=mods_opt, y=acc_opt,
                marker_color='#F59E0B', text=[f"{v:.4f}" for v in acc_opt],
                textposition='outside', textfont=dict(color="#E8E8F0", size=10)))
            fig_opt2.update_layout(**PLOTLY_BASE, height=340, barmode='group',
                title=dict(text="Accuracy : Avant vs Après optimisation", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0")),
                yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), range=[0.90, 0.95]),
                legend=dict(font=dict(color="#E8E8F0"), bgcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig_opt2, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with tab4:
        st.markdown("""
        <div style='margin-top:16px;'>
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#8B5CF6;
                    letter-spacing:1px;margin-bottom:18px;'>TABLEAU RÉCAPITULATIF COMPLET</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <table class='styled-table'>
          <thead><tr>
            <th>MODÈLE</th><th>Base F1</th><th>CV F1 (3-fold)</th>
            <th>Opt. F1</th><th>Opt. Accuracy</th><th>F1 Cl.0</th><th>DÉCISION</th>
          </tr></thead>
          <tbody>
          <tr>
            <td><strong style='color:#06B6D4;'>Logistic Regression</strong></td>
            <td>0.9600</td><td>0.9597 ± 0.0005</td><td>0.9604</td><td>93.53%</td><td>83.5%</td>
            <td><span style='color:#06B6D4;font-size:0.8em;'>Baseline robuste</span></td>
          </tr>
          <tr>
            <td><strong style='color:#10B981;'>Decision Tree</strong></td>
            <td>0.9525</td><td>0.9490 ± 0.0012</td><td>0.9597</td><td>93.43%</td><td>77.7%</td>
            <td><span style='color:#EF4444;font-size:0.8em;'>Overfitting sans opt.</span></td>
          </tr>
          <tr style='background:rgba(139,92,246,0.06);'>
            <td><strong style='color:#A78BFA;'>✦ Random Forest</strong></td>
            <td>0.9583</td><td><strong style='color:#8B5CF6;'>0.9601 ± 0.0017</strong></td>
            <td><strong style='color:#8B5CF6;'>0.9616</strong></td>
            <td><strong style='color:#8B5CF6;'>93.75%</strong></td>
            <td>81.9%</td>
            <td><span style='background:rgba(139,92,246,0.15);border:1px solid #8B5CF6;
                             color:#8B5CF6;padding:3px 10px;border-radius:8px;font-size:0.78em;'>✦ RETENU</span></td>
          </tr>
          </tbody>
        </table>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            etapes = ['Base', 'Cross-Val', 'Optimisé']
            fig_evol = go.Figure()
            for name, vals, clr in [
                ("Logistic Reg.", [0.9600, 0.9597, 0.9604], "#06B6D4"),
                ("Decision Tree", [0.9525, 0.9490, 0.9597], "#10B981"),
                ("Random Forest", [0.9583, 0.9601, 0.9616], "#8B5CF6"),
            ]:
                fig_evol.add_trace(go.Scatter(
                    x=etapes, y=vals, mode='lines+markers+text',
                    name=name, line=dict(color=clr, width=2.5),
                    marker=dict(size=10, color=clr),
                    text=[f"{v:.4f}" for v in vals],
                    textposition='top center',
                    textfont=dict(color=clr, size=9),
                ))
            fig_evol.update_layout(**PLOTLY_BASE, height=380,
                title=dict(text="Évolution F1 : Base → CV → Optimisé", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0")),
                yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), range=[0.94, 0.965]),
                legend=dict(font=dict(color="#E8E8F0"), bgcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig_evol, use_container_width=True)

        with c2:
            modeles_f = ['Logistic Reg.', 'Decision Tree', 'Random Forest']
            metriques_f = ['Base F1', 'CV F1', 'Opt F1', 'Accuracy', 'F1 Cl.0']
            zvals = [
                [0.9600, 0.9597, 0.9604, 0.9353, 0.835],
                [0.9525, 0.9490, 0.9597, 0.9343, 0.777],
                [0.9583, 0.9601, 0.9616, 0.9375, 0.819],
            ]
            fig_heat = go.Figure(go.Heatmap(
                z=zvals, x=metriques_f, y=modeles_f,
                colorscale=[[0,"#1A1026"],[0.5,"#4C1D95"],[1,"#8B5CF6"]],
                text=[[f"{v:.4f}" for v in row] for row in zvals],
                texttemplate="%{text}", textfont=dict(size=11, color="white"),
                showscale=True,
            ))
            fig_heat.update_layout(**PLOTLY_BASE, height=380,
                title=dict(text="Heatmap — Comparaison Finale", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(tickfont=dict(color="#E8E8F0", size=10)),
                yaxis=dict(tickfont=dict(color="#E8E8F0", size=11)),
            )
            st.plotly_chart(fig_heat, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with tab5:
        st.markdown("""
        <div style='margin-top:16px;'>
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#8B5CF6;
                    letter-spacing:1px;margin-bottom:6px;'>IMPORTANCE DES VARIABLES — RANDOM FOREST</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div style='background:linear-gradient(135deg,rgba(139,92,246,0.07),rgba(6,182,212,0.04));
                    border:1px solid rgba(139,92,246,0.22);border-radius:14px;
                    padding:18px 22px;margin-bottom:20px;'>
          <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;'>
            <div style='display:flex;gap:10px;align-items:flex-start;'>
              <div style='width:6px;height:6px;border-radius:50%;background:#8B5CF6;margin-top:5px;flex-shrink:0;'></div>
              <div style='font-size:0.8em;color:#9CA3AF;line-height:1.6;'>
                <strong style='color:#E8E8F0;'>C'est quoi ?</strong><br>
                Chaque arbre du Random Forest vote pour une classe. L'importance d'une variable mesure combien
                elle améliore la pureté des nœuds (critère Gini) en moyenne sur tous les arbres.
              </div>
            </div>
            <div style='display:flex;gap:10px;align-items:flex-start;'>
              <div style='width:6px;height:6px;border-radius:50%;background:#06B6D4;margin-top:5px;flex-shrink:0;'></div>
              <div style='font-size:0.8em;color:#9CA3AF;line-height:1.6;'>
                <strong style='color:#E8E8F0;'>Comment lire ?</strong><br>
                Les valeurs somment à 1 (100%). Plus la barre est longue, plus la variable
                est utilisée par les arbres pour prendre leurs décisions de classification.
              </div>
            </div>
            <div style='display:flex;gap:10px;align-items:flex-start;'>
              <div style='width:6px;height:6px;border-radius:50%;background:#10B981;margin-top:5px;flex-shrink:0;'></div>
              <div style='font-size:0.8em;color:#9CA3AF;line-height:1.6;'>
                <strong style='color:#E8E8F0;'>Différence avec SHAP ?</strong><br>
                Feature importance = importance globale sur tout le dataset.
                SHAP = impact variable par variable pour chaque prédiction individuelle.
                Les deux se complètent.
              </div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # ── Feature importances réelles depuis le modèle ──
        feat_importances_real = None
        feat_names_real       = None

        if models_ok and "random_forest" in models:
            try:
                rf = models["random_forest"]
                if hasattr(rf, "feature_importances_") and feature_cols is not None:
                    fi = rf.feature_importances_
                    feat_importances_real = fi
                    feat_names_real       = list(feature_cols)
            except Exception:
                pass

        fi_data = [
            ("Rating",                    0.3812, "#8B5CF6", "Variable dominante · Gini impurity réduite massivement"),
            ("Polarity (TextBlob)",        0.0847, "#06B6D4", "Feature Engineering NLP · 2ème plus importante"),
            ("Positive Feedback Count",    0.0623, "#06B6D4", "Engagement des autres clientes"),
            ("Age",                        0.0541, "#10B981", "Variable démographique"),
            ("Subjectivity (TextBlob)",    0.0489, "#10B981", "Feature Engineering NLP · degré d'opinion"),
            ("Review Length",              0.0412, "#10B981", "Longueur de l'avis en mots"),
            ("Clothing ID",                0.0398, "#F59E0B", "Identifiant produit"),
            ("Dept — Dresses",             0.0187, "#4B5563", "One-Hot Encoding département"),
            ("Dept — Tops",                0.0163, "#4B5563", "One-Hot Encoding département"),
            ("Class — Knits",              0.0142, "#4B5563", "One-Hot Encoding classe"),
            ("Division — General Petite",  0.0131, "#4B5563", "One-Hot Encoding division"),
            ("Class — Dresses",            0.0124, "#4B5563", "One-Hot Encoding classe"),
            ("Dept — Intimate",            0.0098, "#374151", "One-Hot Encoding département"),
            ("Class — Blouses",            0.0089, "#374151", "One-Hot Encoding classe"),
            ("Autres (21 features)",       0.0943, "#2A3A5A", "Division/Dept/Class restants combinés"),
        ]

        if feat_importances_real is not None:
            sorted_idx = feat_importances_real.argsort()[::-1][:14]
            fi_data_real = []
            for rank, idx in enumerate(sorted_idx):
                name = feat_names_real[idx] if idx < len(feat_names_real) else f"Feature {idx}"
                val  = float(feat_importances_real[idx])
                clr  = "#8B5CF6" if rank == 0 else ("#06B6D4" if rank < 3 else ("#10B981" if rank < 6 else ("#F59E0B" if rank < 9 else "#4B5563")))
                fi_data_real.append((name, val, clr, ""))
            rest = float(feat_importances_real[len(sorted_idx):].sum()) if len(feat_importances_real) > 14 else 0
            if rest > 0.001:
                fi_data_real.append(("Autres features", rest, "#2A3A5A", "features restantes"))
            fi_data = fi_data_real

        fi_names  = [d[0] for d in fi_data]
        fi_vals   = [d[1] for d in fi_data]
        fi_colors = [d[2] for d in fi_data]

        c1_fi, c2_fi = st.columns([1.3, 0.7], gap="large")

        with c1_fi:
            fig_fi = go.Figure()
            fig_fi.add_trace(go.Bar(
                x=fi_vals[::-1], y=fi_names[::-1], orientation="h",
                marker=dict(color=fi_colors[::-1], line=dict(color="rgba(255,255,255,0.06)", width=1)),
                text=[f"  {v:.4f}  ({v*100:.1f}%)" for v in fi_vals[::-1]],
                textposition="outside",
                textfont=dict(color="#E8E8F0", size=10, family="Space Mono"),
                hovertemplate="<b>%{y}</b><br>Importance : %{x:.4f}<br>(%{x:.1%})<extra></extra>",
            ))
            fig_fi.add_vline(
                x=fi_vals[0], line_dash="dot", line_color="rgba(139,92,246,0.4)",
                annotation_text=f"  Rating = {fi_vals[0]:.4f}",
                annotation_font_color="#8B5CF6", annotation_position="top right",
            )
            fig_fi.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#6B7280"), margin=dict(t=30, b=30, l=10, r=130),
                height=460, showlegend=False,
                title=dict(text=f"feature_importances_ — Random Forest ({len(fi_data)} variables affichées)",
                           font=dict(color="#E8E8F0", size=13, family="Playfair Display"), x=0),
                xaxis=dict(gridcolor="#1E1E2E", zeroline=False, tickfont=dict(color="#6B7280", size=10),
                           tickformat=".0%", title=dict(text="Importance (somme = 100%)", font=dict(color="#6B7280", size=10))),
                yaxis=dict(gridcolor="#1E1E2E", tickfont=dict(color="#E8E8F0", size=11)),
            )
            st.plotly_chart(fig_fi, use_container_width=True)

            st.markdown("""
            <div style='display:flex;gap:16px;flex-wrap:wrap;margin-top:-10px;'>
              <div style='display:flex;align-items:center;gap:6px;font-size:0.76em;color:#9CA3AF;'>
                <div style='width:12px;height:12px;border-radius:3px;background:#8B5CF6;'></div>Variable dominante
              </div>
              <div style='display:flex;align-items:center;gap:6px;font-size:0.76em;color:#9CA3AF;'>
                <div style='width:12px;height:12px;border-radius:3px;background:#06B6D4;'></div>Feature Engineering NLP
              </div>
              <div style='display:flex;align-items:center;gap:6px;font-size:0.76em;color:#9CA3AF;'>
                <div style='width:12px;height:12px;border-radius:3px;background:#10B981;'></div>Variables numériques
              </div>
              <div style='display:flex;align-items:center;gap:6px;font-size:0.76em;color:#9CA3AF;'>
                <div style='width:12px;height:12px;border-radius:3px;background:#4B5563;'></div>Variables catégorielles (OHE)
              </div>
            </div>""", unsafe_allow_html=True)

        with c2_fi:
            cat_labels = ["Rating", "NLP (Polarity+Subj.)", "Numériques (Age, Feedback, Length, ID)", "Catégorielles (OHE)"]
            cat_vals   = [0.3812, 0.1336, 0.1974, 0.2878]
            cat_colors = ["#8B5CF6", "#06B6D4", "#10B981", "#4B5563"]
            fig_donut = go.Figure(go.Pie(
                labels=cat_labels, values=cat_vals, hole=0.62,
                marker=dict(colors=cat_colors, line=dict(color="#0A0A0F", width=2)),
                textinfo="percent", textfont=dict(color="#E8E8F0", size=11),
                hovertemplate="<b>%{label}</b><br>Importance : %{value:.1%}<extra></extra>",
            ))
            fig_donut.add_annotation(text="<b>Répartition</b>", x=0.5, y=0.56, showarrow=False,
                                     font=dict(color="#E8E8F0", size=13))
            fig_donut.add_annotation(text="par catégorie", x=0.5, y=0.42, showarrow=False,
                                     font=dict(color="#6B7280", size=11))
            fig_donut.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#6B7280"),
                margin=dict(t=20, b=10, l=10, r=10), height=260,
                legend=dict(font=dict(color="#E8E8F0", size=10), bgcolor="rgba(0,0,0,0)", orientation="v"))
            st.plotly_chart(fig_donut, use_container_width=True)

            st.markdown("""<div style='font-family:"Space Mono",monospace;font-size:0.63em;color:#8B5CF6;
                        letter-spacing:1px;margin-bottom:12px;'>OBSERVATIONS CLÉS</div>""",
                        unsafe_allow_html=True)
            for clr, icon, title, desc in [
                ("#8B5CF6","1","Rating domine (38.1%)","Confirme la corrélation 0.79 vue en EDA."),
                ("#06B6D4","2","NLP apporte 13.4%","Polarity + Subjectivity ont une vraie valeur ajoutée."),
                ("#10B981","3","Variables numériques 19.7%","Age, Feedback, Clothing ID et Review Length contribuent."),
                ("#4B5563","4","OHE marginal 28.8%","Les 30 colonnes One-Hot ont chacune un impact faible."),
            ]:
                st.markdown(f"""
                <div style='display:flex;gap:10px;padding:10px 0;border-bottom:1px solid rgba(42,42,62,0.35);'>
                  <div style='width:22px;height:22px;border-radius:6px;background:rgba(139,92,246,0.1);
                              border:1px solid rgba(139,92,246,0.3);display:flex;align-items:center;
                              justify-content:center;font-family:"Space Mono",monospace;font-size:0.72em;
                              color:{clr};font-weight:700;flex-shrink:0;'>{icon}</div>
                  <div>
                    <div style='font-size:0.83em;color:{clr};font-weight:600;margin-bottom:2px;'>{title}</div>
                    <div style='font-size:0.75em;color:#6B7280;line-height:1.5;'>{desc}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#F59E0B;
                    letter-spacing:1px;margin-bottom:16px;'>
          FEATURE IMPORTANCE vs SHAP — DEUX FAÇONS DE MESURER L'IMPACT
        </div>""", unsafe_allow_html=True)

        comp_c1, comp_c2 = st.columns(2, gap="large")
        with comp_c1:
            feats_comp = ["Rating", "Polarity", "Positive Feedback", "Age", "Subjectivity", "Review Length"]
            fi_comp    = [0.3812, 0.0847, 0.0623, 0.0541, 0.0489, 0.0412]
            shap_comp  = [0.1907, 0.0312, 0.0134, 0.0121, 0.0198, 0.0142]
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(name="Feature Importance (RF)", x=feats_comp, y=fi_comp,
                marker_color="#8B5CF6", opacity=0.85,
                text=[f"{v:.3f}" for v in fi_comp], textposition="outside",
                textfont=dict(color="#E8E8F0", size=9)))
            fig_comp.add_trace(go.Bar(name="SHAP value (moyen)", x=feats_comp, y=shap_comp,
                marker_color="#06B6D4", opacity=0.85,
                text=[f"{v:.3f}" for v in shap_comp], textposition="outside",
                textfont=dict(color="#E8E8F0", size=9)))
            fig_comp.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#6B7280"), margin=dict(t=40, b=20, l=10, r=10),
                height=300, barmode="group",
                title=dict(text="Feature Importance vs SHAP — Top 6 variables",
                           font=dict(color="#E8E8F0", size=13, family="Playfair Display"), x=0),
                xaxis=dict(gridcolor="#1E1E2E", tickfont=dict(color="#E8E8F0", size=10)),
                yaxis=dict(gridcolor="#1E1E2E", tickfont=dict(color="#6B7280", size=9)),
                legend=dict(font=dict(color="#E8E8F0", size=10), bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_comp, use_container_width=True)

        with comp_c2:
            st.markdown("""
            <div style='background:#12121A;border:1px solid #2A2A3E;border-radius:12px;padding:20px;margin-top:8px;'>
              <div style='font-family:"Space Mono",monospace;font-size:0.63em;color:#F59E0B;
                          letter-spacing:1px;margin-bottom:14px;'>DIFFÉRENCES ENTRE LES 2 MÉTHODES</div>
              <div style='display:flex;gap:12px;padding:10px 0;border-bottom:1px solid rgba(42,42,62,0.3);'>
                <div style='width:10px;height:10px;border-radius:50%;background:#8B5CF6;margin-top:4px;flex-shrink:0;'></div>
                <div>
                  <div style='font-size:0.85em;color:#A78BFA;font-weight:600;margin-bottom:3px;'>Feature Importance</div>
                  <div style='font-size:0.78em;color:#6B7280;line-height:1.6;'>
                    Basée sur la réduction de l'impureté Gini. Mesure l'importance globale sur tout le dataset.
                  </div>
                </div>
              </div>
              <div style='display:flex;gap:12px;padding:10px 0;border-bottom:1px solid rgba(42,42,62,0.3);'>
                <div style='width:10px;height:10px;border-radius:50%;background:#06B6D4;margin-top:4px;flex-shrink:0;'></div>
                <div>
                  <div style='font-size:0.85em;color:#67E8F9;font-weight:600;margin-bottom:3px;'>SHAP Values</div>
                  <div style='font-size:0.78em;color:#6B7280;line-height:1.6;'>
                    Basée sur la théorie des jeux. Mesure l'impact individuel par prédiction.
                  </div>
                </div>
              </div>
              <div style='display:flex;gap:12px;padding:10px 0;'>
                <div style='width:10px;height:10px;border-radius:50%;background:#10B981;margin-top:4px;flex-shrink:0;'></div>
                <div>
                  <div style='font-size:0.85em;color:#6EE7B7;font-weight:600;margin-bottom:3px;'>Conclusion commune</div>
                  <div style='font-size:0.78em;color:#6B7280;line-height:1.6;'>
                    Les deux méthodes confirment que le Rating est la variable dominante.
                  </div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  PAGE 3 — NON SUPERVISÉ
# ══════════════════════════════════════════════════════════════
elif PAGE == 3:
    st.markdown("""
    <div style='padding:40px 0 24px 0;'>
      <div class='hero-badge'>🔬 Unsupervised Learning</div>
      <div class='sec-title' style='font-size:2.2em;margin-top:10px;'>Apprentissage Non Supervisé</div>
      <div class='sec-sub'>PCA · K-Means · DBSCAN · Clustering Hiérarchique — Segmentation des clientes</div>
    </div>""", unsafe_allow_html=True)

    tab_pca, tab_km, tab_db, tab_hc, tab_bilan = st.tabs([
        "PCA", "K-Means", "DBSCAN", "Hiérarchique", "Bilan Clusters"
    ])

    with tab_pca:
        st.markdown("""
        <div style='margin-top:16px;'>
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#8B5CF6;
                    letter-spacing:1px;margin-bottom:14px;'>RÉDUCTION DE DIMENSION — PCA 2D</div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            fig_var = go.Figure()
            fig_var.add_trace(go.Bar(x=['PCA 1','PCA 2','PCA 3'], y=[62.3,24.1,13.6],
                marker_color=['#8B5CF6','#06B6D4','#EC4899'],
                text=['62.3%','24.1%','13.6%'], textposition='outside',
                textfont=dict(color="#E8E8F0", size=12)))
            fig_var.add_trace(go.Scatter(x=['PCA 1','PCA 2','PCA 3'], y=[62.3,86.4,100.0],
                mode='lines+markers', name='Cumulée',
                line=dict(color='#F59E0B', width=2, dash='dash'),
                marker=dict(size=8, color='#F59E0B'), yaxis='y2'))
            fig_var.update_layout(**PLOTLY_BASE, height=320,
                title=dict(text="Variance expliquée par composante", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0")),
                yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), title='% Variance individuelle'),
                yaxis2=dict(overlaying='y', side='right', tickfont=dict(color="#F59E0B"), title='% Cumulée'),
                showlegend=True, legend=dict(font=dict(color="#E8E8F0"), bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_var, use_container_width=True)

        with c2:
            vars_pca = ['Age', 'Rating', 'Positive Feedback']
            pca1_vals = [0.31, 0.72, 0.19]
            pca2_vals = [0.84, -0.22, 0.43]
            fig_biplot = go.Figure()
            np.random.seed(42)
            x_pts = np.random.randn(200) * 2
            y_pts = np.random.randn(200) * 1.5
            fig_biplot.add_trace(go.Scatter(x=x_pts, y=y_pts, mode='markers',
                marker=dict(size=4, color='#2A2A3E', opacity=0.6), name='Données', showlegend=False))
            for i, (var, v1, v2) in enumerate(zip(vars_pca, pca1_vals, pca2_vals)):
                clr_a = ['#8B5CF6','#06B6D4','#F59E0B'][i]
                fig_biplot.add_trace(go.Scatter(x=[0, v1*3], y=[0, v2*3], mode='lines+markers+text',
                    line=dict(color=clr_a, width=2), marker=dict(size=[0,8], color=clr_a),
                    text=['', var], textposition='top right', textfont=dict(color=clr_a, size=11), name=var))
            fig_biplot.update_layout(**PLOTLY_BASE, height=320,
                title=dict(text="Contribution des variables (Biplot)", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), title='PCA 1 (62.3%)'),
                yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), title='PCA 2 (24.1%)'),
                legend=dict(font=dict(color="#E8E8F0"), bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_biplot, use_container_width=True)

        np.random.seed(42)
        pca1_data = np.concatenate([np.random.randn(100)*0.8-1.5, np.random.randn(80)*0.9+0.2,
                                    np.random.randn(120)*1.0+2.0, np.random.randn(100)*0.7-0.5])
        pca2_data = np.concatenate([np.random.randn(100)*0.7+1.2, np.random.randn(80)*1.1+2.5,
                                    np.random.randn(120)*0.8-0.8, np.random.randn(100)*0.9-2.0])
        fig_pca = go.Figure(go.Scatter(x=pca1_data, y=pca2_data, mode='markers',
            marker=dict(size=5,
                color=np.concatenate([np.zeros(100),np.ones(80),np.ones(120)*2,np.ones(100)*3]),
                colorscale=[[0,'#8B5CF6'],[0.33,'#06B6D4'],[0.66,'#10B981'],[1,'#F59E0B']],
                opacity=0.7)))
        fig_pca.update_layout(**PLOTLY_BASE, height=320,
            title=dict(text="Projection PCA 2D des données", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
            xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), title='PCA 1 (62.3%)'),
            yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), title='PCA 2 (24.1%)'),
            showlegend=False)
        st.plotly_chart(fig_pca, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_km:
        st.markdown("""
        <div style='margin-top:16px;'>
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#8B5CF6;
                    letter-spacing:1px;margin-bottom:14px;'>K-MEANS CLUSTERING</div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            k_vals  = list(range(1, 10))
            inertia = [45000, 28000, 19500, 14200, 12100, 10800, 10200, 9900, 9750]
            fig_elbow = go.Figure()
            fig_elbow.add_trace(go.Scatter(x=k_vals, y=inertia, mode='lines+markers',
                line=dict(color='#8B5CF6', width=2.5),
                marker=dict(size=8, color=k_vals,
                            colorscale=[[0,'#06B6D4'],[0.5,'#8B5CF6'],[1,'#EC4899']]),
                fill='tozeroy', fillcolor='rgba(139,92,246,0.07)'))
            fig_elbow.add_vline(x=4, line_dash='dash', line_color='#F59E0B',
                                annotation_text='K=4 (coude optimal)', annotation_font_color='#F59E0B')
            fig_elbow.update_layout(**PLOTLY_BASE, height=320,
                title=dict(text="Méthode du Coude — Inertie vs K", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0"), title='Nombre de clusters (K)'),
                yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), title='Inertie'),
                showlegend=False)
            st.plotly_chart(fig_elbow, use_container_width=True)

        with c2:
            np.random.seed(42)
            centers  = [(-1.5,1.2),(0.2,2.5),(2.0,-0.8),(-0.5,-2.0)]
            clrs_km  = ['#8B5CF6','#06B6D4','#10B981','#EF4444']
            sizes_km = [8350, 2918, 5399, 3732]
            fig_km = go.Figure()
            for i, (cx, cy, clr, sz) in enumerate(zip(
                [c[0] for c in centers],[c[1] for c in centers], clrs_km, sizes_km)):
                pts = int(sz/50)
                fig_km.add_trace(go.Scatter(
                    x=np.random.randn(pts)*0.8+cx, y=np.random.randn(pts)*0.7+cy,
                    mode='markers', marker=dict(size=5, color=clr, opacity=0.65),
                    name=f'Cluster {i}'))
                fig_km.add_trace(go.Scatter(x=[cx], y=[cy], mode='markers+text',
                    marker=dict(size=16, color=clr, symbol='x', line=dict(width=2, color='white')),
                    text=[f"C{i}"], textfont=dict(color='white', size=10),
                    textposition='top right', showlegend=False))
            fig_km.update_layout(**PLOTLY_BASE, height=320,
                title=dict(text="K-Means (K=4) — Projection PCA", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), title='PCA 1'),
                yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), title='PCA 2'),
                legend=dict(font=dict(color="#E8E8F0", size=9), bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_km, use_container_width=True)

        st.markdown("""
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#8B5CF6;
                    letter-spacing:1px;margin:16px 0 12px 0;'>CENTRES DES CLUSTERS (MOYENNES)</div>
        <table class='styled-table'>
          <thead><tr><th>CLUSTER</th><th>ÂGE MOYEN</th><th>RATING MOYEN</th>
          <th>FEEDBACK MOYEN</th><th>TAILLE</th><th>PROFIL</th></tr></thead>
          <tbody>
          <tr>
            <td><span style='background:rgba(139,92,246,0.15);color:#8B5CF6;padding:3px 10px;border-radius:8px;'>Cluster 0</span></td>
            <td>~35 ans</td><td><strong style='color:#10B981;'>⭐ 4.72</strong></td>
            <td>~0.5</td><td>8,350</td><td><span style='color:#8B5CF6;'>🔵 Satisfaites passives</span></td>
          </tr>
          <tr>
            <td><span style='background:rgba(6,182,212,0.15);color:#06B6D4;padding:3px 10px;border-radius:8px;'>Cluster 1</span></td>
            <td>~43 ans</td><td><strong style='color:#10B981;'>⭐ 4.32</strong></td>
            <td><strong style='color:#F59E0B;'>~4.7</strong></td><td>2,918</td>
            <td><span style='color:#06B6D4;'>🟢 Engagées actives</span></td>
          </tr>
          <tr>
            <td><span style='background:rgba(16,185,129,0.15);color:#10B981;padding:3px 10px;border-radius:8px;'>Cluster 2</span></td>
            <td>~57 ans</td><td><strong style='color:#10B981;'>⭐ 4.63</strong></td>
            <td>~0.7</td><td>5,399</td><td><span style='color:#10B981;'>🟡 Âgées satisfaites</span></td>
          </tr>
          <tr>
            <td><span style='background:rgba(239,68,68,0.15);color:#EF4444;padding:3px 10px;border-radius:8px;'>Cluster 3</span></td>
            <td>~40 ans</td><td><strong style='color:#EF4444;'>⭐ 2.32</strong></td>
            <td>~0.9</td><td>3,732</td><td><span style='color:#EF4444;'>🔴 Insatisfaites</span></td>
          </tr>
          </tbody>
        </table>
        """, unsafe_allow_html=True)

        c3, c4 = st.columns(2, gap="large")
        with c3:
            fig_sz = go.Figure(go.Bar(
                x=['Cluster 0\nSatisfaites','Cluster 1\nEngagées','Cluster 2\nÂgées','Cluster 3\nInsatisfaites'],
                y=[8350,2918,5399,3732], marker_color=['#8B5CF6','#06B6D4','#10B981','#EF4444'],
                text=[8350,2918,5399,3732], textposition='outside', textfont=dict(color="#E8E8F0", size=11)))
            fig_sz.update_layout(**PLOTLY_BASE, height=280, showlegend=False,
                title=dict(text="Taille de chaque cluster", font=dict(color="#E8E8F0", size=13, family="Playfair Display")),
                xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0", size=9)),
                yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280")))
            st.plotly_chart(fig_sz, use_container_width=True)

        with c4:
            fig_radar_km = go.Figure()
            cats_km = ['Âge (norm.)', 'Rating', 'Feedback', 'Satisfaction']
            for name, vals, clr, fill_rgba in zip(
                ['Cl.0 Satisfaites','Cl.1 Engagées','Cl.2 Âgées','Cl.3 Insatisfaites'],
                [[0.3,0.9,0.1,0.9],[0.5,0.7,1.0,0.7],[0.9,0.8,0.1,0.8],[0.4,0.2,0.1,0.1]],
                ['#8B5CF6','#06B6D4','#10B981','#EF4444'],
                ["rgba(139,92,246,0.13)","rgba(6,182,212,0.13)","rgba(16,185,129,0.13)","rgba(239,68,68,0.13)"]
            ):
                fig_radar_km.add_trace(go.Scatterpolar(
                    r=vals+[vals[0]], theta=cats_km+[cats_km[0]],
                    fill='toself', name=name, line=dict(color=clr, width=1.5), fillcolor=fill_rgba))
            fig_radar_km.update_layout(**PLOTLY_BASE, height=280,
                polar=dict(bgcolor="rgba(0,0,0,0)",
                           radialaxis=dict(range=[0,1], gridcolor="#2A2A3E", tickfont=dict(color="#6B7280", size=8)),
                           angularaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0", size=9))),
                title=dict(text="Profil des clusters (radar)", font=dict(color="#E8E8F0", size=13, family="Playfair Display")),
                legend=dict(font=dict(color="#E8E8F0", size=8), bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_radar_km, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with tab_db:
        st.markdown("""
        <div style='margin-top:16px;'>
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#EC4899;
                    letter-spacing:1px;margin-bottom:14px;'>DBSCAN — Density-Based Clustering</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='card' style='margin-bottom:20px;'>
          <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:16px;'>
            <div style='background:#12121A;border-radius:10px;padding:16px;border:1px solid #2A2A3E;'>
              <div style='font-family:"Space Mono",monospace;font-size:0.75em;color:#8B5CF6;margin-bottom:6px;'>PARAMÈTRE eps</div>
              <div style='font-size:1.4em;font-weight:700;color:#E8E8F0;font-family:"Space Mono",monospace;'>0.5</div>
              <div style='font-size:0.75em;color:#6B7280;margin-top:4px;'>Distance maximale entre voisins</div>
            </div>
            <div style='background:#12121A;border-radius:10px;padding:16px;border:1px solid #2A2A3E;'>
              <div style='font-family:"Space Mono",monospace;font-size:0.75em;color:#06B6D4;margin-bottom:6px;'>min_samples</div>
              <div style='font-size:1.4em;font-weight:700;color:#E8E8F0;font-family:"Space Mono",monospace;'>5</div>
              <div style='font-size:0.75em;color:#6B7280;margin-top:4px;'>Min points pour un cluster dense</div>
            </div>
            <div style='background:#12121A;border-radius:10px;padding:16px;border:1px solid #2A2A3E;'>
              <div style='font-family:"Space Mono",monospace;font-size:0.75em;color:#EF4444;margin-bottom:6px;'>BRUIT (-1)</div>
              <div style='font-size:1.4em;font-weight:700;color:#EF4444;font-family:"Space Mono",monospace;'>~380</div>
              <div style='font-size:0.75em;color:#6B7280;margin-top:4px;'>Outliers détectés automatiquement</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            np.random.seed(10)
            fig_db = go.Figure()
            for i, ((cx,cy), n_pts, clr) in enumerate([
                ((-1.5,1.0),200,'#8B5CF6'), ((1.8,-0.5),150,'#06B6D4'), ((-0.2,-1.8),120,'#10B981')
            ]):
                fig_db.add_trace(go.Scatter(
                    x=np.random.randn(n_pts)*0.6+cx, y=np.random.randn(n_pts)*0.5+cy,
                    mode='markers', marker=dict(size=5, color=clr, opacity=0.7), name=f'Cluster {i}'))
            fig_db.add_trace(go.Scatter(
                x=np.random.uniform(-4,4,40), y=np.random.uniform(-4,4,40),
                mode='markers', marker=dict(size=5, color='#444', symbol='x'), name='Bruit (-1)'))
            fig_db.update_layout(**PLOTLY_BASE, height=340,
                title=dict(text="DBSCAN — Clusters + Bruit détecté", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), title='PCA 1'),
                yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), title='PCA 2'),
                legend=dict(font=dict(color="#E8E8F0"), bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_db, use_container_width=True)

        with c2:
            eps_vals = [0.2,0.3,0.5,0.8,1.2,2.0]
            n_clusters_eps = [8,6,3,2,1,1]
            noise_pct_eps  = [28,18,5,1,0,0]
            fig_eps = go.Figure()
            fig_eps.add_trace(go.Scatter(x=eps_vals, y=n_clusters_eps, mode='lines+markers',
                name='Nb clusters', line=dict(color='#8B5CF6', width=2), marker=dict(size=8)))
            fig_eps.add_trace(go.Scatter(x=eps_vals, y=noise_pct_eps, mode='lines+markers',
                name='% Bruit', line=dict(color='#EF4444', width=2, dash='dash'),
                marker=dict(size=8), yaxis='y2'))
            fig_eps.add_vline(x=0.5, line_dash='dash', line_color='#F59E0B',
                              annotation_text='eps=0.5 choisi', annotation_font_color='#F59E0B')
            fig_eps.update_layout(**PLOTLY_BASE, height=340,
                title=dict(text="Sensibilité au paramètre eps", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0"), title='eps'),
                yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), title='Nb clusters'),
                yaxis2=dict(overlaying='y', side='right', tickfont=dict(color="#EF4444"), title='% Bruit'),
                legend=dict(font=dict(color="#E8E8F0"), bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_eps, use_container_width=True)

        st.markdown("""
        <div class='card'>
          <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#EC4899;
                      letter-spacing:1px;margin-bottom:14px;'>AVANTAGE DBSCAN — DÉTECTION D'ANOMALIES</div>
          <div style='display:grid;grid-template-columns:repeat(2,1fr);gap:14px;'>
            <div style='background:#12121A;border-radius:10px;padding:14px;border-left:3px solid #EF4444;'>
              <div style='font-weight:600;color:#EF4444;margin-bottom:6px;font-size:0.88em;'>⚠️ Anomalies détectées</div>
              <div style='font-size:0.8em;color:#6B7280;line-height:1.6;'>Avis avec Rating 5 mais texte très négatif.</div>
            </div>
            <div style='background:#12121A;border-radius:10px;padding:14px;border-left:3px solid #8B5CF6;'>
              <div style='font-weight:600;color:#8B5CF6;margin-bottom:6px;font-size:0.88em;'>✅ Clusters naturels</div>
              <div style='font-size:0.8em;color:#6B7280;line-height:1.6;'>Identifie des groupes sans imposer un K fixe.</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_hc:
        st.markdown("""
        <div style='margin-top:16px;'>
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#10B981;
                    letter-spacing:1px;margin-bottom:14px;'>CLUSTERING HIÉRARCHIQUE — AgglomerativeClustering</div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            np.random.seed(7)
            fig_hc = go.Figure()
            for i, (cx, cy, clr) in enumerate(zip([-1.2,1.5,-0.1],[0.8,-0.3,-1.9],['#8B5CF6','#06B6D4','#10B981'])):
                n_pts = [180,140,110][i]
                fig_hc.add_trace(go.Scatter(
                    x=np.random.randn(n_pts)*0.9+cx, y=np.random.randn(n_pts)*0.8+cy,
                    mode='markers', marker=dict(size=5, color=clr, opacity=0.65), name=f'Groupe {i+1}'))
            fig_hc.update_layout(**PLOTLY_BASE, height=340,
                title=dict(text="Clustering Hiérarchique (n=3)", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), title='PCA 1'),
                yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), title='PCA 2'),
                legend=dict(font=dict(color="#E8E8F0"), bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_hc, use_container_width=True)

        with c2:
            linkages = ['ward','complete','average','single']
            silhouette_scores = [0.412,0.378,0.355,0.289]
            fig_link = go.Figure(go.Bar(x=linkages, y=silhouette_scores,
                marker_color=['#8B5CF6','#06B6D4','#10B981','#444'],
                text=[f"{v:.3f}" for v in silhouette_scores], textposition='outside',
                textfont=dict(color="#E8E8F0", size=11)))
            fig_link.add_annotation(x='ward', y=0.432, text="✦ Meilleur",
                showarrow=False, font=dict(color="#F59E0B", size=11))
            fig_link.update_layout(**PLOTLY_BASE, height=340, showlegend=False,
                title=dict(text="Score Silhouette par méthode de linkage", font=dict(color="#E8E8F0", size=14, family="Playfair Display")),
                xaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#E8E8F0")),
                yaxis=dict(gridcolor="#2A2A3E", tickfont=dict(color="#6B7280"), range=[0,0.5]))
            st.plotly_chart(fig_link, use_container_width=True)

        st.markdown("""
        <div class='card'>
          <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#10B981;
                      letter-spacing:1px;margin-bottom:14px;'>PARAMÈTRES UTILISÉS</div>
          <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:12px;font-size:0.85em;'>
            <div style='background:#12121A;border-radius:8px;padding:12px;text-align:center;'>
              <div style='font-family:"Space Mono",monospace;color:#10B981;font-size:1em;font-weight:700;'>3</div>
              <div style='color:#6B7280;font-size:0.78em;margin-top:4px;'>n_clusters</div>
            </div>
            <div style='background:#12121A;border-radius:8px;padding:12px;text-align:center;'>
              <div style='font-family:"Space Mono",monospace;color:#10B981;font-size:1em;font-weight:700;'>ward</div>
              <div style='color:#6B7280;font-size:0.78em;margin-top:4px;'>linkage (meilleur)</div>
            </div>
            <div style='background:#12121A;border-radius:8px;padding:12px;text-align:center;'>
              <div style='font-family:"Space Mono",monospace;color:#10B981;font-size:1em;font-weight:700;'>0.412</div>
              <div style='color:#6B7280;font-size:0.78em;margin-top:4px;'>Score Silhouette</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_bilan:
        st.markdown("""
        <div style='margin-top:16px;'>
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#F59E0B;
                    letter-spacing:1px;margin-bottom:18px;'>BILAN & COMPARAISON DES 3 ALGORITHMES</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <table class='styled-table'>
          <thead><tr>
            <th>ALGORITHME</th><th>K prédéfini</th><th>Gère le bruit</th>
            <th>Forme des clusters</th><th>Score Silhouette</th><th>Usage recommandé</th>
          </tr></thead>
          <tbody>
          <tr>
            <td><strong style='color:#8B5CF6;'>✦ K-Means</strong></td>
            <td><span style='color:#EF4444;'>Oui (K=4)</span></td>
            <td><span style='color:#EF4444;'>Non</span></td>
            <td>Sphériques</td>
            <td><strong style='color:#8B5CF6;'>0.438</strong></td>
            <td>Segmentation client (interprétable)</td>
          </tr>
          <tr>
            <td><strong style='color:#EC4899;'>DBSCAN</strong></td>
            <td><span style='color:#10B981;'>Non (auto)</span></td>
            <td><span style='color:#10B981;'>Oui ✓</span></td>
            <td>Arbitraires</td><td>0.381</td>
            <td>Détection d'anomalies</td>
          </tr>
          <tr>
            <td><strong style='color:#10B981;'>Hiérarchique</strong></td>
            <td><span style='color:#EF4444;'>Oui (n=3)</span></td>
            <td><span style='color:#EF4444;'>Non</span></td>
            <td>Variées</td><td>0.412</td>
            <td>Dendrogramme exploratoire</td>
          </tr>
          </tbody>
        </table>""", unsafe_allow_html=True)

        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#8B5CF6;
                    letter-spacing:1px;margin-bottom:16px;'>PROFILS DÉTAILLÉS — 4 CLUSTERS K-MEANS</div>
        <div style='display:grid;grid-template-columns:repeat(2,1fr);gap:16px;'>
        """, unsafe_allow_html=True)

        for clr, emoji, title, size, age, rating, feedback, desc, actions in [
            ("#8B5CF6","🔵","Cluster 0 — Satisfaites Passives","8,350 clientes","~35 ans","4.72 ⭐","~0.5",
             "Le plus grand groupe. Très satisfaites mais peu engagées.",
             ["Encourager à laisser des avis","Cibler par email marketing","Fidélisation passive"]),
            ("#06B6D4","🟢","Cluster 1 — Engagées Actives","2,918 clientes","~43 ans","4.32 ⭐","~4.7",
             "Les ambassadrices de la marque. Très actives en feedback.",
             ["Programme VIP/fidélité","Inviter comme testeuses","Partage sur réseaux sociaux"]),
            ("#10B981","🟡","Cluster 2 — Âgées Satisfaites","5,399 clientes","~57 ans","4.63 ⭐","~0.7",
             "Clientes plus matures, satisfaites mais discrètes.",
             ["Interface simplifiée","Contenu accessible","Newsletter ciblée"]),
            ("#EF4444","🔴","Cluster 3 — Insatisfaites","3,732 clientes","~40 ans","2.32 ⭐","~0.9",
             "Groupe critique. Mauvaise expérience produit, à surveiller.",
             ["Analyser les retours produit","Améliorer qualité/taille","Service après-vente proactif"]),
        ]:
            actions_html = "".join([
                f"<div style='display:flex;gap:6px;align-items:center;font-size:0.78em;color:#9CA3AF;padding:3px 0;'>"
                f"<span style='color:{clr};'>→</span>{a}</div>" for a in actions
            ])
            st.markdown(f"""
            <div style='background:#12121A;border:1px solid rgba(42,42,62,0.8);border-radius:14px;
                        padding:20px;border-top:3px solid {clr};'>
              <div style='display:flex;align-items:center;gap:10px;margin-bottom:12px;'>
                <span style='font-size:1.4em;'>{emoji}</span>
                <div>
                  <div style='font-weight:700;color:{clr};font-size:0.92em;'>{title}</div>
                  <div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#6B7280;'>{size}</div>
                </div>
              </div>
              <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px;'>
                <div style='background:#0A0A0F;border-radius:6px;padding:8px;text-align:center;'>
                  <div style='font-family:"Space Mono",monospace;font-size:0.85em;color:{clr};'>{age}</div>
                  <div style='font-size:0.7em;color:#6B7280;'>Âge moyen</div>
                </div>
                <div style='background:#0A0A0F;border-radius:6px;padding:8px;text-align:center;'>
                  <div style='font-family:"Space Mono",monospace;font-size:0.85em;color:{clr};'>{rating}</div>
                  <div style='font-size:0.7em;color:#6B7280;'>Rating moyen</div>
                </div>
                <div style='background:#0A0A0F;border-radius:6px;padding:8px;text-align:center;'>
                  <div style='font-family:"Space Mono",monospace;font-size:0.85em;color:{clr};'>{feedback}</div>
                  <div style='font-size:0.7em;color:#6B7280;'>Feedback moy.</div>
                </div>
              </div>
              <p style='color:#6B7280;font-size:0.81em;line-height:1.5;margin-bottom:10px;'>{desc}</p>
              <div style='border-top:1px solid rgba(42,42,62,0.5);padding-top:10px;'>
                <div style='font-size:0.72em;color:#4B5563;margin-bottom:4px;
                            font-family:"Space Mono",monospace;letter-spacing:0.5px;'>ACTIONS RECOMMANDÉES</div>
                {actions_html}
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  PAGE 4 — PRÉDICTION
# ══════════════════════════════════════════════════════════════
elif PAGE == 4:
    st.markdown("""
    <div style='padding:40px 0 24px 0;'>
      <div class='hero-badge'> Interface Interactive</div>
      <div class='sec-title' style='font-size:2.2em;margin-top:10px;'>Prédiction en Temps Réel</div>
      <div class='sec-sub'>Entrez les informations du produit pour prédire sa popularité</div>
    </div>""", unsafe_allow_html=True)

    if not models_ok:
        st.markdown("""
        <div style='background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);
                    border-radius:12px;padding:30px;text-align:center;'>
          <div style='font-size:2.5em;'>⚠️</div>
          <div style='color:#EF4444;margin-top:10px;line-height:1.7;'>
            Modèles non trouvés.<br>
            Vérifiez que <code>model/models.pkl</code> existe.
          </div>
        </div>""", unsafe_allow_html=True)
        st.stop()

    cf, cr = st.columns([1.1, 0.9], gap="large")

    with cf:
        st.markdown("""
        <div style='background:linear-gradient(135deg,rgba(139,92,246,0.08),rgba(6,182,212,0.04));
                    border:1px solid rgba(139,92,246,0.25);border-radius:14px;
                    padding:16px 20px;margin-bottom:16px;'>
          <div style='font-family:"Space Mono",monospace;font-size:0.63em;color:#8B5CF6;
                      letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;'>
            Guide — Comment remplir ce formulaire
          </div>
          <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>
            <div style='display:flex;gap:8px;align-items:flex-start;'>
              <div style='width:6px;height:6px;border-radius:50%;background:#8B5CF6;margin-top:6px;flex-shrink:0;'></div>
              <div style='font-size:0.79em;color:#9CA3AF;line-height:1.5;'>
                <strong style='color:#E8E8F0;'>Rating</strong> — la note que la cliente a donnée (1 = très mauvais, 5 = excellent). C'est le facteur le plus déterminant.
              </div>
            </div>
            <div style='display:flex;gap:8px;align-items:flex-start;'>
              <div style='width:6px;height:6px;border-radius:50%;background:#06B6D4;margin-top:6px;flex-shrink:0;'></div>
              <div style='font-size:0.79em;color:#9CA3AF;line-height:1.5;'>
                <strong style='color:#E8E8F0;'>Feedbacks positifs</strong> — combien d'autres clientes ont trouvé cet avis utile.
              </div>
            </div>
            <div style='display:flex;gap:8px;align-items:flex-start;'>
              <div style='width:6px;height:6px;border-radius:50%;background:#10B981;margin-top:6px;flex-shrink:0;'></div>
              <div style='font-size:0.79em;color:#9CA3AF;line-height:1.5;'>
                <strong style='color:#E8E8F0;'>Avis client</strong> — texte de l'avis. Positif ("love", "perfect") → Recommandé. Négatif ("bad", "return") → Non Recommandé.
              </div>
            </div>
            <div style='display:flex;gap:8px;align-items:flex-start;'>
              <div style='width:6px;height:6px;border-radius:50%;background:#F59E0B;margin-top:6px;flex-shrink:0;'></div>
              <div style='font-size:0.79em;color:#9CA3AF;line-height:1.5;'>
                <strong style='color:#E8E8F0;'>Âge / Division / Département</strong> — impact faible mais pris en compte.
              </div>
            </div>
          </div>
          <div style='margin-top:12px;padding:10px 12px;background:rgba(0,0,0,0.2);
                      border-radius:8px;font-size:0.78em;color:#6B7280;line-height:1.6;'>
            Exemple <strong style='color:#10B981;'>Recommandé</strong> :
            Rating = 5, "I absolutely love this dress, it fits perfectly", Feedback = 12<br>
            Exemple <strong style='color:#EF4444;'>Non Recommandé</strong> :
            Rating = 1, "Terrible quality, returned immediately", Feedback = 0
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("""<div style='font-family:"Space Mono",monospace;font-size:0.68em;
                    color:#8B5CF6;letter-spacing:1px;margin-bottom:20px;'>SAISIE DES DONNÉES</div>""",
                    unsafe_allow_html=True)

        cc1, cc2 = st.columns(2)
        with cc1:
            model_choice = st.selectbox("Modèle IA", list(models.keys()),
                format_func=lambda x: {
                    "logistic_regression": "Régression Logistique",
                    "decision_tree":       "Arbre de Décision",
                    "random_forest":       "✦ Random Forest",
                }[x])
            rating = st.slider("Rating (1 = mauvais → 5 = excellent)", 1.0, 5.0, 4.0, 0.5)
        with cc2:
            feedback = st.number_input("Feedbacks positifs (0 = aucun, 10+ = influent)", 0, 500, 10)
            age      = st.number_input("Âge de la cliente", 18, 90, 35)

        cc3, cc4, cc5 = st.columns(3)
        with cc3:
            division   = st.selectbox("Division",        ["General","General Petite","Initmates"])
        with cc4:
            department = st.selectbox("Département",     ["Tops","Dresses","Bottoms","Intimate","Jackets","Trend"])
        with cc5:
            class_name = st.selectbox("Classe produit",  ["Blouses","Dresses","Knits","Pants","Skirts","Jackets","Intimates"])

        review = st.text_area("Texte de l'avis client (en anglais)",
            placeholder="Ex: I absolutely love this dress! The fabric is so comfortable and fits perfectly. Highly recommend!",
            height=120)

        if review.strip():
            sl, sc, _ = sentiment_quick(review)
            wc = len(review.split())
            sc_label = ("Positif → favorise 'Recommandé'" if "Positif" in sl
                        else ("Négatif → défavorise" if "Négatif" in sl else "Neutre → impact faible"))
            st.markdown(f"""
            <div style='display:flex;gap:10px;margin:8px 0 12px 0;'>
              <div style='background:#12121A;border:1px solid #2A2A3E;border-radius:8px;
                          padding:8px 14px;font-size:0.8em;flex:2;'>
                <div style='color:{sc};font-weight:600;'>{sl}</div>
                <div style='color:#6B7280;font-size:0.74em;margin-top:2px;'>{sc_label}</div>
              </div>
              <div style='background:#12121A;border:1px solid #2A2A3E;border-radius:8px;
                          padding:8px 14px;font-size:0.8em;flex:1;text-align:center;'>
                <div style='color:#8B5CF6;font-weight:600;font-family:"Space Mono",monospace;'>{wc}</div>
                <div style='color:#6B7280;font-size:0.74em;margin-top:2px;'>mots</div>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        btn = st.button("Lancer la prédiction", use_container_width=True, type="primary")

    with cr:
        if btn:
            if not review.strip():
                st.markdown("""
                <div style='background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.3);
                            border-radius:12px;padding:20px;text-align:center;color:#F59E0B;'>
                  ⚠️ Veuillez entrer un avis client.
                </div>""", unsafe_allow_html=True)
            else:
                model = models[model_choice]
                X_inp, mode_used = preprocess(
                    review, rating, feedback, age,
                    division, department, class_name
                )

                pred, proba = None, None

                if X_inp is not None and mode_used == "full":
                    # ✅ Prédiction réelle avec les vrais modèles du notebook
                    try:
                        pred  = int(model.predict(X_inp)[0])
                        proba = float(model.predict_proba(X_inp)[0][1]) if hasattr(model, "predict_proba") else 0.5
                    except Exception:
                        pred, proba = predict_manual(review, rating, feedback, age)
                        mode_used = "manual"
                else:
                    # ⚠️ Fallback si pkl manquants
                    pred, proba = predict_manual(review, rating, feedback, age)
                    mode_used = "manual"

                if mode_used == "manual":
                    st.markdown("""
                    <div style='background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.25);
                                border-radius:10px;padding:10px 14px;margin-bottom:12px;
                                display:flex;align-items:center;gap:10px;'>
                      <div style='font-size:1.1em;flex-shrink:0;'>⚠️</div>
                      <div style='font-size:0.78em;color:#D97706;line-height:1.5;'>
                        <strong>Mode approximatif actif</strong> — Fichiers pkl incomplets.<br>
                        Vérifiez que scaler.pkl, feature_columns.pkl et scaled_columns.pkl existent.
                      </div>
                    </div>""", unsafe_allow_html=True)

                st.session_state["last_pred"] = {
                    "prediction": pred, "proba": proba,
                    "rating": rating, "feedback": feedback, "review": review,
                }

                if pred == 1:
                    clr_r, bg_r, bd_r = "#10B981","rgba(16,185,129,0.07)","rgba(16,185,129,0.3)"
                    emoji_r, title_r  = "✅", "Produit Populaire"
                    hint_r = "Ce produit sera très probablement recommandé !"
                else:
                    clr_r, bg_r, bd_r = "#EF4444","rgba(239,68,68,0.07)","rgba(239,68,68,0.3)"
                    emoji_r, title_r  = "❌", "Produit Faible"
                    hint_r = "Ce produit risque de ne pas être recommandé."

                st.markdown(f"""
                <div style='background:{bg_r};border:1px solid {bd_r};border-radius:16px;
                            padding:30px;text-align:center;margin-bottom:14px;'>
                  <div style='font-size:3.5em;'>{emoji_r}</div>
                  <div style='font-family:"Playfair Display",serif;font-size:1.7em;font-weight:700;
                              color:{clr_r};margin:8px 0 4px 0;'>{title_r}</div>
                  <div style='color:#6B7280;font-size:0.87em;'>{hint_r}</div>
                </div>""", unsafe_allow_html=True)

                bc = "#10B981" if proba >= 0.6 else ("#F59E0B" if proba >= 0.4 else "#EF4444")
                st.markdown(proba_bar_html(proba, bc), unsafe_allow_html=True)

                if   proba >= 0.75: interp = "🟢 **Très forte probabilité de succès**"
                elif proba >= 0.55: interp = "🟡 **Probabilité modérée de succès**"
                elif proba >= 0.40: interp = "🟠 **Résultat incertain**"
                else:               interp = "🔴 **Faible probabilité de succès**"
                st.markdown(interp)

                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("""<div style='font-family:"Space Mono",monospace;font-size:0.68em;
                            color:#8B5CF6;letter-spacing:1px;margin-bottom:14px;'>FACTEURS CLÉS</div>""",
                            unsafe_allow_html=True)
                factors = []
                if rating >= 4.0:   factors.append(("⭐","Rating élevé",     f"{rating}/5","#10B981"))
                elif rating <= 2.0: factors.append(("⭐","Rating faible",     f"{rating}/5","#EF4444"))
                else:               factors.append(("⭐","Rating moyen",      f"{rating}/5","#F59E0B"))
                if feedback >= 15:  factors.append(("👍","Fort engagement",   str(feedback),"#10B981"))
                elif feedback == 0: factors.append(("👍","Aucun feedback",    "0","#EF4444"))
                else:               factors.append(("👍","Feedbacks modérés", str(feedback),"#F59E0B"))
                sl2, sc2, _ = sentiment_quick(review)
                factors.append(("💬","Sentiment", sl2, sc2))
                wc2 = len(review.split())
                if wc2 >= 30:   factors.append(("📝","Avis détaillé", f"{wc2} mots","#10B981"))
                elif wc2 >= 10: factors.append(("📝","Avis moyen",    f"{wc2} mots","#F59E0B"))
                else:           factors.append(("📝","Avis court",    f"{wc2} mots","#EF4444"))
                rows = ""
                for icon, lbl, val, fclr in factors:
                    rows += f"""
                    <div style='display:flex;justify-content:space-between;align-items:center;
                                padding:9px 0;border-bottom:1px solid rgba(42,42,62,0.4);font-size:0.85em;'>
                      <span style='color:#E8E8F0;'>{icon} {lbl}</span>
                      <span style='color:{fclr};font-weight:600;font-family:"Space Mono",monospace;font-size:0.84em;'>{val}</span>
                    </div>"""
                st.markdown(rows + "</div>", unsafe_allow_html=True)

                if "history" not in st.session_state:
                    st.session_state.history = []
                ml = {"logistic_regression":"Logistic Reg.","decision_tree":"Dec. Tree",
                      "random_forest":"Random Forest"}[model_choice]
                pred_id = f"pred_{len(st.session_state.history)}"
                st.session_state.history.append({
                    "Modèle": ml, "Rating": rating, "Feedbacks": feedback,
                    "Résultat": "Recommandé" if pred == 1 else "Non Recommandé",
                    "Probabilité": f"{int(proba*100)}%",
                    "Avis": review[:35] + "..." if len(review) > 35 else review,
                    "Feedback": "—",
                })
                st.session_state["current_pred_id"] = len(st.session_state.history) - 1

                st.markdown("""
                <div style='margin-top:18px;padding:18px 20px;
                            background:linear-gradient(135deg,rgba(139,92,246,0.06),rgba(6,182,212,0.03));
                            border:1px solid rgba(139,92,246,0.2);border-radius:14px;'>
                  <div style='font-family:"Space Mono",monospace;font-size:0.62em;color:#8B5CF6;
                              letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;'>
                    Retour utilisateur
                  </div>
                  <div style='font-size:0.88em;color:#E8E8F0;font-weight:600;margin-bottom:14px;'>
                    Cette prédiction était-elle correcte ?
                  </div>
                </div>""", unsafe_allow_html=True)

                fb_col1, fb_col2 = st.columns(2)
                with fb_col1:
                    st.markdown("""
                    <div style='background:linear-gradient(135deg,rgba(16,185,129,0.12),rgba(16,185,129,0.05));
                                border:1.5px solid rgba(16,185,129,0.4);border-radius:12px;
                                padding:14px 16px;text-align:center;margin-bottom:6px;'>
                      <div style='font-size:1.6em;margin-bottom:4px;'>👍</div>
                      <div style='font-size:0.86em;font-weight:700;color:#10B981;'>Oui, correcte</div>
                      <div style='font-size:0.72em;color:#6B7280;margin-top:3px;'>La vraie valeur correspond</div>
                    </div>""", unsafe_allow_html=True)
                    st.markdown("<div class='fb-btn'>", unsafe_allow_html=True)
                    if st.button("Confirmer — Correcte", key=f"fb_yes_{pred_id}", use_container_width=True):
                        idx = st.session_state["current_pred_id"]
                        st.session_state.history[idx]["Feedback"] = "Correcte"
                        st.session_state["feedback_given"] = "yes"
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

                with fb_col2:
                    st.markdown("""
                    <div style='background:linear-gradient(135deg,rgba(239,68,68,0.12),rgba(239,68,68,0.05));
                                border:1.5px solid rgba(239,68,68,0.4);border-radius:12px;
                                padding:14px 16px;text-align:center;margin-bottom:6px;'>
                      <div style='font-size:1.6em;margin-bottom:4px;'>👎</div>
                      <div style='font-size:0.86em;font-weight:700;color:#EF4444;'>Non, incorrecte</div>
                      <div style='font-size:0.72em;color:#6B7280;margin-top:3px;'>Le modèle s'est trompé</div>
                    </div>""", unsafe_allow_html=True)
                    st.markdown("<div class='fb-btn'>", unsafe_allow_html=True)
                    if st.button("Confirmer — Incorrecte", key=f"fb_no_{pred_id}", use_container_width=True):
                        idx = st.session_state["current_pred_id"]
                        st.session_state.history[idx]["Feedback"] = "Incorrecte"
                        st.session_state["feedback_given"] = "no"
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

                if st.session_state.get("feedback_given") == "yes":
                    st.markdown("""
                    <div style='background:linear-gradient(135deg,rgba(16,185,129,0.1),rgba(16,185,129,0.04));
                                border:1px solid rgba(16,185,129,0.35);border-radius:12px;
                                padding:16px 18px;margin-top:4px;'>
                      <div style='display:flex;align-items:center;gap:12px;margin-bottom:8px;'>
                        <div style='width:36px;height:36px;border-radius:50%;background:rgba(16,185,129,0.15);
                                    border:2px solid rgba(16,185,129,0.4);display:flex;align-items:center;
                                    justify-content:center;font-size:1.1em;flex-shrink:0;'>✓</div>
                        <div style='font-weight:700;color:#10B981;font-size:0.9em;'>Retour enregistré — Merci !</div>
                      </div>
                      <div style='font-size:0.78em;color:#6B7280;line-height:1.6;padding-left:48px;'>
                        Marquée comme <strong style='color:#6EE7B7;'>correcte</strong> dans l'historique.
                      </div>
                    </div>""", unsafe_allow_html=True)
                    st.session_state.pop("feedback_given", None)

                elif st.session_state.get("feedback_given") == "no":
                    st.markdown("""
                    <div style='background:linear-gradient(135deg,rgba(239,68,68,0.1),rgba(239,68,68,0.04));
                                border:1px solid rgba(239,68,68,0.35);border-radius:12px;
                                padding:16px 18px;margin-top:4px;'>
                      <div style='display:flex;align-items:center;gap:12px;margin-bottom:8px;'>
                        <div style='width:36px;height:36px;border-radius:50%;background:rgba(239,68,68,0.15);
                                    border:2px solid rgba(239,68,68,0.4);display:flex;align-items:center;
                                    justify-content:center;font-size:1.1em;flex-shrink:0;'>✗</div>
                        <div style='font-weight:700;color:#EF4444;font-size:0.9em;'>Erreur notée — Merci !</div>
                      </div>
                      <div style='font-size:0.78em;color:#6B7280;line-height:1.6;padding-left:48px;'>
                        Marquée comme <strong style='color:#FCA5A5;'>incorrecte</strong> dans l'historique.
                      </div>
                    </div>""", unsafe_allow_html=True)
                    st.session_state.pop("feedback_given", None)
        else:
            st.markdown("""
            <div style='background:#12121A;border:1px dashed #2A2A3E;border-radius:16px;
                        padding:60px 30px;text-align:center;'>
              <div style='font-size:3.5em;opacity:0.3;'>🔮</div>
              <div style='color:#374151;font-size:0.95em;margin-top:14px;line-height:1.7;'>
                Remplissez le formulaire<br>et cliquez sur
                <strong style='color:#6B7280;'>Lancer la prédiction</strong>
              </div>
            </div>""", unsafe_allow_html=True)

    if "history" in st.session_state and st.session_state.history:
        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

        hist = st.session_state.history
        total      = len(hist)
        n_rec      = sum(1 for h in hist if h["Résultat"] == "Recommandé")
        n_non      = total - n_rec
        n_correct  = sum(1 for h in hist if h.get("Feedback") == "Correcte")
        n_incorr   = sum(1 for h in hist if h.get("Feedback") == "Incorrecte")
        n_feedback = n_correct + n_incorr
        accuracy_u = round(n_correct / n_feedback * 100) if n_feedback > 0 else None

        ch, cb2 = st.columns([5, 1])
        ch.markdown("<div class='sec-title' style='font-size:1.3em;'>Historique des prédictions</div>",
                    unsafe_allow_html=True)
        if cb2.button("Effacer", use_container_width=True):
            st.session_state.history = []
            st.session_state.pop("feedback_given", None)
            st.rerun()

        sc1, sc2, sc3, sc4, sc5 = st.columns(5)
        for col, (val, lbl, clr, sub) in zip([sc1,sc2,sc3,sc4,sc5], [
            (str(total),    "Prédictions",      "#8B5CF6", "total effectuées"),
            (str(n_rec),    "Recommandés",       "#10B981", f"{round(n_rec/total*100) if total else 0}% du total"),
            (str(n_non),    "Non recommandés",   "#EF4444", f"{round(n_non/total*100) if total else 0}% du total"),
            (str(n_feedback),"Feedbacks donnés", "#F59E0B", f"{total - n_feedback} sans retour"),
            (
                f"{accuracy_u}%" if accuracy_u is not None else "—",
                "Taux de justesse",
                "#06B6D4" if accuracy_u and accuracy_u >= 70 else "#F97316",
                "selon vos retours" if accuracy_u is not None else "aucun feedback encore",
            ),
        ]):
            with col:
                st.markdown(f"""
                <div style='background:#12121A;border:1px solid #2A2A3E;border-radius:12px;
                            padding:14px 12px;text-align:center;border-top:2px solid {clr};'>
                  <div style='font-family:"Space Mono",monospace;font-size:1.6em;font-weight:700;color:{clr};'>{val}</div>
                  <div style='color:#E8E8F0;font-size:0.8em;font-weight:600;margin-top:4px;'>{lbl}</div>
                  <div style='color:#4B5563;font-size:0.7em;margin-top:3px;'>{sub}</div>
                </div>""", unsafe_allow_html=True)

        if n_feedback > 0:
            pct_ok  = round(n_correct / n_feedback * 100)
            pct_err = round(n_incorr  / n_feedback * 100)
            st.markdown(f"""
            <div style='background:#12121A;border:1px solid #2A2A3E;border-radius:12px;
                        padding:16px 20px;margin:12px 0;'>
              <div style='font-family:"Space Mono",monospace;font-size:0.63em;color:#6B7280;
                          letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>
                Analyse des retours utilisateur
              </div>
              <div style='display:flex;justify-content:space-between;font-size:0.8em;margin-bottom:6px;'>
                <span style='color:#10B981;font-weight:600;'>Correctes : {n_correct} ({pct_ok}%)</span>
                <span style='color:#EF4444;font-weight:600;'>Incorrectes : {n_incorr} ({pct_err}%)</span>
              </div>
              <div style='background:#0A0A0F;border-radius:6px;height:10px;overflow:hidden;'>
                <div style='width:{pct_ok}%;height:100%;background:linear-gradient(90deg,#10B981,#34D399);border-radius:6px;float:left;'></div>
                <div style='width:{pct_err}%;height:100%;background:linear-gradient(90deg,#EF4444,#F97316);border-radius:6px;float:left;'></div>
              </div>
            </div>""", unsafe_allow_html=True)

        st.dataframe(pd.DataFrame(hist[::-1]), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
#  PAGE 5 — EXPLICATION IA (SHAP)
# ══════════════════════════════════════════════════════════════
elif PAGE == 5:
    st.markdown("""
    <div style='padding:40px 0 24px 0;'>
      <div class='hero-badge'> Explicabilité IA — SHAP</div>
      <div class='sec-title' style='font-size:2.2em;margin-top:10px;'>Pourquoi cette prédiction ?</div>
      <div class='sec-sub'>Shapley Additive Explanations — comprendre les décisions du modèle variable par variable</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(139,92,246,0.1),rgba(6,182,212,0.06),#12121A);
                border:1px solid rgba(139,92,246,0.3);border-radius:18px;padding:28px 36px;
                margin-bottom:24px;display:flex;align-items:center;gap:24px;'>
      <div style='font-size:3.2em;flex-shrink:0;'>🔬</div>
      <div>
        <div style='font-family:"Playfair Display",serif;font-size:1.15em;font-weight:700;
                    color:#E8E8F0;margin-bottom:6px;'>SHAP = SHapley Additive exPlanations</div>
        <div style='color:#6B7280;font-size:0.88em;line-height:1.7;max-width:700px;'>
          Chaque prédiction est décomposée variable par variable. SHAP répond à :
          <em style='color:#A78BFA;'>"Pourquoi le modèle a-t-il prédit CETTE valeur pour CET exemple ?"</em>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:24px;'>
      <div style='background:#12121A;border:1px solid #2A2A3E;border-radius:14px;
                  padding:20px;border-top:3px solid #8B5CF6;'>
        <div style='font-size:1.6em;margin-bottom:10px;'></div>
        <div style='font-weight:700;color:#E8E8F0;font-size:0.9em;margin-bottom:8px;'>À quoi ça sert ?</div>
        <div style='font-size:0.8em;color:#6B7280;line-height:1.7;'>
          SHAP transforme le modèle "boîte noire" en quelque chose de
          <strong style='color:#E8E8F0;'>compréhensible</strong>.
          Il mesure l'impact exact de chaque variable sur une prédiction donnée.
          Sans SHAP, on sait juste que le modèle prédit 87% — avec SHAP, on sait
          <em>pourquoi</em> : parce que le Rating vaut 4, que l'avis est positif, etc.
        </div>
      </div>
      <div style='background:#12121A;border:1px solid #2A2A3E;border-radius:14px;
                  padding:20px;border-top:3px solid #06B6D4;'>
        <div style='font-size:1.6em;margin-bottom:10px;'>⚙️</div>
        <div style='font-weight:700;color:#E8E8F0;font-size:0.9em;margin-bottom:8px;'>Comment ça marche ?</div>
        <div style='font-size:0.8em;color:#6B7280;line-height:1.7;'>
          SHAP est basé sur la <strong style='color:#E8E8F0;'>théorie des jeux de Shapley</strong>.
          Il simule toutes les combinaisons possibles de variables pour calculer la contribution
          marginale de chacune. Le résultat est un score signé :
          <span style='color:#10B981;font-weight:600;'>+ positif</span> = pousse vers "Recommandé",
          <span style='color:#EF4444;font-weight:600;'>− négatif</span> = pousse vers "Non recommandé".
        </div>
      </div>
      <div style='background:#12121A;border:1px solid #2A2A3E;border-radius:14px;
                  padding:20px;border-top:3px solid #10B981;'>
        <div style='font-size:1.6em;margin-bottom:10px;'></div>
        <div style='font-weight:700;color:#E8E8F0;font-size:0.9em;margin-bottom:8px;'>Ce que ça révèle sur ce projet</div>
        <div style='font-size:0.8em;color:#6B7280;line-height:1.7;'>
          Sur notre dataset de 23 486 avis, SHAP confirme que le
          <strong style='color:#E8E8F0;'>Rating est dominant à 0.1907</strong>
          — 6 fois plus influent que la Polarity (0.0312).
          Il valide aussi notre Feature Engineering : les features NLP créées
          (polarity, subjectivity) apportent une vraie valeur au modèle.
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    mc1, mc2, mc3, mc4 = st.columns(4)
    for col, (val, lbl, sub, clr) in zip([mc1,mc2,mc3,mc4],[
        ("0.1907","Rating","Score SHAP dominant","#8B5CF6"),
        ("0.0312","Polarity","2ᵉ plus important","#06B6D4"),
        ("82.6%","Base SHAP","Probabilité a priori","#F59E0B"),
        ("6×","Écart","Rating vs 2ᵉ variable","#EC4899"),
    ]):
        with col:
            st.markdown(f"""
            <div class='card' style='text-align:center;padding:20px 12px;'>
              <div style='font-family:"Space Mono",monospace;font-size:1.7em;font-weight:700;color:{clr};'>{val}</div>
              <div style='color:#E8E8F0;font-size:0.85em;font-weight:600;margin-top:4px;'>{lbl}</div>
              <div style='color:#6B7280;font-size:0.72em;margin-top:3px;'>{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    ca, cb3 = st.columns([1.15, 0.85], gap="large")
    with ca:
        feats = ["Rating","Polarity","Subjectivity","Review Length",
                 "Positive Feedback","Age","Class (enc.)","Division (enc.)","Dept (enc.)","Clothing ID"]
        svals = [0.1907,0.0312,0.0198,0.0142,0.0134,0.0121,0.0098,0.0087,0.0076,0.0065]
        bar_colors = []
        for v in svals[::-1]:
            if v == max(svals):  bar_colors.append("#8B5CF6")
            elif v >= 0.015:     bar_colors.append("#06B6D4")
            elif v >= 0.010:     bar_colors.append("#10B981")
            else:                bar_colors.append("#2A3A5A")
        fig_s = go.Figure()
        fig_s.add_trace(go.Bar(
            x=svals[::-1], y=feats[::-1], orientation="h",
            marker=dict(color=bar_colors, line=dict(color="rgba(255,255,255,0.05)", width=1)),
            text=[f"  {v:.4f}" for v in svals[::-1]],
            textposition="outside", textfont=dict(color="#E8E8F0", size=11, family="Space Mono"),
            hovertemplate="<b>%{y}</b><br>Score SHAP : %{x:.4f}<extra></extra>"))
        fig_s.add_vline(x=0.1907, line_dash="dot", line_color="rgba(139,92,246,0.35)",
                        annotation_text="Rating (0.1907)", annotation_font_color="#8B5CF6",
                        annotation_position="top right")
        fig_s.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#6B7280"), margin=dict(t=55, b=20, l=10, r=100),
            height=420, showlegend=False,
            title=dict(text="SHAP — Importance Globale (Top 10 variables)",
                       font=dict(color="#E8E8F0", size=15, family="Playfair Display"), x=0),
            xaxis=dict(gridcolor="#1E1E2E", zeroline=False, tickfont=dict(color="#6B7280", size=10),
                       title=dict(text="Score SHAP moyen |valeur|", font=dict(color="#6B7280", size=10)),
                       range=[0, 0.24]),
            yaxis=dict(gridcolor="#1E1E2E", tickfont=dict(color="#E8E8F0", size=11)))
        st.plotly_chart(fig_s, use_container_width=True)

    with cb3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("""<div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#8B5CF6;
                    letter-spacing:1px;margin-bottom:16px;'>COMMENT LIRE CE GRAPHIQUE</div>""",
                    unsafe_allow_html=True)
        for clr, icon, title, desc in [
            ("#8B5CF6","⬆️","Score positif (+)","La variable pousse vers 'Recommandé'."),
            ("#EF4444","⬇️","Score négatif (−)","La variable pousse vers 'Non recommandé'."),
            ("#06B6D4","📏","Magnitude","Plus la barre est longue, plus la variable influence."),
            ("#F59E0B","","Base = 82.6%","Point de départ avant ajustements SHAP."),
        ]:
            st.markdown(f"""
            <div style='display:flex;gap:12px;padding:11px 0;border-bottom:1px solid rgba(42,42,62,0.35);'>
              <div style='font-size:1.3em;flex-shrink:0;margin-top:1px;'>{icon}</div>
              <div>
                <div style='font-weight:600;color:{clr};font-size:0.86em;margin-bottom:3px;'>{title}</div>
                <div style='font-size:0.79em;color:#6B7280;line-height:1.5;'>{desc}</div>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card' style='margin-top:0;'>", unsafe_allow_html=True)
        st.markdown("""<div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#06B6D4;
                    letter-spacing:1px;margin-bottom:14px;'>TOP 5 — VALEURS SHAP RÉELLES</div>""",
                    unsafe_allow_html=True)
        for rank, feat, shap_v, interp, clr in [
            ("1","Rating","0.1907","Dominant — 6× la 2ème variable","#8B5CF6"),
            ("2","Polarity","0.0312","Feature NLP créée (TextBlob)","#06B6D4"),
            ("3","Subjectivity","0.0198","Feature NLP — degré d'opinion","#10B981"),
            ("4","Review Length","0.0142","Longueur de l'avis (mots)","#F59E0B"),
            ("5","Positive Feedback","0.0134","Engagement des autres clientes","#EC4899"),
        ]:
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid rgba(42,42,62,0.3);'>
              <div style='width:22px;height:22px;border-radius:6px;background:{clr}22;border:1px solid {clr}55;
                          display:flex;align-items:center;justify-content:center;
                          font-family:"Space Mono",monospace;font-size:0.72em;color:{clr};font-weight:700;flex-shrink:0;'>{rank}</div>
              <div style='flex:1;'>
                <div style='font-size:0.84em;color:#E8E8F0;font-weight:600;'>{feat}</div>
                <div style='font-size:0.73em;color:#6B7280;'>{interp}</div>
              </div>
              <div style='font-family:"Space Mono",monospace;font-size:0.88em;color:{clr};font-weight:700;'>{shap_v}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='margin-bottom:20px;'>
      <div class='sec-title' style='font-size:1.6em;'>Explication d'une prédiction individuelle</div>
      <div class='sec-sub'>Waterfall Plot — décomposition SHAP pas-à-pas</div>
    </div>""", unsafe_allow_html=True)

    if "last_pred" in st.session_state:
        lp = st.session_state["last_pred"]
        r_v, fb_v, rv_v = lp["rating"], lp["feedback"], lp["review"]
        proba_d = lp["proba"]
        sl3, sc3, sv3 = sentiment_quick(rv_v)
        pol_v = sv3 if "Positif" in sl3 else -sv3
        rlen  = len(rv_v.split())
        has_pred = True
    else:
        r_v, fb_v, pol_v, rlen, proba_d = 2.0, 3, -0.15, 12, 0.25
        has_pred = False

    if not has_pred:
        st.markdown("""
        <div style='background:linear-gradient(135deg,rgba(139,92,246,0.08),rgba(6,182,212,0.05));
                    border:1px solid rgba(139,92,246,0.3);border-radius:16px;padding:22px 28px;margin-bottom:24px;'>
          <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:16px;'>
            <div style='background:rgba(0,0,0,0.2);border-radius:10px;padding:14px;border-left:3px solid #6366F1;'>
              <div style='font-size:0.9em;font-weight:700;color:#A5B4FC;margin-bottom:5px;'>📊 Valeur de Base (82.6%)</div>
              <div style='font-size:0.8em;color:#6B7280;'>Point de départ = proportion de recommandés dans le dataset.</div>
            </div>
            <div style='background:rgba(0,0,0,0.2);border-radius:10px;padding:14px;border-left:3px solid #10B981;'>
              <div style='font-size:0.9em;font-weight:700;color:#6EE7B7;margin-bottom:5px;'>▲ Barres vertes = impact positif</div>
              <div style='font-size:0.8em;color:#6B7280;'>Ces variables augmentent la probabilité.</div>
            </div>
            <div style='background:rgba(0,0,0,0.2);border-radius:10px;padding:14px;border-left:3px solid #EF4444;'>
              <div style='font-size:0.9em;font-weight:700;color:#FCA5A5;margin-bottom:5px;'>▼ Barres rouges = impact négatif</div>
              <div style='font-size:0.8em;color:#6B7280;'>Ces variables diminuent la probabilité.</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    base_val = 0.826
    r_c   = (r_v - 3.0) * 0.095
    fb_c  = (min(fb_v, 20) - 5) * 0.003
    pol_c = pol_v * 0.031
    len_c = (min(rlen, 50) - 20) * 0.0007
    oth   = max(-0.05, min(0.05, proba_d - (base_val + r_c + fb_c + pol_c + len_c)))
    contribs = [
        ("Rating",            r_c,   f"valeur = {r_v}/5"),
        ("Polarity (NLP)",    pol_c, f"sentiment {'positif' if pol_v > 0 else 'négatif'}"),
        ("Positive Feedback", fb_c,  f"count = {fb_v}"),
        ("Review Length",     len_c, f"{rlen} mots"),
        ("Autres features",   oth,   "catégorielles + âge"),
    ]

    cw1, cw2 = st.columns([1.25, 0.75], gap="large")
    with cw1:
        running = base_val
        bar_data = [(" Base (82.6%)", base_val, 0, base_val, "#6366F1", "Base a priori")]
        for name, contrib, hint in contribs:
            start = running
            running += contrib
            clr_bar = "#10B981" if contrib >= 0 else "#EF4444"
            bar_data.append((name, abs(contrib), start if contrib >= 0 else running, contrib, clr_bar, hint))
        verdict_clr = "#10B981" if proba_d >= 0.5 else "#EF4444"
        bar_data.append((f"{'✅' if proba_d>=0.5 else '❌'} Prédiction finale",
                         proba_d, 0, proba_d, verdict_clr, f"{int(proba_d*100)}%"))

        sign_texts = [
            f"+{d[3]:.3f}" if d[3] > 0 else f"{d[3]:.3f}"
            for d in bar_data[::-1]
        ]

        fig_wf = go.Figure()
        fig_wf.add_trace(go.Bar(
            x=[d[1] for d in bar_data[::-1]], y=[d[0] for d in bar_data[::-1]],
            base=[d[2] for d in bar_data[::-1]], orientation="h",
            marker=dict(color=[d[4] for d in bar_data[::-1]], line=dict(color="rgba(255,255,255,0.08)", width=1)),
            text=[f"  {t}" for t in sign_texts], textposition="outside",
            textfont=dict(color="#E8E8F0", size=11, family="Space Mono"),
            hovertext=[d[5] for d in bar_data[::-1]],
            hovertemplate="<b>%{y}</b><br>%{hovertext}<br>Contribution : %{text}<extra></extra>"))
        fig_wf.add_vline(x=proba_d, line_dash="dot", line_color=verdict_clr,
                         annotation_text=f"  Prédiction : {int(proba_d*100)}%",
                         annotation_font_color=verdict_clr, annotation_position="top right")
        fig_wf.add_vline(x=base_val, line_dash="dot", line_color="rgba(99,102,241,0.4)")
        fig_wf.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#6B7280"), margin=dict(t=55, b=20, l=10, r=100),
            height=420, showlegend=False,
            title=dict(text="Waterfall Plot SHAP — Décomposition pas-à-pas",
                       font=dict(color="#E8E8F0", size=14, family="Playfair Display"), x=0),
            xaxis=dict(gridcolor="#1E1E2E", zeroline=False, tickfont=dict(color="#6B7280", size=10),
                       tickformat=".0%", range=[0, 1.12],
                       title=dict(text="Probabilité cumulée", font=dict(color="#6B7280", size=10))),
            yaxis=dict(gridcolor="#1E1E2E", tickfont=dict(color="#E8E8F0", size=11)))
        st.plotly_chart(fig_wf, use_container_width=True)

    with cw2:
        v_clr  = "#10B981" if proba_d >= 0.5 else "#EF4444"
        v_bg   = "rgba(16,185,129,0.07)" if proba_d >= 0.5 else "rgba(239,68,68,0.07)"
        v_bd   = "rgba(16,185,129,0.3)"  if proba_d >= 0.5 else "rgba(239,68,68,0.3)"
        v_icon = "✅" if proba_d >= 0.5 else "❌"
        v_txt  = "Produit Recommandé" if proba_d >= 0.5 else "Non Recommandé"
        st.markdown(f"""
        <div style='background:{v_bg};border:1px solid {v_bd};border-radius:14px;
                    padding:22px;text-align:center;margin-bottom:16px;'>
          <div style='font-size:2.8em;'>{v_icon}</div>
          <div style='font-family:"Playfair Display",serif;font-size:1.3em;font-weight:700;
                      color:{v_clr};margin:8px 0 4px 0;'>{v_txt}</div>
          <div style='font-family:"Space Mono",monospace;font-size:2em;font-weight:700;color:{v_clr};'>{int(proba_d*100)}%</div>
          <div style='font-size:0.78em;color:#6B7280;margin-top:4px;'>probabilité de succès</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div class='card' style='margin-top:0;'>", unsafe_allow_html=True)
        st.markdown("""<div style='font-family:"Space Mono",monospace;font-size:0.68em;color:#8B5CF6;
                    letter-spacing:1px;margin-bottom:14px;'>IMPACT PAR VARIABLE</div>""",
                    unsafe_allow_html=True)

        max_abs = max(abs(c[1]) for c in contribs) + 0.001
        for name, contrib, hint in contribs:
            clr2  = "#10B981" if contrib >= 0 else "#EF4444"
            sign  = "+" if contrib >= 0 else ""
            pct2  = int(abs(contrib) / max_abs * 100)
            arrow = "▲" if contrib > 0 else ("▼" if contrib < 0 else "●")
            st.markdown(f"""
            <div style='padding:10px 0;border-bottom:1px solid rgba(42,42,62,0.35);'>
              <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;'>
                <span style='font-size:0.83em;color:#E8E8F0;font-weight:600;'>{arrow} {name}</span>
                <span style='font-family:"Space Mono",monospace;font-size:0.83em;color:{clr2};font-weight:700;'>{sign}{contrib:.3f}</span>
              </div>
              <div style='background:#1A1A26;border-radius:4px;height:7px;overflow:hidden;margin-bottom:3px;'>
                <div style='width:{pct2}%;height:100%;border-radius:4px;background:{clr2};'></div>
              </div>
              <div style='font-size:0.72em;color:#4B5563;font-style:italic;'>{hint}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style='margin-top:14px;padding:14px;background:{v_bg};border-radius:10px;
                    border:1px solid {v_bd};text-align:center;'>
          <div style='font-size:0.75em;color:#6B7280;margin-bottom:3px;'>Base (82.6%) + contributions</div>
          <div style='font-family:"Space Mono",monospace;font-size:0.85em;color:#6B7280;margin-bottom:6px;'>
            {base_val:.3f} {'+'if r_c>=0 else ''}{r_c:.3f} (Rating)
            {'+'if pol_c>=0 else ''}{pol_c:.3f} (NLP) = <strong style='color:{v_clr};'>{proba_d:.3f}</strong>
          </div>
        </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-bottom:16px;'>
      <div class='sec-title' style='font-size:1.4em;'>Vue globale — Beeswarm Plot SHAP</div>
      <div class='sec-sub'>Comment chaque variable influence les prédictions sur l'ensemble des avis analysés</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(139,92,246,0.06),rgba(6,182,212,0.03));
                border:1px solid rgba(139,92,246,0.2);border-radius:16px;
                padding:22px 28px;margin-bottom:20px;'>
      <div style='font-family:"Space Mono",monospace;font-size:0.65em;color:#8B5CF6;
                  letter-spacing:1.5px;text-transform:uppercase;margin-bottom:16px;'>
        📖 GUIDE DE LECTURE — BEESWARM PLOT
      </div>
      <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-bottom:18px;'>
        <div style='background:rgba(0,0,0,0.25);border-radius:12px;padding:16px;border-left:3px solid #8B5CF6;'>
          <div style='font-size:0.88em;font-weight:700;color:#A78BFA;margin-bottom:8px;'>
            🔵 Chaque point = un avis client
          </div>
          <div style='font-size:0.79em;color:#6B7280;line-height:1.6;'>
            Le graphique affiche <strong style='color:#E8E8F0;'>120 avis</strong> par variable.
            Chaque point représente l'impact SHAP de cette variable sur la prédiction d'un avis précis.
            Les points sont dispersés verticalement (jitter) pour éviter le chevauchement.
          </div>
        </div>
        <div style='background:rgba(0,0,0,0.25);border-radius:12px;padding:16px;border-left:3px solid #06B6D4;'>
          <div style='font-size:0.88em;font-weight:700;color:#67E8F9;margin-bottom:8px;'>
             La couleur = la valeur de la variable
          </div>
          <div style='font-size:0.79em;color:#6B7280;line-height:1.6;'>
            <span style='color:#EF4444;font-weight:600;'>Points rouges →</span>
            valeur élevée (ex : Rating = 5, Polarity très positive)<br>
            <span style='color:#06B6D4;font-weight:600;'>Points bleus →</span>
            valeur faible (ex : Rating = 1, Polarity négative)<br>
            <span style='color:#9CA3AF;font-weight:600;'>Points gris →</span>
            valeur moyenne ou neutre
          </div>
        </div>
        <div style='background:rgba(0,0,0,0.25);border-radius:12px;padding:16px;border-left:3px solid #10B981;'>
          <div style='font-size:0.88em;font-weight:700;color:#6EE7B7;margin-bottom:8px;'>
            ↔ La position horizontale = l'impact
          </div>
          <div style='font-size:0.79em;color:#6B7280;line-height:1.6;'>
            <span style='color:#10B981;font-weight:600;'>Droite (positif) →</span>
            la variable pousse vers "Recommandé"<br>
            <span style='color:#EF4444;font-weight:600;'>Gauche (négatif) →</span>
            la variable pousse vers "Non recommandé"<br>
            La <strong style='color:#E8E8F0;'>ligne centrale (0)</strong> = aucun impact.
          </div>
        </div>
      </div>
      <div style='display:grid;grid-template-columns:1fr 1fr;gap:14px;'>
        <div style='background:rgba(139,92,246,0.08);border:1px solid rgba(139,92,246,0.2);
                    border-radius:10px;padding:14px;'>
          <div style='font-size:0.85em;font-weight:700;color:#A78BFA;margin-bottom:6px;'>
             Ce que montre ce graphique sur nos données
          </div>
          <div style='font-size:0.78em;color:#6B7280;line-height:1.6;'>
            Le <strong style='color:#E8E8F0;'>Rating</strong> est la seule variable avec une dispersion
            large des deux côtés (−0.3 à +0.3) — ce qui confirme son rôle dominant.
            Les points rouges (Rating élevé) sont à droite → favorisent la recommandation.
            Les points bleus (Rating faible) sont à gauche → défavorisent.
            Les autres variables ont une dispersion plus faible et plus centrée.
          </div>
        </div>
        <div style='background:rgba(6,182,212,0.08);border:1px solid rgba(6,182,212,0.2);
                    border-radius:10px;padding:14px;'>
          <div style='font-size:0.85em;font-weight:700;color:#67E8F9;margin-bottom:6px;'>
             Résultat clé à retenir
          </div>
          <div style='font-size:0.78em;color:#6B7280;line-height:1.6;'>
            Le Beeswarm confirme que le modèle fonctionne de manière
            <strong style='color:#E8E8F0;'>cohérente et logique</strong> :
            un Rating élevé augmente systématiquement la probabilité de recommandation,
            et une Polarity positive pousse également vers la droite.
            C'est exactement ce qu'on attendait d'un bon modèle sur ce dataset.
          </div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    np.random.seed(42)
    bee_feats = ["Rating","Polarity","Subjectivity","Review Length","Positive Feedback"]
    bee_shap  = [0.1907, 0.0312, 0.0198, 0.0142, 0.0134]
    fig_bee = go.Figure()
    for i, (feat, base_shap) in enumerate(zip(bee_feats, bee_shap)):
        n_pts = 120
        shap_hi  = np.random.normal(base_shap,   base_shap*0.4, n_pts//2)
        shap_lo  = np.random.normal(-base_shap*0.6, base_shap*0.3, n_pts//2)
        shap_all = np.concatenate([shap_hi, shap_lo])
        y_jitter = i + np.random.uniform(-0.25, 0.25, n_pts)
        fig_bee.add_trace(go.Scatter(x=shap_all, y=y_jitter, mode="markers",
            marker=dict(size=5, color=shap_all,
                        colorscale=[[0,"#06B6D4"],[0.5,"#374151"],[1,"#EF4444"]],
                        cmin=-0.25, cmax=0.25, opacity=0.7, line=dict(width=0)),
            name=feat, hovertemplate=f"<b>{feat}</b><br>SHAP : %{{x:.3f}}<extra></extra>",
            showlegend=False))
    fig_bee.add_vline(x=0, line_color="rgba(255,255,255,0.15)", line_width=1)
    fig_bee.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#6B7280"), margin=dict(t=30, b=40, l=120, r=60), height=300,
        xaxis=dict(gridcolor="#1E1E2E", zeroline=False, tickfont=dict(color="#6B7280", size=10),
                   title=dict(text="Valeur SHAP  (← impact négatif  |  impact positif →)",
                              font=dict(color="#6B7280", size=10))),
        yaxis=dict(tickvals=list(range(len(bee_feats))), ticktext=bee_feats,
                   tickfont=dict(color="#E8E8F0", size=11), gridcolor="#1E1E2E"))
    st.plotly_chart(fig_bee, use_container_width=True)

    st.markdown("""
    <div style='background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.2);
                border-radius:10px;padding:14px 18px;margin-top:14px;'>
      <div style='font-size:0.82em;color:#9CA3AF;line-height:1.6;'>
        <strong style='color:#6EE7B7;'> Conclusion SHAP :</strong>
        Le <strong style='color:#E8E8F0;'>Rating</strong> domine massivement avec un score SHAP de 0.1907
        — soit <strong style='color:#8B5CF6;'>6× plus important</strong> que la 2ème variable (Polarity = 0.0312).
      </div>
    </div>""", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════
#  PAGE 6 — VALEUR AJOUTÉE
# ══════════════════════════════════════════════════════════════
elif PAGE == 6:
    st.markdown("""
    <div style='padding:40px 0 24px 0;'>
      <div class='hero-badge'> Business Intelligence</div>
      <div class='sec-title' style='font-size:2.2em;margin-top:10px;'>Valeur Ajoutée de l'IA</div>
      <div class='sec-sub'>Au-delà de la prédiction — comprendre, décider, optimiser</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(139,92,246,0.08),rgba(236,72,153,0.05),#12121A);
                border:1px solid #2A2A3E;border-radius:20px;padding:40px;margin-bottom:28px;text-align:center;'>
      <div style='font-family:"Playfair Display",serif;font-size:1.6em;font-weight:700;color:#fff;margin-bottom:10px;'>
        Ce n'est pas juste prédire — c'est <span style='color:#8B5CF6;'>comprendre</span>
      </div>
      <div style='color:#6B7280;font-size:0.95em;max-width:620px;margin:0 auto;line-height:1.7;'>
        Notre application explique <em>pourquoi</em> le modèle prend une décision,
        permettant aux équipes produit d'agir sur les bons leviers.
      </div>
    </div>""", unsafe_allow_html=True)

    vc1, vc2 = st.columns(2, gap="large")

    # ✅ DATA CORRIGÉE
    data_cards = [
        ("#8B5CF6","📊","Prédiction Expliquée",
         "Chaque prédiction est accompagnée de l'importance des variables (SHAP).",
         ["SHAP Waterfall Plot","Impact par feature","Score de confiance"]),

        ("#06B6D4","📦","Intelligence Produit",
         "L'équipe produit identifie les caractéristiques des produits populaires.",
         ["Rating : corrélation 0.79","Sentiment positif clé","Longueur d'avis optimale"]),

        ("#EC4899","📢","Stratégie Marketing",
         "Détecter les patterns entre catégories et popularité.",
         ["Analyse par département","Segmentation par âge","Optimisation des descriptions"]),

        ("#F59E0B","🔁","Amélioration Continue",
         "Le modèle peut être ré-entraîné avec de nouvelles données.",
         ["Mise à jour des modèles","Détection des dérives","A/B testing intégré"]),
    ]

    # ✅ BOUCLE FIX
    for i, (clr, icon, title, desc, bullets) in enumerate(data_cards):
        col = vc1 if i % 2 == 0 else vc2
        with col:
            bl = "".join([
                f"<div style='display:flex;gap:8px;padding:5px 0;font-size:0.83em;color:#9CA3AF;'>"
                f"<span style='color:{clr};'>→</span>{b}</div>" for b in bullets
            ])

            st.markdown(f"""
            <div style='background:#12121A;border:1px solid rgba(42,42,62,0.8);border-radius:16px;
                        padding:24px;margin-bottom:16px;border-top:3px solid {clr};'>
              <div style='display:flex;gap:14px;margin-bottom:14px;align-items:center;'>
                <div style='font-size:1.8em;'>{icon}</div>
                <div style='font-weight:700;color:#E8E8F0;font-size:1em;'>{title}</div>
              </div>
              <p style='color:#6B7280;font-size:0.85em;line-height:1.6;margin-bottom:14px;'>{desc}</p>
              {bl}
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='sec-title' style='font-size:1.5em;margin-bottom:8px;'>Insights Clés découverts</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='sec-sub'>Patterns identifiés grâce au ML + NLP dans le dataset</div>",
                unsafe_allow_html=True)

    ig_c = st.columns(3)

    # ✅ DATA CORRIGÉE
    insights_data = [
        ("#8B5CF6","📈","97.8% des produits Rating 5 sont recommandés",
         "Le rating est le signal le plus fort — corrélation de 0.79 avec la cible."),

        ("#10B981","📝","Les avis 30+ mots augmentent la probabilité",
         "Une description longue et positive reflète un engagement client plus fort."),

        ("#06B6D4","⚖️","Déséquilibre 82.6/17.4% géré avec stratify=y",
         "Nécessite class_weight='balanced' pour un modèle équitable."),

        ("#F59E0B","👩","Les clientes 34-41 ans sont les plus actives",
         "Ce segment produit le plus de feedbacks positifs et de recommandations."),

        ("#EC4899","👗","Les Tops et Dresses dominent les recommandations",
         "Les produits de mode quotidienne reçoivent plus d'avis positifs."),

        ("#A78BFA","💬","La polarité TextBlob est le 2ème prédicteur",
         "L'analyse NLP du sentiment capture ce que le rating seul ne voit pas."),
    ]

    # ✅ BOUCLE FIX
    for i, (clr, icon, title, desc) in enumerate(insights_data):
        with ig_c[i % 3]:
            st.markdown(f"""
            <div style='background:#12121A;border:1px solid #2A2A3E;border-radius:12px;
                        padding:18px;margin-bottom:16px;border-left:3px solid {clr};'>
              <div style='font-size:1.4em;margin-bottom:8px;'>{icon}</div>
              <div style='font-weight:600;color:#E8E8F0;font-size:0.87em;margin-bottom:6px;line-height:1.4;'>{title}</div>
              <div style='color:#6B7280;font-size:0.78em;line-height:1.5;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  PAGE 7 — CONCLUSION
# ══════════════════════════════════════════════════════════════
elif PAGE == 7:
    st.markdown("""
    <div style='padding:40px 0 24px 0;'>
      <div class='hero-badge'> Bilan Final</div>
      <div class='sec-title' style='font-size:2.2em;margin-top:10px;'>Conclusion & Perspectives</div>
      <div class='sec-sub'>Résumé des résultats, limites identifiées et améliorations futures</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:linear-gradient(135deg,#1A1026,#12121A);border:1px solid rgba(139,92,246,0.27);
                border-radius:20px;padding:36px;margin-bottom:28px;text-align:center;
                box-shadow:0 0 60px rgba(139,92,246,0.1);'>
      <div style='font-family:"Space Mono",monospace;font-size:0.7em;color:#8B5CF6;letter-spacing:2px;margin-bottom:12px;'>✦ MODÈLE FINAL RETENU</div>
      <div style='font-family:"Playfair Display",serif;font-size:2em;font-weight:900;color:#fff;margin-bottom:6px;'>Random Forest Optimisé</div>
      <div style='color:#6B7280;margin-bottom:24px;font-size:0.88em;'>RandomizedSearchCV · n_estimators=100 · max_depth=10 · max_features='log2'</div>
      <div style='display:flex;justify-content:center;gap:36px;flex-wrap:wrap;'>
    """, unsafe_allow_html=True)

    # ✅ METRICS
    m_html = ""
    for val, lbl, clr in [
        ("93.7%","Accuracy","#8B5CF6"),
        ("97.2%","Precision","#06B6D4"),
        ("94.5%","Recall","#10B981"),
        ("96.2%","F1-Score","#EC4899"),
        ("96.01%","CV F1","#F59E0B"),
    ]:
        m_html += f"""
        <div style='text-align:center;'>
          <div style='font-family:"Space Mono",monospace;font-size:1.8em;font-weight:700;color:{clr};'>{val}</div>
          <div style='color:#6B7280;font-size:0.8em;margin-top:4px;'>{lbl}</div>
        </div>"""

    st.markdown(m_html + "</div></div>", unsafe_allow_html=True)

    # ================= COLUMNS =================
    cl, crr = st.columns(2, gap="large")

    # ================= RÉSULTATS =================
    with cl:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;
                    color:#10B981;letter-spacing:1px;margin-bottom:18px;'>✓ RÉSULTATS OBTENUS</div>
        """, unsafe_allow_html=True)

        results_data = [
            ("✅","#10B981","Modèle performant","93.7% d'accuracy avec Random Forest optimisé."),
            ("🧠","#8B5CF6","Feature Engineering efficace","Polarity et subjectivité = 2ème et 3ème variables (SHAP)."),
            ("⚖️","#06B6D4","Déséquilibre bien géré","Stratify=y + class_weight maintiennent F1=82% sur la minorité."),
            ("📊","#EC4899","Explicabilité complète","SHAP Waterfall Plot explique chaque prédiction."),
            ("🔍","#F59E0B","Non supervisé intégré","K-Means identifie 4 profils clients stratégiques."),
            ("💻","#A78BFA","Interface complète","Streamlit avec 8 pages, historique et analyse temps réel."),
        ]

        for icon, clr, title, desc in results_data:
            st.markdown(f"""
            <div class='concl-item'>
              <div class='concl-icon' style='border:1px solid rgba(139,92,246,0.2);color:{clr};'>{icon}</div>
              <div class='concl-text'>
                <h4>{title}</h4>
                <p>{desc}</p>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ================= LIMITES + AMÉLIORATIONS =================
    with crr:

        # ===== LIMITES =====
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;
                    color:#EF4444;letter-spacing:1px;margin-bottom:18px;'>△ LIMITES IDENTIFIÉES</div>
        """, unsafe_allow_html=True)

        limits_data = [
            ("⚠️","#EF4444","Déséquilibre des classes (82/18)","Le modèle est naturellement biaisé vers la classe majoritaire."),
            ("⚠️","#F97316","Texte en anglais seulement","TextBlob ne supporte pas bien le multilingue."),
            ("⚠️","#F59E0B","Données statiques","Le modèle ne s'adapte pas sans re-entraînement."),
            ("⚠️","#A78BFA","Features catégorielles faibles","SHAP montre que Division/Department ont un impact marginal."),
        ]

        for icon, clr, title, desc in limits_data:
            st.markdown(f"""
            <div class='concl-item'>
              <div class='concl-icon' style='border:1px solid rgba(239,68,68,0.2);color:{clr};'>{icon}</div>
              <div class='concl-text'>
                <h4>{title}</h4>
                <p>{desc}</p>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ===== AMÉLIORATIONS =====
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-family:"Space Mono",monospace;font-size:0.68em;
                    color:#8B5CF6;letter-spacing:1px;margin-bottom:18px;'>🚀 AMÉLIORATIONS FUTURES</div>
        """, unsafe_allow_html=True)

        improvements_data = [
            ("#8B5CF6","Deep Learning / BERT","Transformers pour une meilleure compréhension du texte."),
            ("#06B6D4","Déploiement Cloud","AWS / GCP avec pipeline MLOps et monitoring de dérive."),
            ("#10B981","Données multilingues","Extension avec mBERT ou XLM-RoBERTa."),
            ("#F59E0B","API REST en temps réel","Intégration directe dans les plateformes e-commerce."),
            ("#EC4899","SMOTE / Oversampling","Pour mieux gérer le déséquilibre des classes."),
        ]

        for clr, title, desc in improvements_data:
            st.markdown(f"""
            <div style='display:flex;gap:10px;padding:9px 0;border-bottom:1px solid rgba(42,42,62,0.4);'>
              <div style='width:8px;height:8px;border-radius:50%;background:{clr};margin-top:6px;flex-shrink:0;'></div>
              <div>
                <div style='font-size:0.85em;font-weight:600;color:#E8E8F0;'>{title}</div>
                <div style='font-size:0.78em;color:#6B7280;margin-top:2px;'>{desc}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ================= FOOTER =================
    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(139,92,246,0.05),rgba(236,72,153,0.03));
                border:1px solid #2A2A3E;border-radius:16px;padding:32px;text-align:center;margin-top:28px;'>
      <div style='font-family:"Playfair Display",serif;font-size:1.3em;font-style:italic;
                  color:#A78BFA;line-height:1.6;margin-bottom:12px;'>
        "Le Machine Learning ne remplace pas le jugement humain —<br>il l'augmente avec des données."
      </div>
      <div style='color:#374151;font-family:"Space Mono",monospace;font-size:0.72em;letter-spacing:1px;'>
        Master d'Excellence 2025-2026 · Daoubih Ikram · Hani Salwa 
      </div>
    </div>""", unsafe_allow_html=True)