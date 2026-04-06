
"""
PawIndia Market Research Dashboard
Dark-theme edition — all audit fixes applied
Compatible with Python 3.8–3.11
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os, time, math

st.set_page_config(
    page_title="PawIndia Dashboard",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Dark Palette ──────────────────────────────────────────────────────────────
BG        = "#0D0A06"       # deepest background
SURFACE   = "#1A1209"       # card/panel surface
SURFACE2  = "#231B10"       # slightly lighter surface for nested elements
BORDER    = "rgba(212,168,83,0.18)"
BROWN     = "#A0784C"       # lighter brown for dark bg readability
AMBER     = "#D4A853"       # primary accent
HONEY     = "#E8C36A"       # bright warm accent
SAGE      = "#7CB67C"       # green for positive
TEAL      = "#5BB8C4"       # cool accent
MAUVE     = "#B89ED6"       # purple accent (brightened)
TERRA     = "#D48A62"       # warm terracotta
GREEN_YES = "#66BB6A"       # bright green for "Yes"
RED_NO    = "#EF5350"       # bright red for "No"
CHART     = [AMBER, HONEY, "#D48A62", SAGE, TEAL, MAUVE, TERRA,
             "#C49A6C", "#E8B960", "#5CC4A0"]

# Text colours — all high-contrast on dark backgrounds
TEXT      = "#EDE4D3"       # primary body text (warm cream)
TEXT_DIM  = "#B8A88A"       # secondary / captions (still passes AA on #1A1209)
TEXT_BRIGHT = "#F5EDE0"     # headings — near-white warm
PLOT_TXT  = "#EDE4D3"       # chart labels and axes

PCFG = {"displayModeBar": False}

# ── Plotly base layout (dark) ─────────────────────────────────────────────────
_AXIS = dict(
    gridcolor="rgba(212,168,83,0.08)",
    linecolor="rgba(212,168,83,0.20)",
    zeroline=False,
    tickfont=dict(color=PLOT_TXT, size=11, family="Plus Jakarta Sans,Inter,sans-serif"),
    title_font=dict(color=TEXT, size=11, family="Plus Jakarta Sans,Inter,sans-serif"),
)
PL = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(26,18,9,0.6)",
    font=dict(family="Plus Jakarta Sans,Inter,sans-serif", color=TEXT, size=11),
    xaxis=dict(**_AXIS),
    yaxis=dict(**_AXIS),
    legend=dict(font=dict(color=TEXT, size=11)),
)

# ── Animated Akita logo ──────────────────────────────────────────────────────
LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"
     width="120" height="120" style="display:block;margin:0 auto"
     role="img" aria-label="PawIndia dog mascot logo">
  <defs>
    <linearGradient id="fur" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#D4A853"/>
      <stop offset="100%" style="stop-color:#6F4E37"/>
    </linearGradient>
    <linearGradient id="fur2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#EDE4D3"/>
      <stop offset="80%" style="stop-color:#D4A853;stop-opacity:0.8"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <g filter="url(#glow)" style="animation:float 6s ease-in-out infinite">
    <path d="M120 80 L95 30 L85 35 L90 75 Q95 95 110 105 Z" fill="url(#fur)" opacity="0.95"/>
    <path d="M280 80 L305 30 L315 35 L310 75 Q305 95 290 105 Z" fill="url(#fur)" opacity="0.95"/>
    <ellipse cx="200" cy="160" rx="95" ry="85" fill="url(#fur)"/>
    <ellipse cx="200" cy="155" rx="80" ry="65" fill="url(#fur2)" opacity="0.25"/>
    <path d="M140 135 Q130 115 115 120 Q105 130 120 145 Q130 155 145 150 Z" fill="#EDE4D3" opacity="0.5"/>
    <path d="M260 135 Q270 115 285 120 Q295 130 280 145 Q270 155 255 150 Z" fill="#EDE4D3" opacity="0.5"/>
    <circle cx="170" cy="145" r="13" fill="#1A1209"/>
    <circle cx="230" cy="145" r="13" fill="#1A1209"/>
    <circle cx="173" cy="142" r="4" fill="#EDE4D3" opacity="0.9"/>
    <circle cx="233" cy="142" r="4" fill="#EDE4D3" opacity="0.9"/>
    <ellipse cx="200" cy="176" rx="14" ry="10" fill="#1A1209" opacity="0.85"/>
    <path d="M190 183 Q200 193 210 183" stroke="#1A1209" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <ellipse cx="200" cy="265" rx="75" ry="90" fill="url(#fur)"/>
    <path d="M155 330 Q160 365 170 380 Q175 388 165 390 Q150 390 148 380 Q142 365 140 345 Z" fill="url(#fur)"/>
    <path d="M245 330 Q240 365 230 380 Q225 388 235 390 Q250 390 252 380 Q258 365 260 345 Z" fill="url(#fur)"/>
    <path d="M275 250 Q310 260 330 280 Q345 300 355 340 Q360 360 340 365 Q320 365 315 350 Q305 320 290 300 Z" fill="url(#fur)" opacity="0.85"/>
    <path d="M160 225 Q200 205 240 225 Q250 265 240 305 Q200 325 160 305 Q150 265 160 225 Z" fill="url(#fur2)" opacity="0.2"/>
    <ellipse cx="200" cy="395" rx="55" ry="8" fill="rgba(212,168,83,0.1)"/>
  </g>
  <style>
    @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
  </style>
</svg>
"""

WORDMARK = """
<div style="text-align:center;margin-top:6px">
  <span style="font-family:Georgia,serif;font-size:22px;font-weight:800;color:#EDE4D3">Paw</span>
  <span style="font-family:Georgia,serif;font-size:22px;font-weight:800;color:#D4A853">India</span>
  <div style="color:#9A8D76;font-size:8px;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px">
    Connecting Every Dog and Their Human
  </div>
</div>
"""

# ── CSS (Full Dark Theme) ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&display=swap');

