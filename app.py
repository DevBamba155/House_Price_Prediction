import streamlit as st
import joblib
import pandas as pd
import random

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
# Robust Bulletproof HTML Renderer (Strips ALL leading indentation)
# -----------------------------------------------------------------------------
def render_html(html_str):
    clean = "\n".join([line.lstrip() for line in html_str.strip().splitlines()])
    st.markdown(clean, unsafe_allow_html=True)

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
    box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.2);
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
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
    margin-bottom: 1.2rem;
}
.section-header {
    font-size: 0.85rem;
    font-weight: 800;
    color: #2563EB;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.85rem;
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
}
div.stButton > button:hover {
    background-color: #2563EB;
    color: #FFFFFF;
    border-color: #2563EB;
    transform: translateY(-1px);
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    color: #FFFFFF;
    border: none;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
}

label {
    color: #334155 !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
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
        # REAL-TIME LIVE PREDICTION DISPLAY (Native Streamlit Containers + Metrics)
        with st.container(border=True):
            st.subheader("💰 Live Estimated Market Price")
            st.metric(
                label="Random Forest Model Prediction",
                value=f"£{predicted_price:,.2f}",
                delta=f"£{price_per_sqft:,.2f} / sq ft ({property_grade})"
            )
            
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.caption("Valuation Range (±5%)")
                st.write(f"**£{lower_estimate:,.0f} – £{upper_estimate:,.0f}**")
            with m_col2:
                st.caption("Est. 30-Yr Mortgage (20% Down @ 6.5%)")
                st.write(f"**~£{est_mortgage:,.0f} / mo**")

        # FEATURE IMPORTANCE & VALUE BREAKDOWN (Native Streamlit Progress Bars)
        with st.container(border=True):
            st.subheader("📊 Feature Impact & Relative Drivers")
            
            qual_pct = min(1.0, (input_values['OverallQual'] / 10.0))
            area_pct = min(1.0, (input_values['GrLivArea'] / 3500.0))
            garage_pct = min(1.0, (input_values['GarageCars'] / 4.0))
            age_pct = min(1.0, max(0.0, (input_values['YearBuilt'] - 1950) / 75.0))

            st.write(f"**⭐ Construction Quality ({input_values['OverallQual']}/10)** - High Impact")
            st.progress(qual_pct)
            
            st.write(f"**📐 Living Area ({input_values['GrLivArea']:,} sq ft)** - High Impact")
            st.progress(area_pct)
            
            st.write(f"**🚗 Garage Capacity ({input_values['GarageCars']} Cars)** - Medium Impact")
            st.progress(garage_pct)

            st.write(f"**🏠 Modernity & Age (Built {input_values['YearBuilt']})** - Moderate Impact")
            st.progress(age_pct)

        # QUICK PROPERTY SUMMARY GRID (Native Streamlit Metrics)
        with st.container(border=True):
            st.subheader("📋 Feature Summary Grid")
            sg1, sg2 = st.columns(2)
            with sg1:
                st.metric("Overall Quality", f"{input_values['OverallQual']} / 10")
                st.metric("Living Area", f"{input_values['GrLivArea']:,} sq ft")
            with sg2:
                st.metric("Lot Area", f"{input_values['LotArea']:,} sq ft")
                st.metric("Basement Area", f"{input_values['TotalBsmtSF']:,} sq ft")

elif st.session_state.get("current_page") == "compare":
    # -------------------------------------------------------------------------
    # PAGE 2: Compare Two Properties Side-by-Side
    # -------------------------------------------------------------------------
    st.header("⚔️ Interactive Property Comparison Matrix")
    
    col_A, col_B = st.columns(2)
    
    # PROPERTY A INPUTS
    with col_A:
        with st.container(border=True):
            st.subheader("🏠 Property A")
            
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

    # PROPERTY B INPUTS
    with col_B:
        with st.container(border=True):
            st.subheader("🏡 Property B")
            
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
    st.subheader("📊 Valuation Comparison Results")
    
    res_c1, res_c2 = st.columns(2)
    with res_c1:
        st.metric("Property A Valuation", f"£{pred_A:,.2f}", f"£{pred_A / values_A['GrLivArea']:,.2f} / sq ft")
    with res_c2:
        st.metric("Property B Valuation", f"£{pred_B:,.2f}", f"£{pred_B / values_B['GrLivArea']:,.2f} / sq ft")

    # Difference Summary Box
    if diff > 0:
        st.success(f"💡 **Property B** is valued at **+£{diff:,.2f} (+{pct_diff:.1f}%) higher** than Property A.")
    elif diff < 0:
        st.info(f"💡 **Property A** is valued at **+£{abs(diff):,.2f} (+{abs(pct_diff):.1f}%) higher** than Property B.")
    else:
        st.warning("💡 Both properties have equal predicted valuation.")

    # FEATURE MATRIX TABLE (Using Streamlit Dataframe / Table)
    st.subheader("📋 Side-by-Side Feature Matrix")
    
    matrix_features = [
        {"Feature": "⭐ Overall Quality", "Property A": f"{val_A_qual} / 10", "Property B": f"{val_B_qual} / 10", "Comparison": "Property B Higher" if val_B_qual > val_A_qual else ("Property A Higher" if val_A_qual > val_B_qual else "Equal")},
        {"Feature": "📐 Living Area", "Property A": f"{val_A_area:,} sq ft", "Property B": f"{val_B_area:,} sq ft", "Comparison": "Property B Higher" if val_B_area > val_A_area else ("Property A Higher" if val_A_area > val_B_area else "Equal")},
        {"Feature": "🏠 Year Built", "Property A": str(val_A_built), "Property B": str(val_B_built), "Comparison": "Property B Newer" if val_B_built > val_A_built else ("Property A Newer" if val_A_built > val_B_built else "Equal")},
        {"Feature": "🛏️ Bedrooms", "Property A": str(val_A_bed), "Property B": str(val_B_bed), "Comparison": "Property B Higher" if val_B_bed > val_A_bed else ("Property A Higher" if val_A_bed > val_B_bed else "Equal")},
        {"Feature": "🚿 Full Bathrooms", "Property A": str(val_A_bath), "Property B": str(val_B_bath), "Comparison": "Property B Higher" if val_B_bath > val_A_bath else ("Property A Higher" if val_A_bath > val_B_bath else "Equal")},
        {"Feature": "🚗 Garage Capacity", "Property A": f"{val_A_cars} Cars", "Property B": f"{val_B_cars} Cars", "Comparison": "Property B Higher" if val_B_cars > val_A_cars else ("Property A Higher" if val_A_cars > val_B_cars else "Equal")},
        {"Feature": "🌿 Lot Area", "Property A": f"{val_A_lot:,} sq ft", "Property B": f"{val_B_lot:,} sq ft", "Comparison": "Property B Higher" if val_B_lot > val_A_lot else ("Property A Higher" if val_A_lot > val_B_lot else "Equal")},
        {"Feature": "🧱 Basement Area", "Property A": f"{val_A_bsmt:,} sq ft", "Property B": f"{val_B_bsmt:,} sq ft", "Comparison": "Property B Higher" if val_B_bsmt > val_A_bsmt else ("Property A Higher" if val_A_bsmt > val_B_bsmt else "Equal")},
        {"Feature": "🚪 Total Rooms", "Property A": str(val_A_rooms), "Property B": str(val_B_rooms), "Comparison": "Property B Higher" if val_B_rooms > val_A_rooms else ("Property A Higher" if val_A_rooms > val_B_rooms else "Equal")},
        {"Feature": "🔥 Fireplaces", "Property A": str(val_A_fire), "Property B": str(val_B_fire), "Comparison": "Property B Higher" if val_B_fire > val_A_fire else ("Property A Higher" if val_A_fire > val_B_fire else "Equal")},
    ]
    
    st.table(pd.DataFrame(matrix_features))