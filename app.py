import streamlit as st
import joblib
import pandas as pd
import random
import textwrap

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="House Price AI Valuation",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# Helper function to render unindented HTML
# -----------------------------------------------------------------------------
def render_html(html_str):
    st.markdown(textwrap.dedent(html_str), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Baseline Defaults & Presets
# -----------------------------------------------------------------------------
DEFAULTS = {
    "OverallQual": 5,
    "OverallCond": 5,
    "GrLivArea": 1500,
    "LotArea": 9000,
    "LotFrontage": 70,
    "GarageCars": 2,
    "GarageArea": 500,
    "TotalBsmtSF": 1000,
    "BsmtFullBath": 1,
    "YearBuilt": 2000,
    "YearRemodAdd": 2005,
    "FullBath": 2,
    "HalfBath": 1,
    "BedroomAbvGr": 3,
    "KitchenAbvGr": 1,
    "TotRmsAbvGrd": 6,
    "Fireplaces": 1,
    "1stFlrSF": 1200,
    "2ndFlrSF": 300,
    "WoodDeckSF": 100,
    "OpenPorchSF": 50,
}

PRESETS = {
    "Budget": {
        "OverallQual": 4,
        "OverallCond": 5,
        "GrLivArea": 950,
        "LotArea": 4500,
        "LotFrontage": 50,
        "GarageCars": 1,
        "GarageArea": 250,
        "TotalBsmtSF": 500,
        "BsmtFullBath": 1,
        "YearBuilt": 1975,
        "YearRemodAdd": 1985,
        "FullBath": 1,
        "HalfBath": 0,
        "BedroomAbvGr": 2,
        "KitchenAbvGr": 1,
        "TotRmsAbvGrd": 4,
        "Fireplaces": 0,
        "1stFlrSF": 900,
        "2ndFlrSF": 0,
        "WoodDeckSF": 0,
        "OpenPorchSF": 20,
    },
    "Family": DEFAULTS,
    "Luxury": {
        "OverallQual": 9,
        "OverallCond": 9,
        "GrLivArea": 3200,
        "LotArea": 18000,
        "LotFrontage": 120,
        "GarageCars": 3,
        "GarageArea": 850,
        "TotalBsmtSF": 1800,
        "BsmtFullBath": 2,
        "YearBuilt": 2021,
        "YearRemodAdd": 2022,
        "FullBath": 3,
        "HalfBath": 1,
        "BedroomAbvGr": 4,
        "KitchenAbvGr": 1,
        "TotRmsAbvGrd": 9,
        "Fireplaces": 2,
        "1stFlrSF": 1800,
        "2ndFlrSF": 1400,
        "WoodDeckSF": 300,
        "OpenPorchSF": 150,
    }
}

# -----------------------------------------------------------------------------
# Modern Sleek Light Theme CSS
# -----------------------------------------------------------------------------
def apply_modern_theme_css():
    render_html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        /* HIDE STREAMLIT TOP HEADER, MENU, STATUS WIDGET, AND SIDEBAR */
        header, [data-testid="stHeader"], #MainMenu, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"], [data-testid="stSidebar"] {
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
        }
        
        /* Global Reset & Typography */
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #0F172A;
        }
        
        .stApp {
            background-color: #F8FAFC;
        }
        
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 100% !important;
        }
        
        /* Top SaaS Header */
        .saas-top-bar {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #2563EB 100%);
            padding: 1.25rem 1.6rem;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.2), 0 8px 10px -6px rgba(15, 23, 42, 0.1);
            margin-bottom: 1.2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .hero-title {
            font-size: 1.65rem;
            font-weight: 800;
            color: #FFFFFF;
            margin: 0;
            letter-spacing: -0.02em;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }
        .hero-subtitle {
            font-size: 0.85rem;
            color: #94A3B8;
            margin-top: 0.2rem;
        }
        
        /* Badges */
        .live-badge {
            background: rgba(16, 185, 129, 0.15);
            color: #10B981;
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 0.3rem 0.8rem;
            border-radius: 9999px;
            font-size: 0.775rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: #10B981;
            border-radius: 50%;
            box-shadow: 0 0 8px #10B981;
        }
        .meta-badge {
            background: rgba(37, 99, 235, 0.12);
            color: #2563EB;
            border: 1px solid rgba(37, 99, 235, 0.25);
            padding: 0.25rem 0.7rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        /* Elevated Light Cards */
        .light-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 1.3rem 1.4rem;
            box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05), 0 2px 4px -2px rgba(15, 23, 42, 0.03);
            margin-bottom: 1.2rem;
            transition: all 0.25s ease;
        }
        .light-card:hover {
            box-shadow: 0 10px 30px -4px rgba(15, 23, 42, 0.08), 0 4px 6px -2px rgba(15, 23, 42, 0.04);
            border-color: #CBD5E1;
        }
        .section-header {
            font-size: 0.85rem;
            font-weight: 800;
            color: #2563EB;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.85rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Prediction Glow Card */
        .prediction-hero-card {
            background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%);
            border-radius: 18px;
            padding: 1.5rem 1.7rem;
            border: 2px solid #2563EB;
            box-shadow: 0 12px 30px -5px rgba(37, 99, 235, 0.15), 0 4px 6px -2px rgba(15, 23, 42, 0.05);
            margin-bottom: 1.2rem;
        }
        .prediction-price {
            font-size: 3rem;
            font-weight: 800;
            color: #2563EB;
            margin: 0.2rem 0;
            line-height: 1.1;
        }

        /* Summary Card Item */
        .summary-card {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 0.85rem 1rem;
            display: flex;
            align-items: center;
            gap: 0.9rem;
            transition: all 0.2s ease;
        }
        .summary-card:hover {
            transform: translateY(-2px);
            border-color: #2563EB;
            background: #FFFFFF;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1);
        }
        .summary-icon {
            font-size: 1.3rem;
            background: rgba(37, 99, 235, 0.1);
            width: 42px;
            height: 42px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            color: #2563EB;
        }
        .summary-title {
            font-size: 0.725rem;
            color: #64748B;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .summary-value {
            font-size: 1.05rem;
            font-weight: 800;
            color: #0F172A;
        }

        /* Button Styling Overrides */
        div.stButton > button {
            background-color: #FFFFFF;
            color: #1E293B;
            border: 1px solid #CBD5E1;
            border-radius: 10px;
            font-weight: 600;
            font-size: 0.875rem;
            padding: 0.5rem 1rem;
            transition: all 0.2s ease;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        }
        div.stButton > button:hover {
            background-color: #2563EB;
            color: #FFFFFF;
            border-color: #2563EB;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
            transform: translateY(-1px);
        }
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            color: #FFFFFF;
            border: none;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
        }
        div.stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
            transform: translateY(-2px);
        }

        /* Custom Labels & Elements */
        label {
            color: #334155 !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
        }

        /* Metric Progress Bar */
        .progress-bar-bg {
            background-color: #E2E8F0;
            border-radius: 9999px;
            height: 8px;
            width: 100%;
            overflow: hidden;
            margin-top: 4px;
        }
        .progress-bar-fill {
            height: 100%;
            border-radius: 9999px;
            transition: width 0.4s ease;
        }
    </style>
    """)

# -----------------------------------------------------------------------------
# Asset Loading (Machine Learning Model)
# -----------------------------------------------------------------------------
@st.cache_resource
def load_ml_assets():
    model = joblib.load("models/house_price_model.pkl")
    columns = joblib.load("models/model_columns.pkl")
    return model, columns

# -----------------------------------------------------------------------------
# Session State Handlers
# -----------------------------------------------------------------------------
def init_session_state():
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "inputs"
    for k, v in DEFAULTS.items():
        if f"key_{k}" not in st.session_state:
            st.session_state[f"key_{k}"] = v
    for k, v in PRESETS["Family"].items():
        if f"key_A_{k}" not in st.session_state:
            st.session_state[f"key_A_{k}"] = v
    for k, v in PRESETS["Family"].items():
        if f"key_B_{k}" not in st.session_state:
            st.session_state[f"key_B_{k}"] = v

def set_preset(preset_name):
    for k, v in PRESETS[preset_name].items():
        st.session_state[f"key_{k}"] = v

def set_preset_compare(prop_prefix, preset_name):
    for k, v in PRESETS[preset_name].items():
        st.session_state[f"key_{prop_prefix}_{k}"] = v

def predict_property(values_dict, model, columns):
    df = pd.DataFrame(0, index=[0], columns=columns)
    for k, v in values_dict.items():
        if k in columns:
            df[k] = v
    return float(model.predict(df)[0])

def reset_inputs():
    for k, v in DEFAULTS.items():
        st.session_state[f"key_{k}"] = v

def randomize_inputs():
    st.session_state["key_OverallQual"] = random.randint(3, 10)
    st.session_state["key_OverallCond"] = random.randint(3, 10)
    st.session_state["key_GrLivArea"] = random.randint(800, 4000)
    st.session_state["key_LotArea"] = random.randint(3000, 25000)
    st.session_state["key_LotFrontage"] = random.randint(40, 150)
    st.session_state["key_GarageCars"] = random.randint(0, 4)
    st.session_state["key_GarageArea"] = random.randint(0, 1000)
    st.session_state["key_TotalBsmtSF"] = random.randint(300, 2500)
    st.session_state["key_BsmtFullBath"] = random.randint(0, 2)
    st.session_state["key_YearBuilt"] = random.randint(1950, 2024)
    st.session_state["key_YearRemodAdd"] = random.randint(st.session_state["key_YearBuilt"], 2024)
    st.session_state["key_FullBath"] = random.randint(1, 4)
    st.session_state["key_HalfBath"] = random.randint(0, 2)
    st.session_state["key_BedroomAbvGr"] = random.randint(2, 6)
    st.session_state["key_KitchenAbvGr"] = 1
    st.session_state["key_TotRmsAbvGrd"] = random.randint(4, 12)
    st.session_state["key_Fireplaces"] = random.randint(0, 3)
    st.session_state["key_1stFlrSF"] = random.randint(600, 2500)
    st.session_state["key_2ndFlrSF"] = random.randint(0, 2000)
    st.session_state["key_WoodDeckSF"] = random.randint(0, 400)
    st.session_state["key_OpenPorchSF"] = random.randint(0, 300)

def get_property_grade(qual):
    if qual >= 8:
        return "Grade A+ (Luxury Executive)", "#059669"
    elif qual == 7:
        return "Grade A (Premium)", "#10B981"
    elif qual == 6:
        return "Grade B+ (Upper Standard)", "#2563EB"
    elif qual == 5:
        return "Grade B (Standard Family)", "#3B82F6"
    else:
        return "Grade C (Economy / Starter)", "#D97706"

# -----------------------------------------------------------------------------
# Main Application Initialization
# -----------------------------------------------------------------------------
apply_modern_theme_css()
init_session_state()
model, columns = load_ml_assets()

# Extract Input Values
input_values = {
    "OverallQual": st.session_state["key_OverallQual"],
    "OverallCond": st.session_state["key_OverallCond"],
    "GrLivArea": st.session_state["key_GrLivArea"],
    "LotArea": st.session_state["key_LotArea"],
    "LotFrontage": st.session_state["key_LotFrontage"],
    "GarageCars": st.session_state["key_GarageCars"],
    "GarageArea": st.session_state["key_GarageArea"],
    "TotalBsmtSF": st.session_state["key_TotalBsmtSF"],
    "BsmtFullBath": st.session_state["key_BsmtFullBath"],
    "YearBuilt": st.session_state["key_YearBuilt"],
    "YearRemodAdd": st.session_state["key_YearRemodAdd"],
    "FullBath": st.session_state["key_FullBath"],
    "HalfBath": st.session_state["key_HalfBath"],
    "BedroomAbvGr": st.session_state["key_BedroomAbvGr"],
    "KitchenAbvGr": st.session_state["key_KitchenAbvGr"],
    "TotRmsAbvGrd": st.session_state["key_TotRmsAbvGrd"],
    "Fireplaces": st.session_state["key_Fireplaces"],
    "1stFlrSF": st.session_state["key_1stFlrSF"],
    "2ndFlrSF": st.session_state["key_2ndFlrSF"],
    "WoodDeckSF": st.session_state["key_WoodDeckSF"],
    "OpenPorchSF": st.session_state["key_OpenPorchSF"],
}

# Real-time Prediction Call
predicted_price = predict_property(input_values, model, columns)
price_per_sqft = predicted_price / input_values["GrLivArea"] if input_values["GrLivArea"] > 0 else 0
property_grade, grade_color = get_property_grade(input_values["OverallQual"])

# Financial Estimates
lower_estimate = predicted_price * 0.95
upper_estimate = predicted_price * 1.05
est_mortgage = (predicted_price * 0.80 * (0.065/12) * ((1 + 0.065/12)**360)) / (((1 + 0.065/12)**360) - 1)

# -----------------------------------------------------------------------------
# Hero Header
# -----------------------------------------------------------------------------
render_html("""
<div class="saas-top-bar">
    <div>
        <div class="hero-title">🏠 House Price Valuation AI</div>
        <div class="hero-subtitle">Real-time machine learning price predictions & property comparison tool</div>
    </div>
    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
        <span class="live-badge"><span class="pulse-dot"></span> Live Random Forest AI</span>
        <span class="meta-badge">Ames Dataset</span>
    </div>