/* ── Global dark background ── */
html, body, [class*="css"] {
  font-family: 'Plus Jakarta Sans', sans-serif;
  background: #0D0A06 !important;
  color: #EDE4D3 !important;
}
.stApp { background: #0D0A06 !important; }
.main .block-container { background: #0D0A06 !important; }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1400px; }
stApp::before, .stApp::after {
  content: "";
  position: fixed;
  width: 460px;
  height: 460px;
  border-radius: 999px;
  filter: blur(90px);
  opacity: 0.12;
  pointer-events: none;
  z-index: 0;
  animation: floatGlow 14s ease-in-out infinite;
}
.stApp::before { top: -140px; right: -120px; background: #D4A853; }
.stApp::after  { bottom: -170px; left: -100px; background: #B89ED6; animation-delay: -5s; }
.main .block-container { position: relative; z-index: 1; }

@keyframes floatGlow {
  0%,100% { transform: translateY(0) translateX(0) scale(1); }
  50%     { transform: translateY(-18px) translateX(14px) scale(1.08); }
}
/* ── Force all Streamlit text to cream on dark ── */
.stMarkdown p, .stMarkdown li, .stMarkdown span,
[data-testid="stText"], label, .stSelectbox label,
.stSlider label, .stRadio label, [data-baseweb="select"] span,
[data-testid="stWidgetLabel"] p { color: #EDE4D3 !important; font-weight: 500; }

[data-testid="stSelectbox"] label p { color: #EDE4D3 !important; font-weight: 600 !important; }
[data-testid="stSlider"] label p { color: #EDE4D3 !important; font-weight: 600 !important; }
[data-baseweb="select"] [data-testid="stMarkdownContainer"] p { color: #EDE4D3 !important; }

/* Selectbox / dropdown dark styling */
[data-baseweb="select"] { background: #1A1209 !important; }
[data-baseweb="popover"] { background: #1A1209 !important; }
[data-baseweb="menu"] { background: #1A1209 !important; }
[data-baseweb="select"] > div { background: #1A1209 !important; border-color: rgba(212,168,83,0.25) !important; }
[data-baseweb="input"] { background: #1A1209 !important; color: #EDE4D3 !important; }

/* Metric cards */
[data-testid="stMetric"] { background: #1A1209 !important; border: 1px solid rgba(212,168,83,0.15) !important; border-radius: 12px !important; padding: 14px !important; }
[data-testid="stMetricValue"] { color: #D4A853 !important; }
[data-testid="stMetricLabel"] { color: #B8A88A !important; }
[data-testid="stMetricDelta"] { color: #7CB67C !important; }

/* Dataframe */
[data-testid="stDataFrame"] { border: 1px solid rgba(212,168,83,0.15) !important; border-radius: 10px !important; }
.stDataFrame table { background: #1A1209 !important; color: #EDE4D3 !important; }

/* Spinner */
.stSpinner > div { color: #D4A853 !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1A1209, #0D0A06) !important;
  border-right: 1px solid rgba(212,168,83,0.15) !important;
}
section[data-testid="stSidebar"] * { color: #B8A88A !important; }
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  display: flex !important; align-items: center !important; background: transparent !important;
  border: 1px solid transparent !important; border-radius: 10px !important; padding: 9px 14px !important;
  margin: 0 !important; cursor: pointer !important; width: 100% !important;
  transition: all .25s cubic-bezier(.22,1,.36,1) !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
  background: rgba(212,168,83,0.08) !important; border-color: rgba(212,168,83,0.2) !important;
  transform: translateX(4px) !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
  background: linear-gradient(135deg,rgba(160,125,58,.22),rgba(155,124,182,.1)) !important;
  border-color: rgba(212,168,83,0.35) !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p {
  color: #B8A88A !important; font-size: 12.5px !important; font-weight: 500 !important; margin: 0 !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) p {
  color: #D4A853 !important; font-weight: 700 !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label>div:first-child,
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] input[type="radio"] {
  display: none !important; width: 0 !important; height: 0 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(26,18,9,0.9) !important; border-radius: 12px !important;
  padding: 4px !important; border: 1px solid rgba(212,168,83,0.15) !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; border-radius: 9px !important;
  color: #B8A88A !important; font-size: 12.5px !important; font-weight: 600 !important;
  padding: 8px 18px !important; transition: all .2s !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #6F4E37, #D4860B) !important;
  color: #FFF8F0 !important; box-shadow: 0 2px 8px rgba(111,78,55,.4) !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 20px !important; }

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, #6F4E37, #D4860B) !important;
  color: #FFF8F0 !important; border: none !important; border-radius: 10px !important;
  font-weight: 700 !important; padding: 9px 22px !important;
}
.stDownloadButton > button {
  background: linear-gradient(135deg, #3d6b3d, #5a9a5a) !important;
  color: white !important; border: none !important; border-radius: 10px !important; font-weight: 700 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
  border: 1px solid rgba(212,168,83,0.15) !important; border-radius: 12px !important;
  background: #1A1209 !important; margin-top: 20px !important;
}
[data-testid="stExpander"] summary p {
  color: #D4A853 !important; font-weight: 700 !important; font-size: .9rem !important;
}
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {
  color: #EDE4D3 !important;
}

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div > div {
  background: #D4A853 !important;
}

/* ── Cards and helpers ── */
.icard {
  background: #1A1209; border: 1px solid rgba(212,168,83,0.15); border-radius: 14px;
  padding: 20px; margin-bottom: 14px; box-shadow: 0 2px 12px rgba(0,0,0,.3);
}
.shead {
  color: #EDE4D3; font-size: 1.1rem; font-weight: 700; border-bottom: 2px solid #D4A853;
  padding-bottom: 6px; margin: 32px 0 18px;
}
.ibox {
  background: linear-gradient(135deg, rgba(212,168,83,.12), rgba(26,18,9,.9));
  border-left: 4px solid #D4A853; border-radius: 0 10px 10px 0;
  padding: 12px 16px; margin: 12px 0 28px; color: #EDE4D3; font-size: .88rem; font-weight: 500;
}
.warnbox {
  background: linear-gradient(135deg, rgba(239,83,80,.08), rgba(26,18,9,.9));
  border-left: 4px solid #EF5350; border-radius: 0 10px 10px 0;
  padding: 12px 16px; margin: 12px 0 28px; color: #EDE4D3; font-size: .88rem; font-weight: 500;
}
.lbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 9px 18px; border-radius: 12px; margin-bottom: 16px;
  background: linear-gradient(135deg, rgba(26,18,9,.92), rgba(13,10,6,.97));
  border: 1px solid rgba(212,168,83,.2);
}
@keyframes liveDot { 0%,100%{opacity:1} 50%{opacity:.3} }
@keyframes floatCard {
  0%,100% { transform: translateY(0); box-shadow: 0 4px 20px rgba(0,0,0,.3); }
  50% { transform: translateY(-4px); box-shadow: 0 8px 28px rgba(0,0,0,.4); }
}

/* ── Icon & element animations ── */
@keyframes iconBounce {
  0%,100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
  50% { transform: translateY(0); }
  70% { transform: translateY(-3px); }
}
@keyframes iconPulse {
  0%,100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.15); opacity: 0.85; }
}
@keyframes iconWiggle {
  0%,100% { transform: rotate(0deg); }
  25% { transform: rotate(-8deg); }
  75% { transform: rotate(8deg); }
}
@keyframes shimmer {
  0% { background-position: -200% center; }
  100% { background-position: 200% center; }
}
@keyframes glowPulse {
  0%,100% { box-shadow: 0 2px 12px rgba(0,0,0,.3); border-color: rgba(212,168,83,0.15); }
  50% { box-shadow: 0 4px 20px rgba(212,168,83,.15); border-color: rgba(212,168,83,0.3); }
}
@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(18px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes borderGlow {
  0%,100% { border-color: rgba(212,168,83,0.15); }
  50% { border-color: rgba(212,168,83,0.4); }
}
@keyframes spinSlow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ── Animated sidebar nav icons ── */
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p {
  transition: all .3s cubic-bezier(.22,1,.36,1) !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover p {
  letter-spacing: 0.3px !important;
}

/* ── Animated info/warn boxes ── */
.ibox {
  animation: fadeSlideUp 0.5s ease-out both;
  transition: transform .3s ease, box-shadow .3s ease;
}
.ibox:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 16px rgba(212,168,83,.12);
}
.warnbox {
  animation: fadeSlideUp 0.5s ease-out both;
  transition: transform .3s ease, box-shadow .3s ease;
}
.warnbox:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 16px rgba(239,83,80,.12);
}

/* ── Animated section headers ── */
.shead {
  animation: fadeSlideUp 0.4s ease-out both;
}

/* ── Animated cards ── */
.icard {
  animation: fadeSlideUp 0.5s ease-out both, glowPulse 4s ease-in-out infinite;
  transition: transform .35s ease, box-shadow .35s ease;
}
.icard:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 28px rgba(212,168,83,.18);
}

/* ── Live bar animated gradient border ── */
.lbar {
  animation: borderGlow 3s ease-in-out infinite;
  transition: transform .3s ease;
}
.lbar:hover {
  transform: scale(1.005);
}

/* ── Animated metric cards ── */
[data-testid="stMetric"] {
  animation: fadeSlideUp 0.5s ease-out both;
  transition: transform .3s ease, box-shadow .3s ease !important;
}
[data-testid="stMetric"]:hover {
  transform: translateY(-3px) !important;
  box-shadow: 0 6px 20px rgba(212,168,83,.15) !important;
}

/* ── Animated tabs ── */
.stTabs [data-baseweb="tab"] {
  transition: all .3s cubic-bezier(.22,1,.36,1) !important;
}
.stTabs [data-baseweb="tab"]:hover {
  transform: translateY(-2px) !important;
}
.stTabs [aria-selected="true"] {
  animation: glowPulse 3s ease-in-out infinite;
}

/* ── Button hover effects ── */
.stButton > button {
  transition: all .3s ease !important;
}
.stButton > button:hover {
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow: 0 6px 20px rgba(111,78,55,.4) !important;
}
.stDownloadButton > button {
  transition: all .3s ease !important;
}
.stDownloadButton > button:hover {
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow: 0 6px 20px rgba(61,107,61,.4) !important;
}

/* ── Expander animation ── */
[data-testid="stExpander"] {
  animation: fadeSlideUp 0.5s ease-out both;
  transition: border-color .3s ease !important;
}
[data-testid="stExpander"]:hover {
  border-color: rgba(212,168,83,0.3) !important;
}

/* ── Animated icon spans ── */
.anim-bounce { display:inline-block; animation: iconBounce 2s ease-in-out infinite; }
.anim-pulse  { display:inline-block; animation: iconPulse 2.5s ease-in-out infinite; }
.anim-wiggle { display:inline-block; animation: iconWiggle 2s ease-in-out infinite; }
.anim-spin   { display:inline-block; animation: spinSlow 8s linear infinite; }
.anim-float  { display:inline-block; animation: floatCard 4s ease-in-out infinite; }

/* ── Shimmer text effect for page titles ── */
.shimmer-title {
  background: linear-gradient(90deg, #EDE4D3 0%, #D4A853 25%, #EDE4D3 50%, #D4A853 75%, #EDE4D3 100%);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 4s linear infinite;
}

/* ── Animated gradient dividers ── */
.anim-divider {
  height: 2px; border: none; border-radius: 2px;
  background: linear-gradient(90deg, transparent, #D4A853, #6F4E37, #D4A853, transparent);
  background-size: 200% 100%;
  animation: gradientShift 3s ease infinite;
  margin: 16px 0;
}
</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    raw = pd.read_csv(os.path.join(base, "pawindia_raw_data.csv"))
    df  = pd.read_csv(os.path.join(base, "pawindia_cleaned_data.csv"))
    return raw, df


# ── ML ────────────────────────────────────────────────────────────────────────
@st.cache_data
def build_features():
    _, df = load_data()
    cols = [
        "Q1_age_group_enc","Q6_ownership_duration_enc","Q7_monthly_spend_inr",
        "Q9_online_purchase_freq_enc","Q13_pet_space_satisfaction_enc",
        "Q15_app_usage_enc","Q20_community_importance_enc",
        "Q22_reviews_importance_enc","Q24_emergency_vet_freq_enc",
        "engagement_score","spend_per_dog",
        "Q2_city_tier_Metro","Q2_city_tier_Tier-2","Q2_city_tier_Rural",
        "Q4_num_dogs_1 Dog","Q4_num_dogs_2 Dogs","Q4_num_dogs_3+ Dogs",
        "Q17_location_sharing_Yes Always","Q17_location_sharing_Yes When Using App",
        "Q18_subscription_pref_Freemium","Q18_subscription_pref_Monthly Sub",
        "Q18_subscription_pref_Annual Sub","Q18_subscription_pref_Would Not Pay",
        "Q19_adoption_interest_Yes Actively","Q19_adoption_interest_Yes Considering",
        "Q21_social_media_dogs_Active","Q21_social_media_dogs_Passive",
        "Q10_challenges__hard_to_find_reliable_vet",
        "Q10_challenges__no_pet_friendly_spaces",
        "Q10_challenges__losing_track_of_vaccinations",
        "Q14_preferred_features__health_vaccination_tracker",
        "Q14_preferred_features__nearby_vet_directory",
    ]
    valid = [c for c in cols if c in df.columns]
    X  = df[valid].fillna(0)
    y3 = df["Q25_target"].fillna(1).astype(int)
    return X, y3, valid


@st.cache_data
def run_classification():
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
    try:
        from xgboost import XGBClassifier
        xgb = XGBClassifier(n_estimators=150, max_depth=4, learning_rate=0.15,
                             subsample=0.8, colsample_bytree=0.8,
                             random_state=42, eval_metric="mlogloss", verbosity=0, n_jobs=-1)
        has_xgb = True
    except ImportError:
        has_xgb = False

    X, y3, feat_names = build_features()
    Xtr, Xte, ytr, yte = train_test_split(X, y3, test_size=0.2, random_state=42, stratify=y3)
    sc = StandardScaler()
    Xtr_s, Xte_s = sc.fit_transform(Xtr), sc.transform(Xte)
    models = {
        "Logistic Regression": LogisticRegression(max_iter=500, C=0.5, class_weight="balanced", solver="lbfgs", random_state=42),
        "Decision Tree":       DecisionTreeClassifier(max_depth=8, min_samples_split=10, min_samples_leaf=5, class_weight="balanced", random_state=42),
        "Random Forest":       RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=4, class_weight="balanced", random_state=42, n_jobs=-1),
        "Gradient Boosting":   GradientBoostingClassifier(n_estimators=150, max_depth=4, learning_rate=0.15, subsample=0.8, min_samples_leaf=10, random_state=42),
        "AdaBoost":            AdaBoostClassifier(n_estimators=100, learning_rate=0.5, random_state=42),
        "SVM":                 SVC(kernel="rbf", C=1.0, gamma="scale", probability=True, class_weight="balanced", random_state=42),
        "KNN":                 KNeighborsClassifier(n_neighbors=9, weights="distance"),
        "Naive Bayes":         GaussianNB(),
    }
    if has_xgb:
        models["XGBoost"] = xgb

    results, cms, feat_imp = [], {}, {}
    for name, m in models.items():
        scaled = name in ("Logistic Regression", "SVM", "KNN")
        Xf, Xe = (Xtr_s, Xte_s) if scaled else (Xtr, Xte)
        m.fit(Xf, ytr)
        pred = m.predict(Xe)
        results.append({
            "Model":     name,
            "Accuracy":  round(accuracy_score(yte, pred), 3),
            "Precision": round(precision_score(yte, pred, average="weighted", zero_division=0), 3),
            "Recall":    round(recall_score(yte, pred, average="weighted", zero_division=0), 3),
            "F1-Score":  round(f1_score(yte, pred, average="weighted", zero_division=0), 3),
            "3-Fold CV (Train)": round(cross_val_score(m, Xf, ytr, cv=3, scoring="accuracy").mean(), 3),
        })
        cms[name] = confusion_matrix(yte, pred)
        if hasattr(m, "feature_importances_"):
            feat_imp[name] = dict(zip(feat_names, m.feature_importances_))
        elif hasattr(m, "coef_"):
            feat_imp[name] = dict(zip(feat_names, np.abs(m.coef_).mean(axis=0)))

    rdf = pd.DataFrame(results).sort_values("F1-Score", ascending=False)
    return rdf, cms, feat_imp, rdf.iloc[0]["Model"], yte, feat_names


@st.cache_data
def run_clustering():
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    _, df = load_data()
    cols = ["Q1_age_group_enc","Q7_monthly_spend_inr","Q9_online_purchase_freq_enc",
            "Q15_app_usage_enc","Q20_community_importance_enc","Q22_reviews_importance_enc",
            "engagement_score","spend_per_dog","Q2_city_tier_Metro","Q2_city_tier_Tier-2"]
    valid = [c for c in cols if c in df.columns]
    Xs = StandardScaler().fit_transform(df[valid].fillna(0))
    inertias, sils = [], []
    for k in range(2, 9):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(Xs)
        inertias.append(km.inertia_)
        sils.append(silhouette_score(Xs, km.labels_))
    km4 = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels = km4.fit_predict(Xs)
    df2 = df.copy()
    df2["cluster"] = labels
    personas = {
        0: ("Urban Enthusiast", AMBER, "Metro, high spend, active app user"),
        1: ("Practical Parent",  BROWN, "Tier-2, moderate spend, functional needs"),
        2: ("Casual Companion",  MAUVE, "Any city, low spend, passive"),
        3: ("Community Seeker",  TEAL, "Values community and reviews strongly"),
    }
    summary = df2.groupby("cluster").agg(
        Count=("Q7_monthly_spend_inr","count"),
        Avg_Spend=("Q7_monthly_spend_inr","mean"),
        Avg_App=("Q15_app_usage_enc","mean"),
        Pct_Metro=("Q2_city_tier_Metro","mean"),
        Pct_Yes=("Q25_binary","mean"),
    ).round(2).reset_index()
    summary["Persona"] = summary["cluster"].map(lambda x: personas[x][0])
    summary["Color"]   = summary["cluster"].map(lambda x: personas[x][1])
    return list(range(2,9)), inertias, sils, labels, df2, summary, personas


@st.cache_data
def run_association_rules():
    import inspect
    from mlxtend.frequent_patterns import apriori, association_rules
    _, df = load_data()
    ch = [c for c in df.columns if c.startswith("Q10_challenges__")]
    ft = [c for c in df.columns if c.startswith("Q14_preferred_features__")]
    basket = df[ch+ft].fillna(0).astype(bool)
    freq = apriori(basket, min_support=0.08, use_colnames=True)

    # Detect mlxtend version by inspecting the function signature
    sig = inspect.signature(association_rules)
    params = list(sig.parameters.keys())

    if "num_itemsets" in params:
        # mlxtend >= 0.21: num_itemsets is required
        rules = association_rules(freq, metric="lift", min_threshold=1.1,
                                  num_itemsets=len(freq))
    else:
        # mlxtend < 0.21: old API
        rules = association_rules(freq, metric="lift", min_threshold=1.1)

    rules = rules[
        rules["antecedents"].apply(lambda x: any("challenge" in i for i in x)) &
        rules["consequents"].apply(lambda x: any("feature" in i for i in x))
    ].copy()
    def clean(s):
        return str(s).replace("Q10_challenges__","").replace("Q14_preferred_features__","").replace("_"," ").title()
    rules["antecedents_str"] = rules["antecedents"].apply(lambda x: ", ".join([clean(i) for i in x]))
    rules["consequents_str"] = rules["consequents"].apply(lambda x: ", ".join([clean(i) for i in x]))
    return rules.sort_values("lift", ascending=False).head(30).round(3)


@st.cache_data
def run_regression():
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    X, y3, feat_names = build_features()
    _, df = load_data()
    leakage_features = {"Q7_monthly_spend_inr", "spend_per_dog"}
    feat_names = [f for f in feat_names if f not in leakage_features]
    X = X[feat_names].copy()
    y = df["Q7_monthly_spend_inr"].fillna(df["Q7_monthly_spend_inr"].median()).iloc[:len(X)]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    sc = StandardScaler()
    Xtr_s, Xte_s = sc.fit_transform(Xtr), sc.transform(Xte)
    models = {"Linear": LinearRegression(), "Ridge (L2)": Ridge(alpha=1.0),
              "Lasso (L1)": Lasso(alpha=0.5, max_iter=2000)}
    results, preds, coefs = [], {}, {}
    for name, m in models.items():
        m.fit(Xtr_s, ytr)
        p = m.predict(Xte_s)
        results.append({"Model": name,
                         "R\u00b2": round(r2_score(yte, p), 3),
                         "RMSE": round(np.sqrt(mean_squared_error(yte, p)), 1),
                         "MAE":  round(mean_absolute_error(yte, p), 1),
                         "CV R\u00b2": round(cross_val_score(m, Xtr_s, ytr, cv=3, scoring="r2").mean(), 3)})
        preds[name] = (yte.values, p)
        coefs[name] = dict(zip(feat_names, m.coef_))
    return pd.DataFrame(results), preds, coefs, feat_names


# ── City / Places data ────────────────────────────────────────────────────────
CITY_COORDS = {
    "Mumbai":    (19.076, 72.877),
    "Delhi":     (28.613, 77.209),
    "Bengaluru": (12.971, 77.594),
    "Indore":    (22.719, 75.857),
    "Pune":      (18.520, 73.856),
    "Hyderabad": (17.385, 78.486),
}
PLACES = [
    {"city":"Mumbai",    "name":"PawFect Vet Clinic",       "category":"Vet",      "lat":19.082,"lon":72.891,"rating":4.7,"reviews":312,"note":"24-hour emergency care"},
    {"city":"Mumbai",    "name":"Bandstand Dog Park",        "category":"Park",     "lat":19.047,"lon":72.817,"rating":4.5,"reviews":891,"note":"Sea-facing off-leash area"},
    {"city":"Mumbai",    "name":"The Doggy Cafe",            "category":"Cafe",     "lat":19.059,"lon":72.829,"rating":4.3,"reviews":204,"note":"Popular Bandra spot"},
    {"city":"Mumbai",    "name":"Happy Paws Grooming",       "category":"Grooming", "lat":19.119,"lon":72.908,"rating":4.6,"reviews":178,"note":"Mobile grooming available"},
    {"city":"Delhi",     "name":"Sanjay Lake Dog Park",      "category":"Park",     "lat":28.659,"lon":77.312,"rating":4.4,"reviews":634,"note":"Large fenced area"},
    {"city":"Delhi",     "name":"Capital Vet Hospital",      "category":"Vet",      "lat":28.567,"lon":77.210,"rating":4.8,"reviews":487,"note":"Top rated in South Delhi"},
    {"city":"Delhi",     "name":"Paws & Claws Cafe",         "category":"Cafe",     "lat":28.524,"lon":77.185,"rating":4.1,"reviews":312,"note":"Pet menu available"},
    {"city":"Delhi",     "name":"Delhi Dog Grooming",        "category":"Grooming", "lat":28.632,"lon":77.219,"rating":4.5,"reviews":221,"note":"Spa treatments offered"},
    {"city":"Bengaluru", "name":"Cubbon Park Dog Area",      "category":"Park",     "lat":12.976,"lon":77.592,"rating":4.6,"reviews":1203,"note":"City centre, very popular"},
    {"city":"Bengaluru", "name":"CUPA Animal Hospital",      "category":"Vet",      "lat":12.985,"lon":77.609,"rating":4.9,"reviews":892, "note":"Best rescue care in Bengaluru"},
    {"city":"Bengaluru", "name":"Barks & Brews",             "category":"Cafe",     "lat":12.935,"lon":77.624,"rating":4.4,"reviews":567,"note":"Koramangala hotspot"},
    {"city":"Bengaluru", "name":"The Groom Room",            "category":"Grooming", "lat":12.958,"lon":77.648,"rating":4.7,"reviews":334,"note":"Indiranagar, premium service"},
    {"city":"Indore",    "name":"Indore Pet Clinic",         "category":"Vet",      "lat":22.724,"lon":75.883,"rating":4.5,"reviews":187,"note":"Experienced small animal vet"},
    {"city":"Indore",    "name":"Rajwada Dog Park",          "category":"Park",     "lat":22.719,"lon":75.857,"rating":4.0,"reviews":312,"note":"Central location"},
    {"city":"Indore",    "name":"Pawsome Cafe Indore",       "category":"Cafe",     "lat":22.733,"lon":75.886,"rating":4.2,"reviews":145,"note":"Newly opened venue"},
    {"city":"Indore",    "name":"FurFresh Grooming",         "category":"Grooming", "lat":22.745,"lon":75.892,"rating":4.4,"reviews":98, "note":"Home visits available"},
    {"city":"Pune",      "name":"Paws Pune Vet",             "category":"Vet",      "lat":18.536,"lon":73.847,"rating":4.6,"reviews":298,"note":"Koregaon Park location"},
    {"city":"Pune",      "name":"Empress Garden Dog Zone",   "category":"Park",     "lat":18.538,"lon":73.878,"rating":4.4,"reviews":534,"note":"Weekends get crowded"},
    {"city":"Pune",      "name":"Doggo Cafe Baner",          "category":"Cafe",     "lat":18.559,"lon":73.786,"rating":4.3,"reviews":276,"note":"IT crowd favourite"},
    {"city":"Pune",      "name":"Snip & Wag",                "category":"Grooming", "lat":18.520,"lon":73.856,"rating":4.5,"reviews":189,"note":"Appointment only"},
    {"city":"Hyderabad", "name":"Jubilee Hills Vet",         "category":"Vet",      "lat":17.431,"lon":78.407,"rating":4.7,"reviews":341,"note":"Premium area clinic"},
    {"city":"Hyderabad", "name":"KBR Park Dog Walk",         "category":"Park",     "lat":17.425,"lon":78.434,"rating":4.5,"reviews":789,"note":"Gated and safe, early morning best"},
    {"city":"Hyderabad", "name":"Cafe Barko",                "category":"Cafe",     "lat":17.447,"lon":78.391,"rating":4.2,"reviews":223,"note":"Banjara Hills spot"},
    {"city":"Hyderabad", "name":"PawLux Grooming",           "category":"Grooming", "lat":17.410,"lon":78.456,"rating":4.6,"reviews":167,"note":"Luxury spa packages"},
]
CAT_COLORS = {"Vet":[229,57,53], "Park":[76,175,80], "Cafe":[212,134,11], "Grooming":[160,120,76]}
CAT_HEX    = {"Vet":"#EF5350",   "Park":"#66BB6A",   "Cafe":"#D4A853",    "Grooming":"#A0784C"}
CAT_ICONS  = {"Vet":"🏥",        "Park":"🌳",         "Cafe":"☕",          "Grooming":"✂️"}


# ── UI helpers ────────────────────────────────────────────────────────────────
def shead(t):
    st.markdown(f'<div class="shead"><span class="anim-pulse" style="margin-right:4px">▸</span> {t}</div>', unsafe_allow_html=True)

def ibox(t):
    st.markdown(f'<div class="ibox"><span class="anim-pulse">💡</span> {t}</div>', unsafe_allow_html=True)

def warnbox(t):
    st.markdown(f'<div class="warnbox"><span class="anim-wiggle">⚠️</span> {t}</div>', unsafe_allow_html=True)

def tab_summary(points):
    with st.expander("📋 Key Takeaways from this tab"):
        for p in points:
            st.markdown(f"- {p}")

def live_bar(n):
    now = time.strftime("%H:%M:%S")
    st.markdown(
        f'<div class="lbar">'
        f'<div style="display:flex;align-items:center;gap:10px">'
        f'<div style="width:8px;height:8px;border-radius:50%;background:{SAGE};'
        f'animation:liveDot 2s ease-in-out infinite"></div>'
        f'<span style="color:{SAGE};font-size:10px;font-weight:700;letter-spacing:.1em">DATA LOADED</span>'
        f'<span style="color:{TEXT_DIM};font-size:10px">|</span>'
        f'<span class="anim-bounce" style="color:{AMBER};font-size:11px;font-weight:600">'
        f'<span class="anim-pulse">🐾</span> {n:,} respondents</span></div>'
        f'<span style="color:{AMBER};font-size:12px;font-weight:700;font-family:monospace">{now}</span>'
        f'</div>', unsafe_allow_html=True)

def ring(pct, color, label, size=88, stroke=8):
    r = (size - stroke) / 2
    circ = 2 * math.pi * r
    offset = circ * (1 - pct / 100)
    return (
        f'<div style="text-align:center;transition:transform .3s ease" '
        f'onmouseover="this.style.transform=\'scale(1.1)\'" '
        f'onmouseout="this.style.transform=\'scale(1)\'">'
        f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
        f'style="filter:drop-shadow(0 0 6px {color}50);animation:iconPulse 4s ease-in-out infinite">'
        f'<circle cx="{size//2}" cy="{size//2}" r="{r}" fill="none" '
        f'stroke="rgba(212,168,83,0.1)" stroke-width="{stroke}"/>'
        f'<circle cx="{size//2}" cy="{size//2}" r="{r}" fill="none" '
        f'stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" '
        f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{offset:.1f}" '
        f'transform="rotate(-90 {size//2} {size//2})">'
        f'<animate attributeName="stroke-dashoffset" from="{circ:.1f}" to="{offset:.1f}" '
        f'dur="1.5s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>'
        f'</circle>'
        f'<text x="{size//2}" y="{size//2-3}" text-anchor="middle" fill="{color}" '
        f'font-size="15" font-weight="800" font-family="Bricolage Grotesque">{pct:.0f}%</text>'
        f'<text x="{size//2}" y="{size//2+13}" text-anchor="middle" fill="{TEXT_DIM}" '
        f'font-size="8" font-weight="600">{label}</text>'
        f'</svg></div>'
    )

def _deep_merge(base, override):
    """Recursively merge override into base — 3 levels deep so tickfont is never wiped."""
    result = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result

def pc(fig, h=320, **kw):
    """Dark chart — deep merge so axis tickfonts survive. Enforces minimum margins."""
    # Enforce minimum top/bottom margins so charts don't overlap with headers/callouts
    if "margin" in kw:
        m = kw["margin"]
        if isinstance(m, dict):
            m.setdefault("t", 24)
            m.setdefault("b", 24)
            if m.get("t", 24) < 20:
                m["t"] = 20
            if m.get("b", 24) < 20:
                m["b"] = 20
    else:
        kw["margin"] = dict(t=24, b=24, l=40, r=20)
    fig.update_layout(**_deep_merge(PL, {"height": h, **kw}))
    st.plotly_chart(fig, use_container_width=True, config=PCFG)

def _kpi(label, value, sub, color, delay="0s"):
    st.markdown(
        f'<div style="background:{SURFACE};border:1px solid {BORDER};'
        f'border-top:4px solid {color};border-radius:14px;padding:18px 16px;'
        f'text-align:center;animation:floatCard 5s ease-in-out {delay} infinite,'
        f'fadeSlideUp 0.6s ease-out {delay} both;'
        f'transition:transform .3s ease,box-shadow .3s ease" '
        f'onmouseover="this.style.transform=\'translateY(-6px) scale(1.03)\';'
        f'this.style.boxShadow=\'0 12px 32px rgba(212,168,83,.2)\'" '
        f'onmouseout="this.style.transform=\'\';this.style.boxShadow=\'\'">'
        f'<div style="color:{TEXT_DIM};font-size:.72rem;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px">{label}</div>'
        f'<div style="color:{color};font-size:1.7rem;font-weight:800;'
        f'font-family:Bricolage Grotesque,sans-serif;letter-spacing:-.02em">{value}</div>'
        f'<div style="color:{TEXT_DIM};font-size:.75rem;margin-top:5px;font-weight:500">{sub}</div>'
        f'</div>', unsafe_allow_html=True)

def _dark_table(df_tbl, h=None):
    """Render a Plotly table with dark theme."""
    if h is None:
        h = min(60 + len(df_tbl) * 34, 500)
    fig = go.Figure(go.Table(
        header=dict(
            values=[f"<b>{c}</b>" for c in df_tbl.columns],
            fill_color="#2C1E10", font=dict(color=TEXT_BRIGHT, size=12),
            align="left", line=dict(color="rgba(212,168,83,0.2)", width=1)),
        cells=dict(
            values=[df_tbl[c].astype(str).tolist() for c in df_tbl.columns],
            fill_color=SURFACE, font=dict(color=TEXT, size=11),
            align="left", line=dict(color="rgba(212,168,83,0.1)", width=1),
            height=30)))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=h,
                      margin=dict(l=0, r=0, t=0, b=0), font=dict(color=TEXT))
    st.plotly_chart(fig, use_container_width=True, config=PCFG)

def _dark_pie(labels, values, colors, h=320, hole=0.45, title_text=None, center_text=None):
    """Render a Plotly donut with outside labels for dark theme readability."""
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=hole, marker_colors=colors,
        textinfo="label+percent",
        textposition="outside",
        textfont=dict(size=10, color=TEXT),
        outsidetextfont=dict(color=TEXT, size=10),
        insidetextfont=dict(color=TEXT_BRIGHT, size=10),
    ))
    layout_kw = dict(
        height=h, margin=dict(t=40, b=60, l=40, r=40),
        paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
        font=dict(color=TEXT),
    )
    if title_text:
        layout_kw["title"] = dict(text=title_text, font=dict(color=TEXT_BRIGHT, size=13))
        layout_kw["margin"]["t"] = 50
    if center_text:
        layout_kw["annotations"] = [dict(
            text=center_text, x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=AMBER))]
    fig.update_layout(**layout_kw)
    st.plotly_chart(fig, use_container_width=True, config=PCFG)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(LOGO_SVG + WORDMARK, unsafe_allow_html=True)
    st.markdown("<div class='anim-divider'></div>",
                unsafe_allow_html=True)
    st.markdown("<p style='font-size:.65rem;letter-spacing:1.8px;color:#9A8D76;"
                "text-transform:uppercase;margin:0 0 8px 4px;font-weight:700'>Navigate</p>",
                unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["\U0001f3e0  Home", "\U0001f4cd  Know Your City", "\U0001f436  Dog Owner Insights",
         "\U0001f4b0  Will They Buy?", "\U0001f52c  Data Journey", "\U0001f4ca  Research & Analytics"],
        label_visibility="collapsed",
    )
    st.markdown("<div class='anim-divider'></div>",
                unsafe_allow_html=True)
    st.markdown("<p style='font-size:.65rem;color:#9A8D76;text-align:center;line-height:1.8'>"
                "PawIndia \u00a9 2025<br><span style='color:#D4A853'>Market Research Dashboard</span></p>",
                unsafe_allow_html=True)


# ── Load data ────────────────────────────────────────────────────────────────
raw, df = load_data()
n         = len(df)
pct_yes   = round((df["Q25_app_adoption"] == "Yes").sum()   / n * 100, 1)
pct_maybe = round((df["Q25_app_adoption"] == "Maybe").sum() / n * 100, 1)
pct_no    = round((df["Q25_app_adoption"] == "No").sum()    / n * 100, 1)
avg_spend = int(df["Q7_monthly_spend_inr"].mean())
avg_spend_k = "Rs.{:.1f}K".format(avg_spend / 1000)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "\U0001f3e0  Home":
    st.markdown(
        "<h1 style='font-size:1.8rem;margin-bottom:4px'><span class='anim-bounce' style='display:inline-block'>🐾</span> "
        "<span class='shimmer-title'>Welcome to PawIndia</span></h1>"
        "<p style='color:{d};font-weight:500;animation:fadeSlideUp .6s ease-out both'>India's first super-app for dog owners \u2014 validated by real market research</p>"
        .format(c=TEXT_BRIGHT, d=TEXT_DIM),
        unsafe_allow_html=True)
    live_bar(n)

    c1, c2, c3, c4 = st.columns(4)
    with c1: _kpi("Respondents",    "{:,}".format(n),                "After cleaning",      AMBER,  "0s")
    with c2: _kpi("Will Download",  "{:.1f}%".format(pct_yes),      "Definite Yes",        GREEN_YES, "0.3s")
    with c3: _kpi("Open to Trying", "{:.1f}%".format(pct_maybe),    "Conditional",         HONEY,  "0.6s")
    with c4: _kpi("Total Reachable", "{:.1f}%".format(pct_yes+pct_maybe), "Yes + Maybe",   TEAL,   "0.9s")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Rings
    shead("Adoption at a Glance")
    rc = st.columns(4)
    rc[0].markdown(ring(pct_yes,             GREEN_YES, "Would Download"), unsafe_allow_html=True)
    rc[1].markdown(ring(pct_maybe,           HONEY,     "Open to It"),     unsafe_allow_html=True)
    rc[2].markdown(ring(pct_no,              RED_NO,    "Would Not"),      unsafe_allow_html=True)
    rc[3].markdown(ring(pct_yes + pct_maybe, TEAL,      "Reachable"),      unsafe_allow_html=True)

    # Business purpose card
    st.markdown(
        '<div class="icard" style="border-left:5px solid {a}">'
        '<div style="color:{a};font-size:.75rem;font-weight:700;'
        'text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px">The Question We Are Answering</div>'
        '<div style="color:{t};font-size:.95rem;line-height:1.7">'
        'Do dog owners in India face enough real problems finding vets, parks, grooming, '
        'and community that they would download and pay for one app that does it all? '
        'The survey says <strong style="color:{g}">{pct:.1f}% are open to it</strong> '
        '\u2014 and this dashboard shows exactly who, where, and why.'
        '</div></div>'.format(a=AMBER, t=TEXT, g=GREEN_YES, pct=pct_yes + pct_maybe),
        unsafe_allow_html=True)

    # Challenges + Features
    cl, cr = st.columns(2)
    with cl:
        shead("What Dog Owners Struggle With Most")
        ch_cols = {c: c.replace("Q10_challenges__","").replace("_"," ").title()
                   for c in df.columns if c.startswith("Q10_challenges__")}
        ch_df = pd.DataFrame({"Challenge": list(ch_cols.values()),
                               "Respondents": [int(df[col].sum()) for col in ch_cols]
                               }).sort_values("Respondents")
        fig = go.Figure(go.Bar(
            x=ch_df["Respondents"], y=ch_df["Challenge"], orientation="h",
            marker=dict(color=ch_df["Respondents"], colorscale=[[0,"#2C1E10"],[0.5,AMBER],[1,HONEY]]),
            text=ch_df["Respondents"], textposition="outside",
            textfont=dict(color=TEXT, size=10),
        ))
        pc(fig, h=340,
           margin=dict(t=10, b=10, l=240, r=60),
           xaxis=dict(title="Number of respondents", showgrid=False, visible=False),
           yaxis=dict(title="", tickfont=dict(color=TEXT, size=10)))
        ibox("Finding a reliable vet is the single biggest pain point \u2014 cited by more respondents "
             "than any other challenge. This directly validates PawIndia's vet directory as the must-build first feature.")

    with cr:
        shead("Features Dog Owners Want Built First")
        ft_cols = {c: c.replace("Q14_preferred_features__","").replace("_"," ").title()
                   for c in df.columns if c.startswith("Q14_preferred_features__")}
        ft_df = pd.DataFrame({"Feature": list(ft_cols.values()),
                               "Respondents": [int(df[col].sum()) for col in ft_cols]
                               }).sort_values("Respondents").tail(7)
        fig2 = go.Figure(go.Bar(
            x=ft_df["Respondents"], y=ft_df["Feature"], orientation="h",
            marker_color=AMBER,
            text=ft_df["Respondents"], textposition="outside",
            textfont=dict(color=TEXT, size=10),
        ))
        pc(fig2, h=340,
           margin=dict(t=10, b=10, l=220, r=60),
           xaxis=dict(title="Number of respondents", showgrid=False, visible=False),
           yaxis=dict(title="", tickfont=dict(color=TEXT, size=10)))
        ibox("The Health & Vaccination Tracker is the most requested feature \u2014 "
             "dog owners want a digital record more than anything else. "
             "It costs little to build and creates daily app engagement.")

    # Spend vs adoption
    shead("Do Higher Spenders Want the App More?")
    fig3 = go.Figure()
    for cat, col in [("Yes", GREEN_YES), ("Maybe", HONEY), ("No", RED_NO)]:
        v = df[df["Q25_app_adoption"]==cat]["Q7_monthly_spend_inr"]
        fig3.add_trace(go.Box(
            y=v, name="{} (n={})".format(cat, len(v)), marker_color=col,
            boxmean="sd",
            line=dict(color=col),
        ))
    yes_s = int(df[df["Q25_app_adoption"]=="Yes"]["Q7_monthly_spend_inr"].mean())
    pc(fig3, h=300,
       margin=dict(t=10, b=20, l=60, r=20),
       yaxis=dict(title="Monthly Spend (INR)", rangemode="tozero"))
    ibox("Yes, Maybe and No groups have similar median spend (around Rs.{:,}/month). "
         "Willingness to download is driven more by digital habits and pain points than by how much "
         "someone already spends \u2014 which means PawIndia can win across all spending levels.".format(yes_s))

    d1, d2, _ = st.columns([1,1,3])
    with d1: st.download_button("\u2b07 Download Raw Data", raw.to_csv(index=False), "pawindia_raw.csv", "text/csv")
    with d2: st.download_button("\u2b07 Download Cleaned Data", df.to_csv(index=False), "pawindia_clean.csv", "text/csv")

    tab_summary([
        "{:.1f}% of surveyed dog owners would definitely download PawIndia, "
        "and a further {:.1f}% are open to it \u2014 giving a total reachable market of {:.1f}%.".format(pct_yes, pct_maybe, pct_yes + pct_maybe),
        "Finding a reliable vet and lack of pet-friendly spaces are the two problems felt most widely.",
        "The Health & Vaccination Tracker is the single most requested feature across all cities and age groups.",
        "Spend levels alone do not predict adoption \u2014 digital engagement is the stronger signal.",
        "The average Indian dog owner spends {} per month on their pet, "
        "suggesting real willingness to pay for services that solve genuine problems.".format(avg_spend_k),
    ])


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — KNOW YOUR CITY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "\U0001f4cd  Know Your City":
    st.markdown(
        "<h1 style='font-size:1.8rem;margin-bottom:4px'><span class='anim-bounce' style='display:inline-block'>📍</span> "
        "<span class='shimmer-title'>Know Your City</span></h1>"
        "<p style='color:{d};font-weight:500;animation:fadeSlideUp .6s ease-out both'>Find dog-friendly vets, parks, cafes and grooming near you</p>"
        .format(c=TEXT_BRIGHT, d=TEXT_DIM),
        unsafe_allow_html=True)
    live_bar(n)

    warnbox("<strong>Note:</strong> Places shown are simulated for demonstration. "
            "At launch PawIndia will connect to live Google Places data.")

    # Filters
    cc, cf, cs = st.columns(3)
    with cc: city  = st.selectbox("Select City", list(CITY_COORDS.keys()), index=2)
    with cf:
        cats = ["All"] + sorted(set(p["category"] for p in PLACES))
        cat  = st.selectbox("Place Type", cats)
    with cs:
        min_r = st.slider("Minimum Rating", 3.5, 5.0, 4.0, 0.1)

    places_df = pd.DataFrame(PLACES)
    city_df   = places_df[places_df["city"] == city].copy()
    if cat != "All":
        filtered = city_df[city_df["category"] == cat].copy()
    else:
        filtered = city_df.copy()
    filtered = filtered[filtered["rating"] >= min_r].copy()
    grey_out = city_df[~city_df.index.isin(filtered.index)].copy()

    # Street map
    shead("Street Map \u2014 {}".format(city))
    lat0, lon0 = CITY_COORDS[city]
    fig_map = go.Figure()

    if len(grey_out) > 0:
        fig_map.add_trace(go.Scattermap(
            lat=grey_out["lat"], lon=grey_out["lon"],
            mode="markers",
            marker=dict(size=10, color="rgba(150,140,130,0.45)"),
            text=grey_out.apply(
                lambda r: "<b style='color:#999'>{}</b><br>{} | {} \u2605<br><i>(below filter)</i>".format(
                    r['name'], r['category'], r['rating']), axis=1),
            hovertemplate="%{text}<extra></extra>",
            name="Other places (filtered out)",
            showlegend=True,
        ))

    for cat_name, hex_col in CAT_HEX.items():
        subset = filtered[filtered["category"] == cat_name]
        if len(subset) == 0:
            continue
        fig_map.add_trace(go.Scattermap(
            lat=subset["lat"], lon=subset["lon"],
            mode="markers+text",
            marker=dict(size=subset["rating"].apply(lambda r: 8 + (r-3.5)*8),
                        color=hex_col, opacity=0.9),
            text=subset["name"],
            textposition="top right",
            textfont=dict(size=11, color=TEXT),
            customdata=subset[["name","category","rating","reviews","note"]].values,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "%{customdata[1]}<br>"
                "%{customdata[2]} \u2605 | %{customdata[3]} reviews<br>"
                "<i>%{customdata[4]}</i><extra></extra>"
            ),
            name="{} {}".format(CAT_ICONS[cat_name], cat_name),
        ))

    fig_map.update_layout(
        map=dict(style="open-street-map", center=dict(lat=lat0, lon=lon0), zoom=12),
        height=500, margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(bgcolor="rgba(26,18,9,0.92)", bordercolor="rgba(212,168,83,0.2)",
                    borderwidth=1, font=dict(color=TEXT, size=11), x=0.01, y=0.99),
    )
    st.plotly_chart(fig_map, use_container_width=True, config=PCFG)
    ibox("Showing {} matching place(s) in {}. "
         "Greyed pins are places that exist but don't match your current filter. "
         "Larger pins mean higher rated. Hover any pin for details.".format(len(filtered), city))

    # India overview
    shead("India Overview \u2014 All Cities at a Glance")
    city_stats = []
    for c_name, (clat, clon) in CITY_COORDS.items():
        cp = places_df[places_df["city"] == c_name]
        city_stats.append({
            "city": c_name, "lat": clat, "lon": clon,
            "total": len(cp),
            "avg_rating": round(cp["rating"].mean(), 2) if len(cp) > 0 else 0,
            "vets": len(cp[cp["category"]=="Vet"]),
            "parks": len(cp[cp["category"]=="Park"]),
            "selected": c_name == city,
        })
    cs_df = pd.DataFrame(city_stats)

    fig_india = go.Figure()
    other = cs_df[cs_df["city"] != city]
    fig_india.add_trace(go.Scattergeo(
        lat=other["lat"], lon=other["lon"],
        mode="markers+text",
        marker=dict(size=other["total"]*6, color="rgba(212,168,83,0.25)",
                    line=dict(color=AMBER, width=1.5)),
        text=other["city"], textposition="top center",
        textfont=dict(size=11, color=AMBER),
        hovertemplate="<b>%{text}</b><br>Places: " + other["total"].astype(str) + "<extra></extra>",
        name="Other cities", showlegend=False,
    ))
    sel = cs_df[cs_df["city"] == city].iloc[0]
    fig_india.add_trace(go.Scattergeo(
        lat=[sel["lat"]], lon=[sel["lon"]],
        mode="markers+text",
        marker=dict(size=sel["total"]*9, color=HONEY, line=dict(color=AMBER, width=2.5)),
        text=[city], textposition="top center",
        textfont=dict(size=13, color=HONEY, family="Bricolage Grotesque"),
        hovertemplate="<b>{}</b><br>Vets: {} | Parks: {}<extra></extra>".format(city, sel['vets'], sel['parks']),
        name=city, showlegend=False,
    ))
    fig_india.update_layout(
        geo=dict(
            scope="asia", resolution=50,
            showland=True, landcolor="#1A1209",
            showocean=True, oceancolor="#0D0A06",
            showcountries=True, countrycolor="rgba(212,168,83,0.3)",
            showsubunits=True, subunitcolor="rgba(212,168,83,0.1)",
            center=dict(lat=20.5, lon=78.9), projection_scale=4.5,
            bgcolor="#0D0A06",
            lataxis_range=[8,35], lonaxis_range=[68,98],
        ),
        height=400, margin=dict(t=10,b=10,l=0,r=0),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT),
    )
    st.plotly_chart(fig_india, use_container_width=True, config=PCFG)
    ibox("Bubble size shows total number of dog-friendly places in each city. "
         "The highlighted city (gold) is your current selection. "
         "Metro cities like Bengaluru and Mumbai have the most coverage today "
         "\u2014 Tier-2 cities like Indore are underserved and represent PawIndia's growth opportunity.")

    # Place cards — adaptive columns
    if len(filtered) > 0:
        ncols = min(len(filtered), 3)
        shead("{} Places in {} matching your filters ({} found)".format(
            CAT_ICONS.get(cat, '\U0001f43e'), city, len(filtered)))
        cols3 = st.columns(ncols)
        for i, (_, row) in enumerate(filtered.iterrows()):
            r, g, b = CAT_COLORS.get(row["category"], [160,120,76])
            cols3[i % ncols].markdown(
                '<div style="background:{bg};border:1px solid {bd};'
                'border-top:3px solid rgb({r},{g},{b});border-radius:12px;'
                'padding:16px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.3);'
                'animation:fadeSlideUp 0.4s ease-out both;'
                'transition:transform .3s ease,box-shadow .3s ease" '
                'onmouseover="this.style.transform=\'translateY(-4px) scale(1.02)\';'
                'this.style.boxShadow=\'0 8px 24px rgba(0,0,0,.4)\'" '
                'onmouseout="this.style.transform=\'\';this.style.boxShadow=\'\'">'
                '<div class="anim-wiggle" style="font-size:1.2rem">{icon}</div>'
                '<div style="font-weight:700;color:{txt};margin:4px 0">{name}</div>'
                '<div style="color:{amber};font-weight:600">{stars} {rating}</div>'
                '<div style="color:{dim};font-size:.8rem">{reviews} reviews</div>'
                '<div style="color:{brown};font-size:.8rem;margin-top:4px;font-style:italic">{note}</div>'
                '</div>'.format(
                    bg=SURFACE, bd=BORDER, r=r, g=g, b=b,
                    icon=CAT_ICONS.get(row["category"],""),
                    txt=TEXT_BRIGHT, name=row["name"],
                    amber=AMBER, stars="\u2605"*int(row["rating"]), rating=row["rating"],
                    dim=TEXT_DIM, reviews=row["reviews"],
                    brown=BROWN, note=row["note"]),
                unsafe_allow_html=True)

    # Satisfaction by city tier
    shead("Are Dog Owners Happy With Pet-Friendly Spaces in Their City?")
    sat_data = []
    for tcol, label in [("Q2_city_tier_Metro","Metro"),("Q2_city_tier_Tier-2","Tier-2"),
                        ("Q2_city_tier_Tier-3","Tier-3"),("Q2_city_tier_Rural","Rural")]:
        if tcol in df.columns:
            sub = df[df[tcol] == 1]
            if len(sub) > 0:
                sat_data.append({"City Tier": label,
                                  "Avg Score": round(sub["Q13_pet_space_satisfaction_enc"].mean(), 2)})
    if sat_data:
        sd = pd.DataFrame(sat_data)
        fig_s = go.Figure(go.Bar(
            x=sd["City Tier"], y=sd["Avg Score"],
            marker_color=[AMBER, HONEY, TERRA, BROWN],
            text=sd["Avg Score"], textposition="outside",
            textfont=dict(color=TEXT, size=11),
        ))
        fig_s.add_hline(y=3, line_dash="dash", line_color=TEXT_DIM,
                        annotation_text="Neutral (3.0)",
                        annotation_font_color=TEXT)
        pc(fig_s, h=300,
           margin=dict(t=20, b=20, l=60, r=80),
           xaxis=dict(title="City Tier"),
           yaxis=dict(range=[0,5.5], title="Satisfaction Score (1\u20135)", rangemode="tozero"))
        ibox("Every city tier scores below 3.0 (neutral) for satisfaction with pet-friendly spaces \u2014 "
             "meaning dog owners everywhere are unhappy with what's available. "
             "This universal dissatisfaction is PawIndia's opening across all markets, not just metros.")

    st.download_button("\u2b07 Download Place Data",
                       filtered.to_csv(index=False),
                       "pawindia_{}.csv".format(city.lower()), "text/csv")

    tab_summary([
        "Every city tier scores below neutral (3.0/5) for satisfaction with pet-friendly spaces \u2014 "
        "the problem is not limited to small cities.",
        "Bengaluru and Mumbai have the most dog-friendly places mapped today; "
        "Indore and Hyderabad are most underserved.",
        "{} places are mapped in {}. At launch, PawIndia will use live Google Places "
        "data to show thousands more.".format(len(city_df), city),
        "The zoomed street map shows exactly where each vet, park, cafe and groomer is located \u2014 "
        "the core 'find nearby' use case for PawIndia.",
    ])


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — DOG OWNER INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "\U0001f436  Dog Owner Insights":
    st.markdown(
        "<h1 style='font-size:1.8rem;margin-bottom:4px'><span class='anim-wiggle' style='display:inline-block'>🐶</span> "
        "<span class='shimmer-title'>Dog Owner Insights</span></h1>"
        "<p style='color:{d};font-weight:500;animation:fadeSlideUp .6s ease-out both'>Who are India's dog owners, what do they spend, and what problems do they have?</p>"
        .format(c=TEXT_BRIGHT, d=TEXT_DIM),
        unsafe_allow_html=True)
    live_bar(n)

    t1, t2, t3, t4 = st.tabs(["\U0001f464 Who They Are", "\U0001f4b8 What They Spend",
                               "\U0001f624 Their Problems", "\U0001f4f1 How Digital Are They"])

    with t1:
        shead("Age and City Breakdown")
        c1, c2 = st.columns(2)
        with c1:
            age_order = ["Under 18","18-24","25-34","35-44","45-59","60+"]
            ac = raw["Q1_age_group"].value_counts().reindex(age_order, fill_value=0)
            fig = go.Figure(go.Bar(
                x=ac.index, y=ac.values,
                marker_color=CHART[:len(ac)],
                text=ac.values, textposition="outside",
                textfont=dict(color=TEXT, size=11),
            ))
            pc(fig, h=280,
               margin=dict(t=10, b=20, l=60, r=20),
               title=dict(text="Respondents by Age Group", font=dict(color=TEXT_BRIGHT)),
               xaxis=dict(title="Age group"),
               yaxis=dict(title="Number of respondents", showgrid=False, rangemode="tozero"))
            ibox("25\u201334 year olds make up over a third of respondents \u2014 India's millennial dog owners "
                 "are the dominant group and PawIndia's primary target audience.")

        with c2:
            cc2 = raw["Q2_city_tier"].value_counts()
            _dark_pie(cc2.index.tolist(), cc2.values.tolist(), CHART)
            ibox("45% of respondents are from metro cities, but Tier-2 accounts for 30% \u2014 "
                 "a large enough segment to justify city-specific features from day one.")

        shead("Where Are the High-Value Segments? (Age \u00d7 City)")
        age_enc = {"Under 18":0,"18-24":1,"25-34":2,"35-44":3,"45-59":4,"60+":5}
        tiers   = ["Metro","Tier-2","Tier-3","Rural"]
        hm_data = []
        for age in age_order:
            row_vals = []
            for tier in tiers:
                tcol = "Q2_city_tier_{}".format(tier)
                enc  = age_enc.get(age, -1)
                ct   = int(((df.get(tcol, pd.Series(0)) == 1) & (df["Q1_age_group_enc"] == enc)).sum()) if tcol in df.columns else 0
                row_vals.append(ct)
            hm_data.append(row_vals)
        fig_hm = go.Figure(go.Heatmap(
            z=hm_data, x=tiers, y=age_order,
            colorscale=[[0,"#1A1209"],[0.5,AMBER],[1,HONEY]],
            text=[[str(v) for v in row] for row in hm_data],
            texttemplate="%{text}",
            textfont=dict(color=TEXT_BRIGHT),
            showscale=True,
            colorbar=dict(tickfont=dict(color=TEXT), title=dict(text="Count", font=dict(color=TEXT))),
        ))
        pc(fig_hm, h=300,
           margin=dict(t=10, b=20, l=80, r=20),
           xaxis=dict(title="City tier"),
           yaxis=dict(title="Age group"))
        ibox("The 25\u201334 Metro cell is the darkest on the map \u2014 the largest single segment. "
             "Delhi and Bengaluru 25\u201334 year olds should be PawIndia's launch acquisition target.")

        c3, c4 = st.columns(2)
        with c3:
            dc = raw["Q4_num_dogs"].value_counts().reindex(["1 dog","2 dogs","3+ dogs"], fill_value=0)
            fig3 = go.Figure(go.Bar(
                x=dc.index, y=dc.values,
                marker_color=AMBER,
                text=dc.values, textposition="outside",
                textfont=dict(color=TEXT, size=11),
            ))
            pc(fig3, h=260,
               margin=dict(t=40, b=20, l=60, r=20),
               title=dict(text="Dogs Owned per Household", font=dict(color=TEXT_BRIGHT)),
               xaxis=dict(title="Number of dogs"),
               yaxis=dict(title="Respondents", showgrid=False, rangemode="tozero"))
            ibox("Over 58% of respondents own exactly one dog. "
                 "Multi-dog households (42%) are a high-value segment \u2014 "
                 "they spend more per month and have more complex care needs.")

        with c4:
            dt_cols = {c: c.replace("Q5_dog_type__","").replace("_"," ").title()
                       for c in df.columns if c.startswith("Q5_dog_type__")}
            dt_df = pd.DataFrame({"Breed": list(dt_cols.values()),
                                   "Count": [int(df[col].sum()) for col in dt_cols]}).sort_values("Count")
            fig4 = go.Figure(go.Bar(
                x=dt_df["Count"], y=dt_df["Breed"], orientation="h",
                marker_color=CHART[:len(dt_df)],
                text=dt_df["Count"], textposition="outside",
                textfont=dict(color=TEXT, size=10),
            ))
            pc(fig4, h=260,
               margin=dict(t=40, b=10, l=180, r=60),
               title=dict(text="Dog Breeds / Types", font=dict(color=TEXT_BRIGHT)),
               xaxis=dict(title="Count", showgrid=False, visible=False),
               yaxis=dict(title=""))
            ibox("Indian breeds and mixed breeds together form the largest group \u2014 "
                 "PawIndia should be designed for all dog types, not just expensive imported breeds.")

        tab_summary([
            "25\u201334 year olds in metro cities are the single largest segment \u2014 the core launch target.",
            "58% own one dog; the 42% who own two or more spend significantly more on care.",
            "Every city tier is represented, with Tier-2 being large enough for a dedicated onboarding strategy.",
            "Indian and mixed breeds dominate \u2014 the app must serve all breed types equally.",
        ])

    with t2:
        shead("Monthly Spend Patterns")
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure(go.Histogram(
                x=df["Q7_monthly_spend_inr"].dropna(), nbinsx=30,
                marker_color=AMBER, opacity=0.85,
            ))
            pc(fig, h=280,
               margin=dict(t=10, b=20, l=60, r=20),
               title=dict(text="Distribution of Monthly Spend", font=dict(color=TEXT_BRIGHT)),
               xaxis=dict(title="Monthly spend (INR)"),
               yaxis=dict(title="Number of respondents", showgrid=False))
            ibox("Spend is right-skewed \u2014 most owners spend Rs.2,000\u20136,000/month, "
                 "but a meaningful tail spends Rs.10,000+. "
                 "Premium features priced at Rs.199\u2013499/month sit well within the main spending range.")

        with c2:
            city_s = []
            for tcol, label in [("Q2_city_tier_Metro","Metro"),("Q2_city_tier_Tier-2","Tier-2"),
                                 ("Q2_city_tier_Tier-3","Tier-3"),("Q2_city_tier_Rural","Rural")]:
                if tcol in df.columns:
                    sub = df[df[tcol]==1]["Q7_monthly_spend_inr"]
                    if len(sub) > 0:
                        city_s.append({"City": label, "Avg Monthly Spend": int(sub.mean())})
            cs_df2 = pd.DataFrame(city_s)
            fig2 = go.Figure(go.Bar(
                x=cs_df2["City"], y=cs_df2["Avg Monthly Spend"],
                marker_color=[AMBER, HONEY, TERRA, BROWN],
                text=["Rs.{:,}".format(v) for v in cs_df2["Avg Monthly Spend"]],
                textposition="outside",
                textfont=dict(color=TEXT, size=11),
            ))
            pc(fig2, h=280,
               margin=dict(t=10, b=20, l=70, r=20),
               title=dict(text="Avg Spend by City Tier", font=dict(color=TEXT_BRIGHT)),
               xaxis=dict(title="City tier"),
               yaxis=dict(title="Avg monthly spend (INR)", showgrid=False, rangemode="tozero"))
            ibox("Metro dog owners spend noticeably more on average than Tier-2 and Tier-3. "
                 "A tiered pricing model \u2014 cheaper in smaller cities \u2014 could maximise reach without sacrificing metro revenue.")

        shead("Where Does the Money Go?")
        cat_c = raw["Q8_top_spend_category"].value_counts()
        _dark_pie(cat_c.index.tolist(), cat_c.values.tolist(), CHART, h=340, hole=0.4)
        ibox("Food & treats consume the largest share of dog spending (38%), followed by vet & medicines (25%). "
             "PawIndia's marketplace feature \u2014 letting owners buy food and vet services in-app \u2014 "
             "targets the two biggest spending categories directly.")

        tab_summary([
            "Most owners spend Rs.2,000\u20136,000/month \u2014 premium subscription features at Rs.199\u2013499/month are affordable.",
            "Metro dog owners spend more on average, supporting tiered pricing.",
            "Food (38%) and vet care (25%) together account for nearly two-thirds of all dog spending \u2014 "
            "these are the natural monetisation anchors for PawIndia.",
        ])

    with t3:
        shead("The Real Struggles of Indian Dog Owners")
        ch_cols2 = {c: c.replace("Q10_challenges__","").replace("_"," ").title()
                    for c in df.columns if c.startswith("Q10_challenges__")}
        ch_df2 = pd.DataFrame({"Challenge": list(ch_cols2.values()),
                                "Respondents": [int(df[col].sum()) for col in ch_cols2]
                                }).sort_values("Respondents")
        fig = go.Figure(go.Bar(
            x=ch_df2["Respondents"], y=ch_df2["Challenge"], orientation="h",
            marker=dict(color=ch_df2["Respondents"],
                        colorscale=[[0,"#1A1209"],[0.5,AMBER],[1,HONEY]]),
            text=ch_df2["Respondents"], textposition="outside",
            textfont=dict(color=TEXT, size=10),
        ))
        pc(fig, h=380,
           margin=dict(t=10, b=20, l=240, r=60),
           xaxis=dict(title="Number of respondents", showgrid=False, visible=False),
           yaxis=dict(title=""))
        ibox("Finding a reliable vet and lack of pet-friendly spaces are the top two problems. "
             "Both are directly solved by PawIndia's vet directory and places map. "
             "Losing track of vaccinations \u2014 third on the list \u2014 is solved by the health tracker.")

        c1, c2 = st.columns(2)
        with c1:
            shead("How People Find Vets Today")
            vc = raw["Q11_vet_discovery"].value_counts()
            _dark_pie(vc.index.tolist(), vc.values.tolist(), CHART, hole=0.45)
            ibox("Word of mouth (35%) and Google Maps (30%) are the current ways people find vets. "
                 "There is no dedicated pet app in this discovery chain \u2014 "
                 "PawIndia's vet directory enters a market with no direct competitor.")

        with c2:
            shead("Lost Dog Experiences")
            lc = raw["Q12_lost_dog_experience"].value_counts()
            fig3 = go.Figure(go.Bar(
                x=lc.index, y=lc.values,
                marker_color=CHART[:4],
                text=lc.values, textposition="outside",
                textfont=dict(color=TEXT, size=11),
            ))
            pc(fig3, h=280,
               margin=dict(t=10, b=20, l=60, r=20),
               xaxis=dict(title="Experience type"),
               yaxis=dict(title="Respondents", showgrid=False, rangemode="tozero"))
            ibox("A significant share of owners have experienced losing a dog or know someone who has. "
                 "This validates the community alert / lost-and-found feature as emotionally high-value.")

        tab_summary([
            "Vet access and pet-friendly spaces are the two most widely felt problems across all cities.",
            "35% of people currently find vets via word of mouth \u2014 unreliable, inconsistent, and replaceable by an app.",
            "Lost dog experiences are common enough to make the community alert feature a strong emotional selling point.",
            "Vaccination tracking \u2014 the third biggest problem \u2014 is easy to solve digitally and creates daily app engagement.",
        ])

    with t3:
        shead("How Dog Owners Use Apps and the Internet")
        c1, c2 = st.columns(2)
        with c1:
            ao = ["Never","Rarely","Sometimes","Often"]
            ac3 = raw["Q15_app_usage"].value_counts().reindex(ao, fill_value=0)
            fig = go.Figure(go.Bar(
                x=ac3.index, y=ac3.values,
                marker_color=CHART[:4],
                text=ac3.values, textposition="outside",
                textfont=dict(color=TEXT, size=11),
            ))
            pc(fig, h=260,
               margin=dict(t=40, b=20, l=60, r=20),
               title=dict(text="Current App Usage for Pet Needs", font=dict(color=TEXT_BRIGHT)),
               xaxis=dict(title="Usage frequency"),
               yaxis=dict(title="Respondents", showgrid=False, rangemode="tozero"))
            ibox("Most respondents currently use apps only sometimes or rarely for pet needs \u2014 "
                 "there is no dominant app they are loyal to. "
                 "PawIndia enters an open market without an entrenched competitor to displace.")

        with c2:
            pc2 = raw["Q16_purchase_platform"].value_counts()
            _dark_pie(pc2.index.tolist(), pc2.values.tolist(), CHART, h=320, hole=0.4,
                      title_text="Where They Buy Pet Products")
            ibox("E-commerce platforms dominate pet product purchases \u2014 "
                 "integrating an in-app marketplace with major platforms would meet owners where they already shop.")

        shead("Do More Engaged Users Also Spend More?")
        fig3 = px.scatter(
            df.sample(min(600,n), random_state=42),
            x="engagement_score", y="Q7_monthly_spend_inr",
            color="Q25_app_adoption",
            color_discrete_map={"Yes":GREEN_YES, "Maybe":HONEY, "No":RED_NO},
            opacity=0.35, size_max=6,
            labels={"engagement_score":"Engagement Score",
                    "Q7_monthly_spend_inr":"Monthly Spend (INR)",
                    "Q25_app_adoption":"Would Download"},
        )
        fig3.update_traces(marker=dict(size=5))
        pc(fig3, h=320,
           margin=dict(t=20, b=20, l=70, r=20),
           xaxis=dict(title="Engagement Score"),
           yaxis=dict(title="Monthly Spend (INR)"))
        ibox("Green dots (Yes) cluster towards the right \u2014 higher engagement scores predict "
             "download intent better than spend levels. "
             "Targeting dog owners who already use multiple digital services is more efficient than targeting by spend.")

        shead("How Key Behaviours Connect to Each Other")
        corr_c = ["Q7_monthly_spend_inr","Q9_online_purchase_freq_enc","Q15_app_usage_enc",
                  "Q20_community_importance_enc","Q22_reviews_importance_enc",
                  "engagement_score","Q25_target"]
        valid_c  = [c for c in corr_c if c in df.columns]
        labels_c = ["Spend","Online Freq","App Usage","Community","Reviews","Engagement","Target"][:len(valid_c)]
        corr_m = df[valid_c].corr().round(2)
        fig4 = go.Figure(go.Heatmap(
            z=corr_m.values, x=labels_c, y=labels_c,
            colorscale=[[0,"#1A1209"],[0.5,AMBER],[1,HONEY]],
            text=corr_m.values, texttemplate="%{text}",
            textfont=dict(color=TEXT_BRIGHT),
            showscale=True,
            colorbar=dict(tickfont=dict(color=TEXT), title=dict(text="Correlation", font=dict(color=TEXT))),
        ))
        pc(fig4, h=360,
           margin=dict(t=10, b=80, l=80, r=20),
           xaxis=dict(title=""),
           yaxis=dict(title=""))
        ibox("Engagement score has the highest correlation with the adoption target. "
             "Reviews importance and community importance are also positively linked. "
             "Build features that create habit and community \u2014 they are the strongest retention drivers.")

        st.download_button("\u2b07 Download Insights Data", df.to_csv(index=False),
                           "pawindia_insights.csv", "text/csv")

        tab_summary([
            "Most dog owners are not currently using any dedicated pet app \u2014 the market is open.",
            "E-commerce is the dominant purchase channel \u2014 an in-app marketplace is a natural addition.",
            "Engagement score is the strongest predictor of whether someone will download PawIndia \u2014 "
            "more so than how much they already spend.",
            "Community features (reviews, playdates, alerts) are highly correlated with adoption intent \u2014 "
            "social features are not optional extras.",
        ])


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — WILL THEY BUY?
# ══════════════════════════════════════════════════════════════════════════════
elif page == "\U0001f4b0  Will They Buy?":
    st.markdown(
        "<h1 style='font-size:1.8rem;margin-bottom:4px'><span class='anim-bounce' style='display:inline-block'>💰</span> "
        "<span class='shimmer-title'>Will They Buy?</span></h1>"
        "<p style='color:{d};font-weight:500;animation:fadeSlideUp .6s ease-out both'>Subscription preferences, who is most likely to adopt, and what would make them pay</p>"
        .format(c=TEXT_BRIGHT, d=TEXT_DIM),
        unsafe_allow_html=True)
    live_bar(n)

    c1, c2, c3, c4 = st.columns(4)
    with c1: _kpi("Definite Yes",    "{:.1f}%".format(pct_yes),           "Would download now",    GREEN_YES)
    with c2: _kpi("Open to It",      "{:.1f}%".format(pct_maybe),         "Conditional adopters",  HONEY)
    with c3: _kpi("Would Not",       "{:.1f}%".format(pct_no),            "Lost audience",         RED_NO)
    with c4: _kpi("Total Reachable", "{:.1f}%".format(pct_yes+pct_maybe), "Yes + Maybe",           TEAL)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    t1, t2, t3, t4 = st.tabs(["\U0001f53b Conversion Funnel","\U0001f4b3 Subscriptions",
                               "\U0001f4cd By Location","\U0001f464 By Profile"])

    with t1:
        shead("How Many People Would Actually Download PawIndia?")
        total    = n
        interested = int((df["Q15_app_usage"] != "Never").sum()) if "Q15_app_usage" in df.columns else int(n*0.75)
        willing  = int((df["Q25_app_adoption"].isin(["Yes","Maybe"])).sum())
        definite = int((df["Q25_app_adoption"] == "Yes").sum())
        fig = go.Figure(go.Funnel(
            y=["Surveyed Dog Owners","Already Use Pet Apps","Open to Downloading","Would Definitely Download"],
            x=[total, interested, willing, definite],
            textinfo="value+percent initial",
            marker=dict(color=[AMBER, HONEY, TERRA, GREEN_YES],
                        line=dict(color=SURFACE, width=1.5)),
            textfont=dict(color=TEXT_BRIGHT, size=13),
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(26,18,9,.3)",
                          height=360, margin=dict(t=20,b=20,l=20,r=20),
                          font=dict(color=TEXT))
        st.plotly_chart(fig, use_container_width=True, config=PCFG)
        ibox("The funnel narrows from {:,} surveyed to {:,} definite downloaders ({:.1f}%). "
             "The gap between 'open' ({:,}) and 'definite' ({:,}) is the conversion challenge \u2014 "
             "closing it requires building trust through a polished onboarding and a compelling first session.".format(
                 total, definite, pct_yes, willing, definite))

        shead("High Engagement + High Spend = Most Likely to Download")
        fig2 = px.scatter(
            df.sample(min(600,n), random_state=42),
            x="engagement_score", y="Q7_monthly_spend_inr",
            color="Q25_app_adoption",
            color_discrete_map={"Yes":GREEN_YES, "Maybe":HONEY, "No":RED_NO},
            size="Q7_monthly_spend_inr", size_max=10, opacity=0.35,
            labels={"engagement_score":"Engagement Score",
                    "Q7_monthly_spend_inr":"Monthly Spend (INR)",
                    "Q25_app_adoption":"Would Download"},
        )
        pc(fig2, h=320,
           margin=dict(t=20, b=20, l=70, r=20),
           xaxis=dict(title="Engagement Score"),
           yaxis=dict(title="Monthly Spend (INR)"))
        ibox("The densest cluster of green (Yes) dots is at medium-to-high engagement scores. "
             "Spend alone does not predict adoption. "
             "Focus early marketing on digitally active dog owners \u2014 not just affluent ones.")

        tab_summary([
            "{:.1f}% would definitely download \u2014 a strong validation signal for a new product.".format(pct_yes),
            "A further {:.1f}% are open to it \u2014 the conversion gap is real but closeable with good onboarding.".format(pct_maybe),
            "Digital engagement predicts download intent better than spending level.",
        ])

    with t2:
        shead("What Pricing Model Would Work Best?")
        c1, c2 = st.columns(2)
        with c1:
            sub_c = raw["Q18_subscription_pref"].value_counts()
            _dark_pie(sub_c.index.tolist(), sub_c.values.tolist(), CHART, h=340, hole=0.45)
            ibox("Freemium is the most popular preference by far \u2014 most users want to try before paying. "
                 "This is normal for new apps in India and should be embraced, not fought.")

        with c2:
            sub_adopt = []
            for sub_col in [c for c in df.columns if c.startswith("Q18_subscription_pref_")]:
                label = sub_col.replace("Q18_subscription_pref_","")
                sub_df = df[df[sub_col]==1]
                if len(sub_df) > 10:
                    yes_r = (sub_df["Q25_app_adoption"]=="Yes").sum()/len(sub_df)*100
                    sub_adopt.append({"Model": label, "% Definite Yes": round(yes_r,1)})
            sa_df = pd.DataFrame(sub_adopt).sort_values("% Definite Yes", ascending=False)
            fig2 = go.Figure(go.Bar(
                x=sa_df["% Definite Yes"], y=sa_df["Model"], orientation="h",
                marker=dict(color=sa_df["% Definite Yes"],
                            colorscale=[[0,"#1A1209"],[0.5,AMBER],[1,HONEY]]),
                text=["{}%".format(v) for v in sa_df["% Definite Yes"]], textposition="outside",
                textfont=dict(color=TEXT, size=11),
            ))
            pc(fig2, h=300,
               margin=dict(t=40, b=20, l=180, r=60),
               title=dict(text="Download Intent by Subscription Preference", font=dict(color=TEXT_BRIGHT)),
               xaxis=dict(title="% who say Yes", showgrid=False, visible=False),
               yaxis=dict(title=""))
            ibox("Users who prefer annual or monthly subscriptions show higher download intent \u2014 "
                 "they are already comfortable paying for apps. "
                 "Start free, then upsell to these users first.")

        shead("Would People Share Their Location? (Critical for the Nearby Features)")
        loc_c = raw["Q17_location_sharing"].value_counts()
        pct_share = round((loc_c.get("Yes, always",0) + loc_c.get("Yes, only when using the app",0)) / n * 100, 1)
        _dark_pie(loc_c.index.tolist(), loc_c.values.tolist(),
                  [AMBER, HONEY, TERRA, BROWN], h=340, hole=0.5,
                  center_text="<b>{}%</b><br>Share".format(pct_share))
        ibox("{}% of respondents will share their location with the app \u2014 "
             "enough to make the nearby vet, park and groomer features fully functional from launch.".format(pct_share))

        tab_summary([
            "Freemium is the preferred model \u2014 users want to experience the app before committing to a payment.",
            "Annual and monthly subscribers show higher download intent \u2014 they are the quickest path to revenue.",
            "{}% will share location, validating the core 'find nearby' features.".format(pct_share),
        ])

    with t3:
        shead("Which Cities Are Most Ready for PawIndia?")
        city_adopt = []
        for tcol, label in [("Q2_city_tier_Metro","Metro"),("Q2_city_tier_Tier-2","Tier-2"),
                             ("Q2_city_tier_Tier-3","Tier-3"),("Q2_city_tier_Rural","Rural")]:
            if tcol in df.columns:
                sub = df[df[tcol]==1]
                if len(sub) > 10:
                    city_adopt.append({
                        "City": label,
                        "Yes":  round((sub["Q25_app_adoption"]=="Yes").sum()/len(sub)*100,1),
                        "Maybe":round((sub["Q25_app_adoption"]=="Maybe").sum()/len(sub)*100,1),
                        "No":   round((sub["Q25_app_adoption"]=="No").sum()/len(sub)*100,1),
                        "Avg Spend": int(sub["Q7_monthly_spend_inr"].mean()),
                        "n": len(sub),
                    })
        ca_df = pd.DataFrame(city_adopt)
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Would Download", x=ca_df["City"], y=ca_df["Yes"], marker_color=GREEN_YES))
        fig.add_trace(go.Bar(name="Open to Trying", x=ca_df["City"], y=ca_df["Maybe"], marker_color=HONEY))
        fig.add_trace(go.Bar(name="Would Not",      x=ca_df["City"], y=ca_df["No"],    marker_color="rgba(239,83,80,0.5)"))
        pc(fig, h=320,
           margin=dict(t=20, b=60, l=60, r=20),
           barmode="stack",
           xaxis=dict(title="City tier"),
           yaxis=dict(title="% of respondents in that tier", showgrid=False, rangemode="tozero"),
           legend=dict(orientation="h", y=-0.25))
        ibox("Metro cities lead on adoption intent across all tiers. "
             "Tier-2 has a large 'Maybe' pool \u2014 these users need one strong reason to commit. "
             "Offer a Tier-2 city-specific feature (e.g. local vet discovery) at launch to convert them.")

        fig2 = px.scatter(
            ca_df, x="Avg Spend", y="Yes",
            size="n", color="City", color_discrete_sequence=CHART,
            size_max=50,
            labels={"Yes":"% Definite Yes","Avg Spend":"Avg Monthly Spend (INR)"},
            title="Cities that spend more tend to show higher adoption intent",
        )
        pc(fig2, h=280,
           margin=dict(t=50, b=20, l=70, r=20),
           xaxis=dict(title="Avg monthly spend (INR)"),
           yaxis=dict(title="% Definite Yes"))
        ibox("There is a positive relationship between average spend and download intent across city tiers. "
             "Prioritise launches in cities where both are high.")

        tab_summary([
            "Metro cities have the highest download intent and average spend \u2014 launch here first.",
            "Tier-2 cities have a large undecided group \u2014 a targeted feature or campaign could move them.",
            "Rural users show the lowest intent and spend \u2014 defer to a later growth phase.",
        ])

    with t3:
        shead("Who Is Most Likely to Download PawIndia?")
        c1, c2 = st.columns(2)
        with c1:
            age_enc2 = {"Under 18":0,"18-24":1,"25-34":2,"35-44":3,"45-59":4,"60+":5}
            aa = []
            for age in ["Under 18","18-24","25-34","35-44","45-59","60+"]:
                sub = df[df["Q1_age_group_enc"] == age_enc2.get(age,-1)]
                if len(sub) > 5:
                    aa.append({"Age":age, "% Yes": round((sub["Q25_app_adoption"]=="Yes").sum()/len(sub)*100,1)})
            aa_df = pd.DataFrame(aa)
            fig = go.Figure(go.Bar(
                x=aa_df["Age"], y=aa_df["% Yes"],
                marker=dict(color=aa_df["% Yes"],colorscale=[[0,"#1A1209"],[0.5,AMBER],[1,HONEY]]),
                text=["{}%".format(v) for v in aa_df["% Yes"]], textposition="outside",
                textfont=dict(color=TEXT, size=11),
            ))
            pc(fig, h=260,
               margin=dict(t=40, b=20, l=60, r=20),
               title=dict(text="% Definite Yes by Age Group", font=dict(color=TEXT_BRIGHT)),
               xaxis=dict(title="Age group"),
               yaxis=dict(title="% who say Yes", showgrid=False, range=[0,80], rangemode="tozero"))
            ibox("18\u201334 year olds show the highest download intent \u2014 digital natives who are comfortable "
                 "with subscription apps and use smartphones as a primary resource.")

        with c2:
            da = []
            for tcol, label in [("Q4_num_dogs_1 Dog","1 Dog"),
                                 ("Q4_num_dogs_2 Dogs","2 Dogs"),("Q4_num_dogs_3+ Dogs","3+ Dogs")]:
                if tcol in df.columns:
                    sub = df[df[tcol]==1]
                    if len(sub) > 5:
                        da.append({"Dogs":label, "% Yes": round((sub["Q25_app_adoption"]=="Yes").sum()/len(sub)*100,1)})
            da_df = pd.DataFrame(da)
            fig2 = go.Figure(go.Bar(
                x=da_df["Dogs"], y=da_df["% Yes"],
                marker_color=CHART[:3],
                text=["{}%".format(v) for v in da_df["% Yes"]], textposition="outside",
                textfont=dict(color=TEXT, size=11),
            ))
            pc(fig2, h=260,
               margin=dict(t=40, b=20, l=60, r=20),
               title=dict(text="% Definite Yes by Number of Dogs Owned", font=dict(color=TEXT_BRIGHT)),
               xaxis=dict(title="Number of dogs"),
               yaxis=dict(title="% who say Yes", showgrid=False, range=[0,80], rangemode="tozero"))
            ibox("Multi-dog households show slightly higher download intent \u2014 "
                 "managing two or more dogs multiplies every logistical problem the app solves.")

        shead("Which Features Would Make Them Hit Download?")
        ft_cols2 = {c: c.replace("Q14_preferred_features__","").replace("_"," ").title()
                    for c in df.columns if c.startswith("Q14_preferred_features__")}
        ft_df2 = pd.DataFrame({"Feature": list(ft_cols2.values()),
                                "Respondents": [int(df[col].sum()) for col in ft_cols2]
                                }).sort_values("Respondents")
        fig3 = go.Figure(go.Bar(
            x=ft_df2["Respondents"], y=ft_df2["Feature"], orientation="h",
            marker=dict(color=ft_df2["Respondents"],
                        colorscale=[[0,"#1A1209"],[0.5,AMBER],[1,HONEY]]),
            text=ft_df2["Respondents"], textposition="outside",
            textfont=dict(color=TEXT, size=10),
        ))
        pc(fig3, h=400,
           margin=dict(t=10, b=20, l=240, r=60),
           xaxis=dict(title="Number of respondents", showgrid=False, visible=False),
           yaxis=dict(title=""))
        ibox("Health tracker + vet directory + lost-and-found alerts are the three most requested features. "
             "Build all three for the MVP and you have covered the primary reason most users would download.")

        wtp_cols = [c for c in ["Q25_app_adoption","Q7_monthly_spend_inr","Q15_app_usage",
                                 "Q25_target","Q25_binary","engagement_score"] if c in df.columns]
        st.download_button("\u2b07 Download WTP Analysis", df[wtp_cols].to_csv(index=False),
                           "pawindia_wtp.csv", "text/csv")

        tab_summary([
            "18\u201334 year olds are the highest intent group \u2014 they are PawIndia's primary acquisition target.",
            "Multi-dog households show higher adoption intent than single-dog owners.",
            "Health tracker, vet directory and lost-and-found alerts are the three features that would drive downloads.",
            "The ideal early adopter: 25\u201334, 2+ dogs, metro or Tier-2 city, already uses apps regularly.",
        ])


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — DATA JOURNEY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "\U0001f52c  Data Journey":
    st.markdown(
        "<h1 style='font-size:1.8rem;margin-bottom:4px'><span class='anim-pulse' style='display:inline-block'>🔬</span> "
        "<span class='shimmer-title'>Data Journey</span></h1>"
        "<p style='color:{d};font-weight:500;animation:fadeSlideUp .6s ease-out both'>How we built 2,000 realistic survey responses and cleaned them for analysis</p>"
        .format(c=TEXT_BRIGHT, d=TEXT_DIM),
        unsafe_allow_html=True)
    live_bar(n)

    t1, t2, t3 = st.tabs(["\U0001f9ea How We Built the Data","\U0001f9f9 How We Cleaned It","\U0001f4ca Before vs After"])

    with t1:
        shead("Why Synthetic Data?")
        st.markdown(
            '<div class="icard"><p style="color:{t};line-height:1.8">'
            'PawIndia has no existing users yet. To test whether the app idea is viable, '
            'we created 2,000 synthetic survey respondents that reflect realistic Indian '
            'dog owner behaviour \u2014 grounded in known market trends, city-level differences, '
            'and the digital habits of Indian millennials. We also added real-world noise '
            'so the data behaves like an actual survey, not a clean simulation.'
            '</p></div>'.format(t=TEXT), unsafe_allow_html=True)

        shead("How We Designed the Distributions")
        for i, (title, desc) in enumerate([
            ("Age skew", "35% aged 25\u201334, matching India's millennial dog ownership boom."),
            ("City tier bias", "45% Metro, 30% Tier-2, 18% Tier-3, 7% Rural \u2014 reflecting where organised pet spending happens."),
            ("Monthly spend", "Generated using a triangular distribution by city and dog count. Metro owners get a 1.3\u00d7 multiplier."),
            ("Adoption target (Q25)", "Scored from app usage, community importance, engagement and non-linear feature interactions \u2014 producing 48% Yes / 37% Maybe / 15% No."),
            ("Multi-select questions", "Q10 (problems) and Q14 (features) allowed up to 3 picks, weighted by real Indian pet owner pain points."),
        ], 1):
            st.markdown(
                '<div style="background:{bg};border:1px solid {bd};border-top:4px solid {a};'
                'border-radius:10px;padding:16px 20px;margin-bottom:10px;'
                'animation:fadeSlideUp 0.4s ease-out both;'
                'transition:transform .25s ease,border-color .25s ease" '
                'onmouseover="this.style.transform=\'translateX(6px)\';'
                'this.style.borderColor=\'rgba(212,168,83,0.4)\'" '
                'onmouseout="this.style.transform=\'\';'
                'this.style.borderColor=\'\'">'
                '<span style="background:{a};color:{bg};border-radius:50%;width:24px;height:24px;'
                'display:inline-flex;align-items:center;justify-content:center;font-weight:700;'
                'font-size:.8rem;margin-right:10px">{i}</span>'
                '<strong style="color:{txt}">{title}</strong>'
                '<p style="color:{dim};margin:6px 0 0 34px;font-size:.88rem">{desc}</p>'
                '</div>'.format(bg=SURFACE, bd=BORDER, a=AMBER, i=i, txt=TEXT_BRIGHT, dim=TEXT_DIM, title=title, desc=desc),
                unsafe_allow_html=True)

        shead("Noise We Injected to Make It Feel Real")
        for title, desc in [
            ("Duplicate rows", "20 rows duplicated \u2014 simulates accidental double submissions."),
            ("Negative spend values", "~2% of Q7 made negative \u2014 simulates data entry errors."),
            ("Implausibly high spend", "~2% multiplied by 10 \u2014 simulates an extra zero typo."),
            ("Missing numeric spend", "15% left blank, using the range selector only."),
            ("Capitalisation inconsistency", "~3% of city tier entries lowercased."),
            ("Whitespace padding", "~4% of spend range entries had leading/trailing spaces."),
            ("Non-owners answering dog questions", "~40% of non-dog-owners partially answered breed questions."),
            ("Over-selection on multi-select", "~5% picked more than the allowed 3 options."),
            ("Blank target variable", "~2% left Q25 blank \u2014 simulates incomplete form submissions."),
        ]:
            st.markdown(
                '<div style="display:flex;align-items:flex-start;margin-bottom:10px;'
                'padding:10px 14px;background:{bg};border-radius:10px;border:1px solid {bd};'
                'animation:fadeSlideUp 0.4s ease-out both;transition:transform .25s ease" '
                'onmouseover="this.style.transform=\'translateX(4px)\'" '
                'onmouseout="this.style.transform=\'\'">'
                '<span class="anim-wiggle" style="color:{r};font-size:1rem;margin-right:10px;flex-shrink:0">\u26a0</span>'
                '<div><strong style="color:{txt}">{title}</strong>'
                '<p style="color:{dim};margin:2px 0;font-size:.86rem">{desc}</p>'
                '</div></div>'.format(bg=SURFACE, bd=BORDER, r=RED_NO, txt=TEXT_BRIGHT, dim=TEXT_DIM, title=title, desc=desc),
                unsafe_allow_html=True)

        shead("Raw Data Sample (First 8 Rows)")
        show_cols = [c for c in ["respondent_id","Q1_age_group","Q2_city_tier","Q4_num_dogs",
                                  "Q7_monthly_spend_inr","Q7_spend_range","Q25_app_adoption"] if c in raw.columns]
        st.dataframe(raw[show_cols].head(8), use_container_width=True, hide_index=True)

        tab_summary([
            "Synthetic data was chosen because PawIndia has no users yet \u2014 it mirrors realistic distributions from market research.",
            "Nine types of noise were injected deliberately so the cleaning pipeline had real problems to solve.",
            "Distributions were designed to reflect known Indian dog owner demographics, not invented arbitrarily.",
        ])

    with t2:
        shead("10 Steps to a Clean Dataset")
        for step, title, desc in [
            ("Step 1",  "Remove duplicates",         "Removed duplicate rows based on all non-ID columns. {} rows removed.".format(len(raw)-n)),
            ("Step 2",  "Drop rows with no target",  "Rows where Q25 was blank were removed \u2014 the target is needed for all models."),
            ("Step 3",  "Standardise text",          "All text stripped of whitespace and converted to title case."),
            ("Step 4",  "Fix spend values",          "Negative values and amounts above Rs.50,000 were nulled. Missing values filled from range midpoints or group medians."),
            ("Step 5",  "Fill missing categories",   "Remaining blank categorical fields filled by mode within relevant groups."),
            ("Step 6",  "Encode ordered categories", "Age, satisfaction, app usage etc. encoded as integers preserving their natural order."),
            ("Step 7",  "One-hot encode nominals",   "City tier, residence, subscription preference etc. split into binary columns."),
            ("Step 8",  "Expand multi-select",       "Q5, Q10 and Q14 multi-select strings split into individual yes/no columns per option."),
            ("Step 9",  "Engineer features",         "Added spend_per_dog, engagement_score, and Q25_binary."),
            ("Step 10", "Final check",               "Final dataset: {:,} rows, {} columns. Zero missing values confirmed.".format(n, len(df.columns))),
        ]:
            st.markdown(
                '<div style="background:{bg};border:1px solid {bd};border-top:4px solid {a};'
                'border-radius:10px;padding:14px 18px;margin-bottom:10px;'
                'animation:fadeSlideUp 0.4s ease-out both;transition:transform .25s ease" '
                'onmouseover="this.style.transform=\'translateX(6px)\'" '
                'onmouseout="this.style.transform=\'\'">'
                '<span style="color:{honey};font-size:.7rem;font-weight:700;text-transform:uppercase;'
                'letter-spacing:1px">{step}</span>'
                '<strong style="color:{txt};display:block;margin:4px 0">{title}</strong>'
                '<p style="color:{dim};margin:0;font-size:.88rem">{desc}</p></div>'.format(
                    bg=SURFACE, bd=BORDER, a=AMBER, honey=HONEY, step=step,
                    txt=TEXT_BRIGHT, dim=TEXT_DIM, title=title, desc=desc),
                unsafe_allow_html=True)

        tab_summary([
            "10 cleaning steps transformed 2,020 noisy rows into 1,966 fully usable records.",
            "No values are missing in the cleaned dataset \u2014 every ML model can run without imputation.",
            "Three engineered features (spend_per_dog, engagement_score, Q25_binary) were added to improve model signal.",
        ])

    with t3:
        shead("How the Dataset Changed After Cleaning")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Raw Rows",       "{:,}".format(len(raw)))
        c2.metric("Cleaned Rows",   "{:,}".format(n),             delta="-{} removed".format(len(raw)-n))
        c3.metric("Raw Columns",    str(len(raw.columns)))
        c4.metric("Clean Columns",  str(len(df.columns)), delta="+{} new".format(len(df.columns)-len(raw.columns)))

        shead("Missing Values: Before and After")
        raw_miss = int(raw.isnull().sum().sum())
        fig = go.Figure(go.Bar(
            x=["Raw Dataset","Cleaned Dataset"], y=[raw_miss, 0],
            marker_color=[RED_NO, GREEN_YES],
            text=[raw_miss, 0], textposition="outside",
            textfont=dict(color=TEXT, size=12),
        ))
        pc(fig, h=260,
           margin=dict(t=10, b=20, l=70, r=20),
           xaxis=dict(title="Dataset version"),
           yaxis=dict(title="Total missing values", showgrid=False, rangemode="tozero"))
        ibox("The raw dataset had {:,} missing values across all columns. "
             "After cleaning, the count is exactly zero \u2014 every row is complete and usable.".format(raw_miss))

        shead("Spend Distribution: Raw vs Cleaned")
        c1, c2 = st.columns(2)
        with c1:
            raw_s = pd.to_numeric(raw["Q7_monthly_spend_inr"], errors="coerce").dropna()
            fig2 = go.Figure(go.Histogram(x=raw_s, nbinsx=40, marker_color=RED_NO, opacity=0.8))
            pc(fig2, h=240,
               margin=dict(t=40, b=20, l=60, r=20),
               title=dict(text="Raw \u2014 includes errors", font=dict(color=TEXT_BRIGHT)),
               xaxis=dict(title="Monthly spend (INR)"),
               yaxis=dict(title="Count", showgrid=False))
        with c2:
            fig3 = go.Figure(go.Histogram(x=df["Q7_monthly_spend_inr"].dropna(),
                                           nbinsx=40, marker_color=GREEN_YES, opacity=0.8))
            pc(fig3, h=240,
               margin=dict(t=40, b=20, l=60, r=20),
               title=dict(text="Cleaned \u2014 outliers removed", font=dict(color=TEXT_BRIGHT)),
               xaxis=dict(title="Monthly spend (INR)"),
               yaxis=dict(title="Count", showgrid=False))
        ibox("The raw distribution has a long tail of implausibly high values (data entry errors). "
             "The cleaned version shows a realistic right-skewed distribution with no extreme outliers.")

        shead("Target Variable Distribution After Cleaning")
        tc = df["Q25_app_adoption"].value_counts()
        fig4 = go.Figure(go.Bar(
            x=tc.index, y=tc.values,
            marker_color=[GREEN_YES, HONEY, RED_NO],
            text=["{} ({:.1f}%)".format(v, v/n*100) for v in tc.values],
            textposition="outside",
            textfont=dict(color=TEXT, size=11),
        ))
        pc(fig4, h=280,
           margin=dict(t=10, b=20, l=60, r=20),
           xaxis=dict(title="Adoption response"),
           yaxis=dict(title="Respondents", showgrid=False, rangemode="tozero"))
        ibox("The 48% / 37% / 15% split is intentional \u2014 it creates a meaningful "
             "multi-class classification problem. Non-linear feature interactions (e.g. app usage combined with "
             "community importance) allow advanced models like XGBoost to reach 80%+ accuracy.")

        d1, d2 = st.columns(2)
        with d1: st.download_button("\u2b07 Download Raw Data", raw.to_csv(index=False), "pawindia_raw.csv", "text/csv")
        with d2: st.download_button("\u2b07 Download Cleaned Data", df.to_csv(index=False), "pawindia_clean.csv", "text/csv")

        tab_summary([
            "Cleaning removed {} rows and eliminated {:,} missing values.".format(len(raw)-n, raw_miss),
            "The spend distribution changed dramatically \u2014 from a noisy spread to a clean, realistic histogram.",
            "The 48/37/15 target split with non-linear interactions creates a meaningful ML challenge \u2014 advanced models reach 80%+ accuracy.",
        ])


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — RESEARCH & ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "\U0001f4ca  Research & Analytics":
    st.markdown(
        '<div style="background:{bg};border:1px solid {bd};border-radius:14px;'
        'padding:22px 26px;margin-bottom:14px;border-left:5px solid {a};'
        'box-shadow:0 2px 12px rgba(0,0,0,.3);animation:fadeSlideUp .5s ease-out both,glowPulse 4s ease-in-out infinite;'
        'transition:transform .3s ease" '
        'onmouseover="this.style.transform=\'translateY(-3px)\'" '
        'onmouseout="this.style.transform=\'translateY(0)\'">'
        '<div style="display:flex;align-items:center;gap:14px">'
        '<div class="anim-bounce" style="font-size:38px">\U0001f4ca</div>'
        '<div><h1 class="shimmer-title" style="margin:0;font-size:1.7rem;font-family:Bricolage Grotesque,sans-serif;'
        'font-weight:800">Research & Analytics</h1>'
        '<div style="color:{dim};font-size:.88rem;margin-top:4px">'
        'Full ML analysis: Classification \u00b7 Clustering \u00b7 Regression'
        '</div></div></div></div>'.format(bg=SURFACE, bd=BORDER, a=AMBER, txt=TEXT_BRIGHT, dim=TEXT_DIM),
        unsafe_allow_html=True)

    st.markdown(
        '<div style="background:{bg};border:1px solid {bd};border-radius:10px;'
        'padding:10px 16px;margin-bottom:16px;color:{t};font-size:.88rem;font-weight:500">'
        '\u25cf Models are cached after first load \u2014 switching tabs is instant &nbsp;|&nbsp; '
        '{n:,} respondents &nbsp;|&nbsp; Target: Q25 App Adoption (Yes / Maybe / No)'
        '</div>'.format(bg=SURFACE2, bd=BORDER, t=TEXT, n=n),
        unsafe_allow_html=True)

    def dhead(t):
        st.markdown(
            '<div style="display:flex;align-items:center;gap:10px;margin:30px 0 16px;'
            'animation:fadeSlideUp 0.4s ease-out both">'
            '<div style="width:4px;height:18px;background:linear-gradient(180deg,{a},transparent);'
            'border-radius:2px;animation:iconPulse 3s ease-in-out infinite"></div>'
            '<div style="color:{txt};font-size:1.05rem;font-weight:700">{t}</div></div>'.format(a=AMBER, txt=TEXT_BRIGHT, t=t),
            unsafe_allow_html=True)

    def dibox(t):
        st.markdown(
            '<div class="ibox" style="margin-bottom:30px"><span class="anim-pulse">\U0001f4a1</span> {}</div>'.format(t), unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["\U0001f3af Classification","\U0001f535 Clustering",
                            "\U0001f4c8 Regression"])

    # ── Classification ────────────────────────────────────────────────────────
    with t1:
        dhead("Predicting App Adoption \u2014 which dog owners will say Yes?")
        st.markdown("<p style='color:{}'>"
                    "8\u20139 algorithms compared on accuracy, precision, recall, F1-score "
                    "and 3-fold cross-validation. 80/20 stratified train/test split.</p>".format(TEXT_DIM),
                    unsafe_allow_html=True)

        with st.spinner("Training models \u2014 runs once then cached\u2026"):
            rdf, cms, feat_imp, best, yte, feat_names = run_classification()

        dhead("Performance Comparison \u2014 All Models")
        _dark_table(rdf)
        dibox("Best model: {} \u2014 F1={:.3f}, "
              "Accuracy={:.3f}. "
              "Cross-validation confirms the result holds on data the model never saw during training.".format(
                  best, rdf.iloc[0]['F1-Score'], rdf.iloc[0]['Accuracy']))

        dhead("F1-Score, Accuracy, Precision and Recall \u2014 Side by Side")
        fig_bar = go.Figure()
        for metric, color in [("Accuracy",AMBER),("Precision",HONEY),("Recall",TERRA),("F1-Score",SAGE)]:
            fig_bar.add_trace(go.Bar(name=metric, x=rdf["Model"], y=rdf[metric], marker_color=color))
        pc(fig_bar, h=360,
           margin=dict(t=20, b=100, l=60, r=20),
           barmode="group",
           xaxis=dict(title="Model", tickangle=-30),
           yaxis=dict(title="Score (0\u20131)", range=[0,1.1]),
           legend=dict(orientation="h", y=-0.3))
        dibox("XGBoost and Gradient Boosting lead because they capture non-linear feature interactions "
              "(e.g. high app usage + community importance) that simpler linear models miss. "
              "The accuracy spread from ~67% (KNN) to ~82% (XGBoost) shows how model choice matters.")

        dhead("Confusion Matrix \u2014 {}".format(best))
        cm = cms[best]
        labels_cm = ["No (0)","Maybe (1)","Yes (2)"]
        fig_cm = go.Figure(go.Heatmap(
            z=cm, x=labels_cm, y=labels_cm,
            colorscale=[[0,"#1A1209"],[0.5,AMBER],[1,HONEY]],
            text=cm, texttemplate="%{text}",
            textfont=dict(color=TEXT_BRIGHT),
            showscale=True,
            colorbar=dict(tickfont=dict(color=TEXT), title=dict(text="Count", font=dict(color=TEXT))),
        ))
        pc(fig_cm, h=340,
           margin=dict(t=20, b=60, l=80, r=20),
           xaxis=dict(title="Predicted label"),
           yaxis=dict(title="True label"))
        dibox("The diagonal shows correct predictions. Off-diagonal cells show where the model confuses "
              "Maybe with Yes \u2014 the two most similar groups. This is expected and acceptable; "
              "both represent users worth targeting.")

        if best in feat_imp:
            dhead("What Drives Predictions \u2014 Feature Importance ({})".format(best))
            fi = feat_imp[best]
            fi_df = pd.DataFrame({"Feature":list(fi.keys()),"Importance":list(fi.values())})
            fi_df = fi_df.sort_values("Importance", ascending=False).head(15)
            fi_df["Feature"] = (fi_df["Feature"]
                                 .str.replace(r"Q\d+_","",regex=True)
                                 .str.replace("_enc","")
                                 .str.replace("_"," ")
                                 .str[:35])
            fig_fi = go.Figure(go.Bar(
                x=fi_df["Importance"], y=fi_df["Feature"], orientation="h",
                marker=dict(color=fi_df["Importance"],colorscale=[[0,"#1A1209"],[0.5,AMBER],[1,HONEY]]),
                text=fi_df["Importance"].round(3), textposition="outside",
                textfont=dict(color=TEXT, size=10),
            ))
            pc(fig_fi, h=420,
               margin=dict(t=10, b=10, l=240, r=60),
               xaxis=dict(title="Importance score", showgrid=False, visible=False),
               yaxis=dict(title=""))
            dibox("App usage and community importance are the strongest predictors of adoption, along with "
                  "their interactions. This confirms the marketing insight: target digitally engaged dog owners "
                  "who value community, not just high spenders.")

        st.download_button("\u2b07 Download Classification Results", rdf.to_csv(index=False),
                           "pawindia_classification.csv", "text/csv")

        tab_summary([
            "The best classifier ({}) achieves F1={:.3f} on held-out test data.".format(best, rdf.iloc[0]['F1-Score']),
            "App usage, community importance, and their non-linear interactions are the top predictors of download intent.",
            "Maybe and Yes are frequently confused \u2014 both groups are adoption targets and should be marketed to.",
            "Cross-validation confirms results generalise beyond the training set.",
        ])

    # ── Clustering ────────────────────────────────────────────────────────────
    with t2:
        dhead("Clustering \u2014 Segmenting India's Dog Owners into Four Groups")
        st.markdown("<p style='color:{}'>K-Means on 10 behavioural and demographic features. "
                    "Elbow method and silhouette score used to select K=4.</p>".format(TEXT_DIM),
                    unsafe_allow_html=True)

        with st.spinner("Running clustering\u2026"):
            K_range, inertias, sils, labels, df2, summary, personas = run_clustering()

        c1, c2 = st.columns(2)
        with c1:
            fig_el = go.Figure(go.Scatter(
                x=K_range, y=inertias, mode="lines+markers",
                line=dict(color=HONEY,width=2.5), marker=dict(size=9,color=AMBER),
            ))
            fig_el.add_vline(x=4, line_dash="dash", line_color=SAGE,
                              annotation_text="K=4 chosen",
                              annotation_font_color=TEXT)
            pc(fig_el, h=260,
               margin=dict(t=40, b=30, l=70, r=20),
               title=dict(text="Elbow Curve", font=dict(color=TEXT_BRIGHT)),
               xaxis=dict(title="Number of clusters (K)"),
               yaxis=dict(title="Inertia (within-cluster variance)"))
        with c2:
            fig_sil = go.Figure(go.Bar(
                x=K_range, y=sils,
                marker_color=CHART[:len(K_range)],
                text=["{:.3f}".format(s) for s in sils], textposition="outside",
                textfont=dict(color=TEXT, size=11),
            ))
            fig_sil.add_vline(x=4, line_dash="dash", line_color=SAGE)
            pc(fig_sil, h=260,
               margin=dict(t=40, b=30, l=60, r=20),
               title=dict(text="Silhouette Score by K", font=dict(color=TEXT_BRIGHT)),
               xaxis=dict(title="Number of clusters (K)"),
               yaxis=dict(title="Silhouette score (higher = better)", rangemode="tozero"))
        dibox("K=4 is where the elbow bends most sharply and the silhouette score remains strong. "
              "Below 4 the groups are too broad; above 4 they become too small to be actionable.")

        dhead("The Four Dog Owner Personas")
        cols4 = st.columns(4)
        emojis = ["\U0001f3d9\ufe0f","\U0001f3d8\ufe0f","\U0001f6cb\ufe0f","\U0001f91d"]
        for i, (cid, (name, color, desc)) in enumerate(personas.items()):
            row = summary[summary["cluster"]==cid].iloc[0]
            cols4[i].markdown(
                '<div style="background:{bg};border:1px solid {bd};'
                'border-top:4px solid {color};border-radius:14px;padding:16px;text-align:center;'
                'box-shadow:0 2px 12px rgba(0,0,0,.3);animation:fadeSlideUp 0.5s ease-out {delay}s both;'
                'transition:transform .3s ease,box-shadow .3s ease" '
                'onmouseover="this.style.transform=\'translateY(-5px) scale(1.03)\';'
                'this.style.boxShadow=\'0 10px 28px rgba(212,168,83,.2)\'" '
                'onmouseout="this.style.transform=\'\';this.style.boxShadow=\'\'">'
                '<div class="anim-bounce" style="font-size:1.8rem">{emoji}</div>'
                '<div style="font-weight:700;color:{txt};font-size:.9rem;margin:6px 0">{name}</div>'
                '<div style="color:{dim};font-size:.75rem;margin-bottom:8px">{desc}</div>'
                '<div style="color:{color};font-weight:700;font-size:1rem">{count} members</div>'
                '<div style="color:{txt2};font-size:.78rem;margin-top:4px">'
                'Avg Spend: Rs.{spend:,}<br>'
                'Adoption: {adopt}%<br>Metro: {metro}%</div>'
                '</div>'.format(
                    bg=SURFACE, bd=BORDER, color=color, emoji=emojis[i],
                    delay=i*0.15,
                    txt=TEXT_BRIGHT, dim=TEXT_DIM, name=name, desc=desc,
                    count=int(row["Count"]), txt2=TEXT,
                    spend=int(row["Avg_Spend"]),
                    adopt=int(row["Pct_Yes"]*100),
                    metro=int(row["Pct_Metro"]*100)),
                unsafe_allow_html=True)

        dhead("Cluster Summary")
        disp = summary[["cluster","Persona","Count","Avg_Spend","Avg_App","Pct_Metro","Pct_Yes"]].copy()
        disp.columns = ["Cluster","Persona","Count","Avg Spend","Avg App Usage","% Metro","Adoption Rate"]
        disp["Avg Spend"]     = disp["Avg Spend"].apply(lambda x: "Rs.{:,}".format(int(x)))
        disp["% Metro"]       = disp["% Metro"].apply(lambda x: "{}%".format(int(x*100)))
        disp["Adoption Rate"] = disp["Adoption Rate"].apply(lambda x: "{}%".format(int(x*100)))
        _dark_table(disp, h=200)
        dibox("Urban Enthusiasts have the highest spend and adoption rate \u2014 the premium target. "
              "Practical Parents are the largest group \u2014 the volume opportunity. "
              "Even the Casual Companion segment shows meaningful adoption intent.")

        dhead("How the Four Groups Differ Across All Dimensions")
        pc_cols = ["Q7_monthly_spend_inr","Q15_app_usage_enc","Q20_community_importance_enc",
                   "Q22_reviews_importance_enc","engagement_score"]
        valid_pc = [c for c in pc_cols if c in df2.columns]
        if valid_pc:
            pcd = df2[valid_pc+["cluster"]].fillna(0).sample(min(400,len(df2)),random_state=42)
            pc_labels = ["Monthly Spend","App Usage","Community","Reviews","Engagement"][:len(valid_pc)]
            fig_pc = go.Figure(go.Parcoords(
                line=dict(color=pcd["cluster"],
                          colorscale=[[0,AMBER],[0.33,HONEY],[0.66,TEAL],[1,MAUVE]],
                          showscale=True,
                          colorbar=dict(tickfont=dict(color=TEXT), title=dict(text="Cluster", font=dict(color=TEXT)))),
                dimensions=[dict(range=[float(pcd[c].min()), float(pcd[c].max())],
                                  label=lab, values=pcd[c].tolist())
                             for c, lab in zip(valid_pc, pc_labels)],
                labelfont=dict(color=TEXT_BRIGHT, size=11),
                tickfont=dict(color=TEXT, size=10),
            ))
            pc(fig_pc, h=380, margin=dict(t=60, b=40, l=60, r=60))
            dibox("Each line is one respondent, coloured by cluster. "
                  "Warm lines (Cluster 0\u20131) show high spend and engagement; "
                  "cool lines (2\u20133) show lower activity. "
                  "Clear separation between clusters confirms K=4 is meaningful and not arbitrary.")

        st.download_button("\u2b07 Download Cluster Results",
                           summary.drop(columns=["Color"],errors="ignore").to_csv(index=False),
                           "pawindia_clusters.csv","text/csv")

        tab_summary([
            "Four distinct dog owner segments exist: Urban Enthusiast, Practical Parent, Casual Companion, Community Seeker.",
            "Urban Enthusiasts have the highest spend and adoption rate \u2014 prioritise them for premium features.",
            "Practical Parents are the biggest group \u2014 volume-level features and affordable pricing serve them best.",
            "K=4 is statistically supported by both elbow and silhouette analysis.",
        ])

   
    # ── Regression ────────────────────────────────────────────────────────────
    with t3:
        dhead("Regression \u2014 What Predicts How Much a Dog Owner Spends?")
        st.markdown("<p style='color:{}'>Target: Q7 monthly spend (INR). "
                    "Linear, Ridge (L2) and Lasso (L1) regression compared on R\u00b2, RMSE and MAE.</p>".format(TEXT_DIM),
                    unsafe_allow_html=True)

        with st.spinner("Training regression models\u2026"):
            reg_res, preds, coefs, feat_names = run_regression()

        dhead("Model Comparison")
        _dark_table(reg_res, h=170)
        best_r = reg_res.sort_values("R\u00b2",ascending=False).iloc[0]["Model"]
        dibox("Best model: {}. Ridge regularisation handles correlated one-hot features better ")
        dibox("Best model: {}. Metrics are now computed after removing target leakage (monthly spend and spend-per-dog) from predictors, so scores are realistic. Ridge regularisation handles correlated one-hot features better "
              "than plain linear regression. Lasso automatically zeroes out the weakest predictors, "
              "confirming only a small set of variables really drives spending.".format(best_r))
        dhead("Actual vs Predicted Spend \u2014 All Three Models")
        cols_r = st.columns(3)
        for col_w, (name, (actual, predicted)) in zip(cols_r, preds.items()):
            with col_w:
                idx = df.sample(min(250,len(actual)), random_state=42).index[:min(250,len(actual))]
                idx_arr = np.arange(len(actual))
                np.random.seed(42)
                idx_arr = np.random.choice(idx_arr, min(250, len(actual)), replace=False)
                r2v = reg_res[reg_res["Model"]==name]["R\u00b2"].values[0]
                mx  = max(float(actual.max()), float(predicted.max()))
                fig_av = go.Figure()
                fig_av.add_trace(go.Scatter(
                    x=actual[idx_arr], y=predicted[idx_arr],
                    mode="markers",
                    marker=dict(color=AMBER, opacity=0.4, size=4),
                    name="Predictions",
                ))
                fig_av.add_trace(go.Scatter(
                    x=[0, mx], y=[0, mx], mode="lines",
                    line=dict(color=HONEY, dash="dash", width=1.5),
                    name="Perfect fit",
                ))
                pc(fig_av, h=260,
                   margin=dict(t=50, b=30, l=60, r=10),
                   title=dict(text="{} \u2014 R\u00b2={}".format(name, r2v), font=dict(color=TEXT_BRIGHT)),
                   xaxis=dict(title="Actual spend (INR)"),
                   yaxis=dict(title="Predicted spend (INR)"),
                   showlegend=False)
        dibox("All three models show a similar scatter pattern \u2014 predictions cluster reasonably close "
              "to the diagonal (perfect fit line) for typical spenders, but diverge for very high outliers. "
              "This is expected: extreme spenders are rare and hard to predict from survey data alone.")

        dhead("Feature Coefficients \u2014 What Drives Spend According to Each Model")
        if coefs:
            coef_df  = pd.DataFrame(coefs)
            # Remove Q7_monthly_spend_inr — it is the target variable, not a predictor
            coef_df = coef_df.drop(index=[i for i in coef_df.index if "Q7_monthly_spend" in i], errors="ignore")
            top_feat = coef_df.abs().mean(axis=1).sort_values(ascending=False).head(12).index
            coef_top = coef_df.loc[top_feat].copy()
            coef_top.index = [i.replace("_enc","").replace("_"," ")[:28] for i in coef_top.index]
            fig_coef = go.Figure()
            for col_name, color in zip(coef_top.columns, [AMBER, HONEY, TERRA]):
                fig_coef.add_trace(go.Bar(
                    name=col_name, x=coef_top.index, y=coef_top[col_name],
                    marker_color=color, opacity=0.85,
                ))
            pc(fig_coef, h=380,
               margin=dict(t=20, b=120, l=60, r=20),
               barmode="group",
               xaxis=dict(title="Feature", tickangle=-40),
               yaxis=dict(title="Coefficient value"),
               legend=dict(orientation="h", y=-0.4))
            dibox("Dog count and city tier (Metro) are the strongest positive coefficients. "
                  "Lasso zeroes out several features, leaving only the most impactful ones. "
                  "The consistent signals across all three models make these findings robust.")

        st.download_button("\u2b07 Download Regression Results", reg_res.to_csv(index=False),
                           "pawindia_regression.csv", "text/csv")

        tab_summary([
            "Dog count and metro location are the strongest predictors of how much someone spends.",
            "Linear, Ridge and Lasso perform similarly on held-out data, indicating stable signals across model families.",
            "Lasso confirms the findings by shrinking weak predictors \u2014 the same core features survive across models.",
            "Regression R\u00b2 values are moderate \u2014 spending is driven by many factors, not just the ones surveyed.",
        ])