</div>
""")

# -----------------------------------------------------------------------------
# Navigation Bar
# -----------------------------------------------------------------------------
nav_col1, nav_col2 = st.columns(2)
with nav_col1:
    if st.button("🏠 Valuation & Calculator", use_container_width=True, type="primary" if st.session_state.get("current_page") in ["inputs", "results"] else "secondary"):
        st.session_state["current_page"] = "inputs"
        st.rerun()
with nav_col2:
    if st.button("⚔️ Compare 2 Properties", use_container_width=True, type="primary" if st.session_state.get("current_page") == "compare" else "secondary"):
        st.session_state["current_page"] = "compare"
        st.rerun()

render_html("<div style='height: 0.5rem;'></div>")

# -----------------------------------------------------------------------------
# Multi-Page Navigation Logic
# -----------------------------------------------------------------------------
if st.session_state.get("current_page", "inputs") in ["inputs", "results"]:
    
    # Quick Preset Bar
    render_html("<div style='font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 0.4rem;'>⚡ Quick Property Presets</div>")
    
    btn_c1, btn_c2, btn_c3, btn_c4, btn_c5 = st.columns(5)
    with btn_c1:
        if st.button("🪙 Budget Starter", use_container_width=True, help="Set Budget Home inputs"):
            set_preset("Budget")
            st.rerun()
    with btn_c2:
        if st.button("🏡 Family Home", use_container_width=True, help="Set Family Home inputs"):
            set_preset("Family")
            st.rerun()
    with btn_c3:
        if st.button("🏰 Luxury Villa", use_container_width=True, help="Set Luxury Villa inputs"):
            set_preset("Luxury")
            st.rerun()
    with btn_c4:
        if st.button("🎲 Random Sample", use_container_width=True, help="Generate random sample property"):
            randomize_inputs()
            st.rerun()
    with btn_c5:
        if st.button("🔄 Reset Defaults", use_container_width=True, help="Reset to default inputs"):
            reset_inputs()
            st.rerun()

    render_html("<hr style='border-color: #E2E8F0; margin: 0.85rem 0;'>")

    # 2 Column Interactive Workspace
    in_col1, in_col2 = st.columns([0.55, 0.45])

    with in_col1:
        render_html("""
        <div class="light-card">
            <div class="section-header">🏗️ Quality & Built Specifications</div>
        """)
        
        st.slider("⭐ Overall Quality (1-10)", 1, 10, key="key_OverallQual", help="Rates overall material and finish quality")
        st.slider("🏚️ Overall Condition (1-10)", 1, 10, key="key_OverallCond", help="Rates overall condition of property")
        
        ic1, ic2 = st.columns(2)
        with ic1:
            st.number_input("🏠 Year Built", 1800, 2025, key="key_YearBuilt")
        with ic2:
            st.number_input("🔨 Year Remodeled", 1800, 2025, key="key_YearRemodAdd")
        
        render_html("<div style='height: 0.5rem;'></div><div class='section-header'>📏 Dimensions & Square Footage</div>")
        
        dc1, dc2 = st.columns(2)
        with dc1:
            st.number_input("📐 Living Area (sq ft)", 300, 6000, step=50, key="key_GrLivArea")
            st.number_input("🌿 Lot Area (sq ft)", 1000, 250000, step=500, key="key_LotArea")
            st.number_input("🏢 First Floor Area", 0, 4000, step=50, key="key_1stFlrSF")
            st.number_input("🪵 Wood Deck Area", 0, 1000, step=25, key="key_WoodDeckSF")
        with dc2:
            st.number_input("📏 Lot Frontage (ft)", 0, 300, key="key_LotFrontage")
            st.number_input("🧱 Basement Area (sq ft)", 0, 4000, step=50, key="key_TotalBsmtSF")
            st.number_input("🏢 Second Floor Area", 0, 3000, step=50, key="key_2ndFlrSF")
            st.number_input("🌤️ Open Porch Area", 0, 1000, step=25, key="key_OpenPorchSF")

        render_html("<div style='height: 0.5rem;'></div><div class='section-header'>🛏️ Rooms, Bathrooms & Amenities</div>")
        
        rc1, rc2 = st.columns(2)
        with rc1:
            st.number_input("🛏️ Bedrooms", 1, 10, key="key_BedroomAbvGr")
            st.number_input("🚿 Full Bathrooms", 0, 5, key="key_FullBath")
            st.number_input("🚪 Total Rooms", 2, 15, key="key_TotRmsAbvGrd")
            st.number_input("🚗 Garage Capacity (Cars)", 0, 5, key="key_GarageCars")
        with rc2:
            st.number_input("🚽 Half Bathrooms", 0, 3, key="key_HalfBath")
            st.number_input("🚿 Basement Full Bath", 0, 3, key="key_BsmtFullBath")
            st.number_input("🔥 Fireplaces", 0, 4, key="key_Fireplaces")
            st.number_input("🚘 Garage Area (sq ft)", 0, 2000, step=50, key="key_GarageArea")

        render_html("</div>")

    with in_col2:
        # REAL-TIME LIVE PREDICTION DISPLAY
        render_html(f"""
        <div class="prediction-hero-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #64748B; letter-spacing: 0.05em;">
                        💰 Live Estimated Market Price
                    </div>
                    <div class="prediction-price">£{predicted_price:,.2f}</div>
                </div>
                <span class="live-badge"><span class="pulse-dot"></span> Live Model</span>
            </div>
            
            <div style="display: flex; gap: 1rem; margin-top: 0.75rem; font-size: 0.85rem; color: #475569; flex-wrap: wrap;">
                <span>📐 Price / sq ft: <b style="color: #0F172A;">£{price_per_sqft:,.2f}</b></span>
                <span>🏷️ Tier: <b style="color: {grade_color};">{property_grade}</b></span>
            </div>
            
            <div style="margin-top: 1rem; padding-top: 0.85rem; border-top: 1px solid #E2E8F0;">
                <div style="display: flex; justify-content: space-between; font-size: 0.825rem; color: #475569; margin-bottom: 0.4rem;">
                    <span>Valuation Confidence Interval (±5%)</span>
                    <b style="color: #2563EB;">£{lower_estimate:,.0f} – £{upper_estimate:,.0f}</b>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.825rem; color: #475569;">
                    <span>Est. 30-Yr Mortgage (20% Down @ 6.5%)</span>
                    <b style="color: #059669;">~£{est_mortgage:,.0f} / mo</b>
                </div>
            </div>
        </div>
        """)

        # FEATURE IMPORTANCE & VALUE BREAKDOWN
        qual_pct = min(100, (input_values['OverallQual'] / 10) * 100)
        area_pct = min(100, (input_values['GrLivArea'] / 3500) * 100)
        garage_pct = min(100, (input_values['GarageCars'] / 4) * 100)
        age_pct = min(100, ((input_values['YearBuilt'] - 1950) / 75) * 100)

        render_html(f"""
        <div class="light-card">
            <div class="section-header">📊 Feature Impact & Relative Drivers</div>
            
            <div style="margin-bottom: 0.8rem;">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 600; color: #334155;">
                    <span>⭐ Construction Quality ({input_values['OverallQual']}/10)</span>
                    <span style="color: #2563EB;">High Impact</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {qual_pct}%; background-color: #2563EB;"></div>
                </div>
            </div>

            <div style="margin-bottom: 0.8rem;">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 600; color: #334155;">
                    <span>📐 Living Area ({input_values['GrLivArea']:,} sq ft)</span>
                    <span style="color: #059669;">High Impact</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {area_pct}%; background-color: #059669;"></div>
                </div>
            </div>

            <div style="margin-bottom: 0.8rem;">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 600; color: #334155;">
                    <span>🚗 Garage Capacity ({input_values['GarageCars']} Cars)</span>
                    <span style="color: #7C3AED;">Medium Impact</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {garage_pct}%; background-color: #7C3AED;"></div>
                </div>
            </div>

            <div style="margin-bottom: 0.4rem;">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 600; color: #334155;">
                    <span>🏠 Modernity & Age (Built {input_values['YearBuilt']})</span>
                    <span style="color: #D97706;">Moderate Impact</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {age_pct}%; background-color: #D97706;"></div>
                </div>
            </div>
        </div>
        """)

        # QUICK PROPERTY SUMMARY GRID
        render_html(f"""
        <div class="light-card">
            <div class="section-header">📋 Feature Summary Grid</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem;">
                <div class="summary-card">
                    <div class="summary-icon">⭐</div>
                    <div>
                        <div class="summary-title">Quality</div>
                        <div class="summary-value">{input_values['OverallQual']} / 10</div>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="summary-icon">📐</div>
                    <div>
                        <div class="summary-title">Living Area</div>
                        <div class="summary-value">{input_values['GrLivArea']:,} sq ft</div>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="summary-icon">🌿</div>
                    <div>
                        <div class="summary-title">Lot Area</div>
                        <div class="summary-value">{input_values['LotArea']:,} sq ft</div>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="summary-icon">🧱</div>
                    <div>
                        <div class="summary-title">Basement</div>
                        <div class="summary-value">{input_values['TotalBsmtSF']:,} sq ft</div>
                    </div>
                </div>
            </div>
        </div>
        """)

elif st.session_state.get("current_page") == "compare":
    # -------------------------------------------------------------------------
    # PAGE 2: Compare Two Properties Side-by-Side
    # -------------------------------------------------------------------------
    render_html("<div style='font-size: 1.25rem; font-weight: 800; color: #0F172A; margin-bottom: 0.85rem;'>⚔️ Interactive Property Comparison Matrix</div>")
    
    col_A, col_B = st.columns(2)
    
    # PROPERTY A INPUTS
    with col_A:
        render_html("""
        <div class="light-card" style="border-top: 4px solid #2563EB;">
            <div style="font-size: 1.1rem; font-weight: 800; color: #2563EB; margin-bottom: 0.6rem;">🏠 Property A</div>
        """)
        
        pa_c1, pa_c2, pa_c3 = st.columns(3)
        with pa_c1:
            if st.button("🪙 Budget", key="btn_PA_budget", use_container_width=True):
                set_preset_compare("A", "Budget")
                st.rerun()
        with pa_c2:
            if st.button("🏡 Family", key="btn_PA_family", use_container_width=True):
                set_preset_compare("A", "Family")
                st.rerun()
        with pa_c3:
            if st.button("🏰 Luxury", key="btn_PA_luxury", use_container_width=True):
                set_preset_compare("A", "Luxury")
                st.rerun()
                
        render_html("<hr style='border-color: #E2E8F0; margin: 0.6rem 0;'>")
        
        val_A_qual = st.slider("⭐ Overall Quality", 1, 10, value=int(st.session_state.get("key_A_OverallQual", 5)), key="key_A_OverallQual")
        val_A_area = st.number_input("📐 Living Area (sq ft)", 300, 6000, value=int(st.session_state.get("key_A_GrLivArea", 1500)), step=50, key="key_A_GrLivArea")
        val_A_built = st.number_input("🏠 Year Built", 1800, 2025, value=int(st.session_state.get("key_A_YearBuilt", 2000)), key="key_A_YearBuilt")
        val_A_bed = st.number_input("🛏️ Bedrooms", 1, 10, value=int(st.session_state.get("key_A_BedroomAbvGr", 3)), key="key_A_BedroomAbvGr")
        val_A_bath = st.number_input("🚿 Full Bathrooms", 0, 5, value=int(st.session_state.get("key_A_FullBath", 2)), key="key_A_FullBath")
        val_A_cars = st.number_input("🚗 Garage Capacity (Cars)", 0, 5, value=int(st.session_state.get("key_A_GarageCars", 2)), key="key_A_GarageCars")
        val_A_lot = st.number_input("🌿 Lot Area (sq ft)", 1000, 250000, value=int(st.session_state.get("key_A_LotArea", 9000)), step=500, key="key_A_LotArea")
        val_A_bsmt = st.number_input("🧱 Basement Area (sq ft)", 0, 4000, value=int(st.session_state.get("key_A_TotalBsmtSF", 1000)), step=50, key="key_A_TotalBsmtSF")
        val_A_rooms = st.number_input("🚪 Total Rooms", 2, 15, value=int(st.session_state.get("key_A_TotRmsAbvGrd", 6)), key="key_A_TotRmsAbvGrd")
        val_A_fire = st.number_input("🔥 Fireplaces", 0, 4, value=int(st.session_state.get("key_A_Fireplaces", 1)), key="key_A_Fireplaces")
        
        render_html("</div>")

    # PROPERTY B INPUTS
    with col_B:
        render_html("""
        <div class="light-card" style="border-top: 4px solid #059669;">
            <div style="font-size: 1.1rem; font-weight: 800; color: #059669; margin-bottom: 0.6rem;">🏡 Property B</div>
        """)
        
        pb_c1, pb_c2, pb_c3 = st.columns(3)
        with pb_c1:
            if st.button("🪙 Budget", key="btn_PB_budget", use_container_width=True):
                set_preset_compare("B", "Budget")
                st.rerun()
        with pb_c2:
            if st.button("🏡 Family", key="btn_PB_family", use_container_width=True):
                set_preset_compare("B", "Family")
                st.rerun()
        with pb_c3:
            if st.button("🏰 Luxury", key="btn_PB_luxury", use_container_width=True):
                set_preset_compare("B", "Luxury")
                st.rerun()
                
        render_html("<hr style='border-color: #E2E8F0; margin: 0.6rem 0;'>")
        
        val_B_qual = st.slider("⭐ Overall Quality", 1, 10, value=int(st.session_state.get("key_B_OverallQual", 5)), key="key_B_OverallQual")
        val_B_area = st.number_input("📐 Living Area (sq ft)", 300, 6000, value=int(st.session_state.get("key_B_GrLivArea", 1500)), step=50, key="key_B_GrLivArea")
        val_B_built = st.number_input("🏠 Year Built", 1800, 2025, value=int(st.session_state.get("key_B_YearBuilt", 2000)), key="key_B_YearBuilt")
        val_B_bed = st.number_input("🛏️ Bedrooms", 1, 10, value=int(st.session_state.get("key_B_BedroomAbvGr", 3)), key="key_B_BedroomAbvGr")
        val_B_bath = st.number_input("🚿 Full Bathrooms", 0, 5, value=int(st.session_state.get("key_B_FullBath", 2)), key="key_B_FullBath")
        val_B_cars = st.number_input("🚗 Garage Capacity (Cars)", 0, 5, value=int(st.session_state.get("key_B_GarageCars", 2)), key="key_B_GarageCars")
        val_B_lot = st.number_input("🌿 Lot Area (sq ft)", 1000, 250000, value=int(st.session_state.get("key_B_LotArea", 9000)), step=500, key="key_B_LotArea")
        val_B_bsmt = st.number_input("🧱 Basement Area (sq ft)", 0, 4000, value=int(st.session_state.get("key_B_TotalBsmtSF", 1000)), step=50, key="key_B_TotalBsmtSF")
        val_B_rooms = st.number_input("🚪 Total Rooms", 2, 15, value=int(st.session_state.get("key_B_TotRmsAbvGrd", 6)), key="key_B_TotRmsAbvGrd")
        val_B_fire = st.number_input("🔥 Fireplaces", 0, 4, value=int(st.session_state.get("key_B_Fireplaces", 1)), key="key_B_Fireplaces")
        
        render_html("</div>")

    # PREDICTION CALCULATIONS
    values_A = {
        "OverallQual": val_A_qual,
        "GrLivArea": val_A_area,
        "YearBuilt": val_A_built,
        "BedroomAbvGr": val_A_bed,
        "FullBath": val_A_bath,
        "GarageCars": val_A_cars,
        "LotArea": val_A_lot,
        "TotalBsmtSF": val_A_bsmt,
        "TotRmsAbvGrd": val_A_rooms,
        "Fireplaces": val_A_fire,
        "OverallCond": 5,
        "LotFrontage": 70,
        "GarageArea": val_A_cars * 250,
        "BsmtFullBath": 1,
        "YearRemodAdd": val_A_built,
        "HalfBath": 1,
        "KitchenAbvGr": 1,
        "1stFlrSF": val_A_area // 2,
        "2ndFlrSF": val_A_area // 2,
        "WoodDeckSF": 100,
        "OpenPorchSF": 50,
    }
    
    values_B = {
        "OverallQual": val_B_qual,
        "GrLivArea": val_B_area,
        "YearBuilt": val_B_built,
        "BedroomAbvGr": val_B_bed,
        "FullBath": val_B_bath,
        "GarageCars": val_B_cars,
        "LotArea": val_B_lot,
        "TotalBsmtSF": val_B_bsmt,
        "TotRmsAbvGrd": val_B_rooms,
        "Fireplaces": val_B_fire,
        "OverallCond": 5,
        "LotFrontage": 70,
        "GarageArea": val_B_cars * 250,
        "BsmtFullBath": 1,
        "YearRemodAdd": val_B_built,
        "HalfBath": 1,
        "KitchenAbvGr": 1,
        "1stFlrSF": val_B_area // 2,
        "2ndFlrSF": val_B_area // 2,
        "WoodDeckSF": 100,
        "OpenPorchSF": 50,
    }
    
    pred_A = predict_property(values_A, model, columns)
    pred_B = predict_property(values_B, model, columns)
    
    diff = pred_B - pred_A
    pct_diff = (diff / pred_A * 100) if pred_A > 0 else 0
    
    # RESULTS BANNER
    render_html("<div style='height: 0.5rem;'></div><div style='font-size: 1.15rem; font-weight: 800; color: #0F172A; margin-bottom: 0.6rem;'>📊 Valuation Comparison Results</div>")
    
    res_c1, res_c2 = st.columns(2)
    with res_c1:
        render_html(f"""
        <div class="light-card" style="border: 2px solid #2563EB;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase;">🏠 Property A Valuation</div>
            <div style="font-size: 2.4rem; font-weight: 800; color: #2563EB;">£{pred_A:,.2f}</div>
            <div style="font-size: 0.85rem; color: #64748B; margin-top: 0.3rem;">Unit Price: <b>£{pred_A / values_A['GrLivArea']:,.2f} / sq ft</b></div>
        </div>
        """)
        
    with res_c2:
        render_html(f"""
        <div class="light-card" style="border: 2px solid #059669;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase;">🏡 Property B Valuation</div>
            <div style="font-size: 2.4rem; font-weight: 800; color: #059669;">£{pred_B:,.2f}</div>
            <div style="font-size: 0.85rem; color: #64748B; margin-top: 0.3rem;">Unit Price: <b>£{pred_B / values_B['GrLivArea']:,.2f} / sq ft</b></div>
        </div>
        """)

    # Difference Summary Box
    if diff > 0:
        diff_text = f"💡 <b>Property B</b> is valued at <b style='color: #059669;'>+£{diff:,.2f} (+{pct_diff:.1f}%) higher</b> than Property A."
        diff_border = "#059669"
        diff_bg = "#ECFDF5"
    elif diff < 0:
        diff_text = f"💡 <b>Property A</b> is valued at <b style='color: #2563EB;'>+£{abs(diff):,.2f} (+{abs(pct_diff):.1f}%) higher</b> than Property B."
        diff_border = "#2563EB"
        diff_bg = "#EFF6FF"
    else:
        diff_text = "💡 Both properties have equal predicted valuation."
        diff_border = "#94A3B8"
        diff_bg = "#F8FAFC"
        
    render_html(f"""
    <div style="background: {diff_bg}; border: 1px solid {diff_border}; padding: 1rem 1.25rem; border-radius: 14px; font-size: 0.95rem; color: #0F172A; margin-bottom: 1.2rem;">
        {diff_text}
    </div>
    """)

    # FEATURE MATRIX TABLE
    table_header = '<div class="light-card" style="padding: 1.4rem;"><div style="font-size: 1.05rem; font-weight: 800; color: #0F172A; margin-bottom: 1rem;">📋 Side-by-Side Feature Matrix</div><table style="width: 100%; border-collapse: collapse; font-size: 0.92rem;"><thead><tr style="border-bottom: 2px solid #E2E8F0; color: #64748B; text-align: left;"><th style="padding: 0.75rem 1rem; width: 35%;">Feature</th><th style="padding: 0.75rem 1rem; width: 25%; color: #2563EB;">Property A</th><th style="padding: 0.75rem 1rem; width: 25%; color: #059669;">Property B</th><th style="padding: 0.75rem 1rem; width: 15%; text-align: right;">Winner</th></tr></thead><tbody>'
    
    matrix_features = [
        ("⭐ Overall Quality", val_A_qual, val_B_qual, "/ 10"),
        ("📐 Living Area", f"{val_A_area:,}", f"{val_B_area:,}", "sq ft"),
        ("🏠 Year Built", val_A_built, val_B_built, ""),
        ("🛏️ Bedrooms", val_A_bed, val_B_bed, "Beds"),
        ("🚿 Full Bathrooms", val_A_bath, val_B_bath, "Baths"),
        ("🚗 Garage Capacity", val_A_cars, val_B_cars, "Cars"),
        ("🌿 Lot Area", f"{val_A_lot:,}", f"{val_B_lot:,}", "sq ft"),
        ("🧱 Basement Area", f"{val_A_bsmt:,}", f"{val_B_bsmt:,}", "sq ft"),
        ("🚪 Total Rooms", val_A_rooms, val_B_rooms, "Rooms"),
        ("🔥 Fireplaces", val_A_fire, val_B_fire, "Fireplaces"),
    ]
    
    rows_html = ""
    for label, valA, valB, unit in matrix_features:
        numA = float(str(valA).replace(',', ''))
        numB = float(str(valB).replace(',', ''))
        if numA > numB:
            comp_badge = "<span style='background: rgba(37, 99, 235, 0.12); color: #2563EB; padding: 0.2rem 0.6rem; border-radius: 9999px; font-weight: 700; font-size: 0.75rem;'>A is Higher</span>"
        elif numB > numA:
            comp_badge = "<span style='background: rgba(5, 150, 105, 0.12); color: #059669; padding: 0.2rem 0.6rem; border-radius: 9999px; font-weight: 700; font-size: 0.75rem;'>B is Higher</span>"
        else:
            comp_badge = "<span style='background: #F1F5F9; color: #64748B; padding: 0.2rem 0.6rem; border-radius: 9999px; font-weight: 600; font-size: 0.75rem;'>Equal</span>"
            
        rows_html += f"<tr style='border-bottom: 1px solid #F1F5F9;'><td style='padding: 0.75rem 1rem; color: #0F172A; font-weight: 600;'>{label}</td><td style='padding: 0.75rem 1rem; color: #475569;'>{valA} {unit}</td><td style='padding: 0.75rem 1rem; color: #475569;'>{valB} {unit}</td><td style='padding: 0.75rem 1rem; text-align: right;'>{comp_badge}</td></tr>"
        
    full_table_html = table_header + rows_html + "</tbody></table></div>"
    render_html(full_table_html)