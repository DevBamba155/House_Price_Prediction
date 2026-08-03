import streamlit as st
import joblib
import pandas as pd
import random

# -----------------------------------------------------------------------------
# Page Configuration (Sidebar Collapsed)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="HOUSE PREDICTION",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
# Premium Dark Theme CSS (Hiding Streamlit Top Header Bar Completely)
# -----------------------------------------------------------------------------
def apply_dark_theme_css():
    st.markdown("""
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
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
            color: #F9FAFB;
        }
        
        .stApp {
            background-color: #0B1120;
        }
        
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 100% !important;
        }
        
        /* Top SaaS Header */
        .saas-top-bar {
            background: linear-gradient(135deg, #111827 0%, #1e293b 60%, #1e3a8a 100%);
            padding: 1.1rem 1.6rem;
            border-radius: 14px;
            border: 1px solid #1F2937;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            margin-bottom: 1.2rem;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            gap: 0.75rem;
        }
        .hero-title {
            font-size: 1.65rem;
            font-weight: 800;
            color: #F9FAFB;
            margin: 0;
            letter-spacing: -0.02em;
            text-align: center;
        }
        .hero-subtitle {
            font-size: 0.85rem;
            color: #94A3B8;
            margin-top: 0.15rem;
        }
        
        /* Badges */
        .live-badge {
            background: rgba(34, 197, 94, 0.15);
            color: #4ADE80;
            border: 1px solid rgba(34, 197, 94, 0.3);
            padding: 0.25rem 0.7rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: #22C55E;
            border-radius: 50%;
            box-shadow: 0 0 8px #22C55E;
        }
        .meta-badge {
            background: rgba(59, 130, 246, 0.15);
            color: #60A5FA;
            border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 0.25rem 0.65rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        /* Dark Card Container */
        .dark-card {
            background-color: #111827;
            border-radius: 14px;
            padding: 1.25rem;
            border: 1px solid #1F2937;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
            margin-bottom: 1rem;
        }
        .card-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #F9FAFB;
            margin-bottom: 0.85rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        /* Prediction Glow Card */
        .prediction-hero-card {
            background: linear-gradient(135deg, #111827 0%, #0F172A 100%);
            border-radius: 16px;
            padding: 1.4rem 1.6rem;
            border: 1px solid #3B82F6;
            box-shadow: 0 0 25px rgba(59, 130, 246, 0.25), 0 10px 25px -5px rgba(0, 0, 0, 0.6);
            margin-bottom: 1rem;
        }
        .prediction-price {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FFFFFF 0%, #60A5FA 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0.15rem 0;
            line-height: 1.1;
        }
        
        /* Summary Metric Card Item */
        .summary-card {
            background: #1F2937;
            border: 1px solid #374151;
            border-radius: 12px;
            padding: 0.85rem 0.95rem;
            display: flex;
            align-items: center;
            gap: 0.85rem;
            transition: all 0.2s ease;
        }
        .summary-card:hover {
            transform: translateY(-2px);
            border-color: #3B82F6;
        }
        .summary-icon {
            font-size: 1.35rem;
            background: rgba(59, 130, 246, 0.12);
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            color: #60A5FA;
        }
        .summary-title {
            font-size: 0.725rem;
            color: #94A3B8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .summary-value {
            font-size: 1.05rem;
            font-weight: 700;
            color: #F9FAFB;
        }
        
        /* Input Labels & Buttons */
        div.stButton > button {
            background-color: #1F2937;
            color: #F9FAFB;
            border: 1px solid #374151;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            background-color: #3B82F6;
            color: #FFFFFF;
            border-color: #3B82F6;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35);
        }
        
        label {
            color: #E2E8F0 !important;
            font-size: 0.825rem !important;
            font-weight: 600 !important;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 0.55rem 0;
            border-bottom: 1px solid #1F2937;
            font-size: 0.85rem;
        }
        .info-row:last-child {
            border-bottom: none;
        }
        .info-label {
            color: #94A3B8;
            font-weight: 500;
        }
        .info-val {
            color: #F9FAFB;
            font-weight: 700;
        }
    </style>
    """, unsafe_allow_html=True)

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
        return "Grade A+ (Luxury Executive)", "#22C55E"
    elif qual == 7:
        return "Grade A (Premium)", "#10B981"
    elif qual == 6:
        return "Grade B+ (Upper Standard)", "#3B82F6"
    elif qual == 5:
        return "Grade B (Standard Family)", "#60A5FA"
    else:
        return "Grade C (Economy / Starter)", "#F59E0B"

def generate_printable_report(input_values, price, price_per_sqft, grade):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Valuation Appraisal Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0B1120; color: #F9FAFB; padding: 30px; }}
            .header {{ border-bottom: 2px solid #3B82F6; padding-bottom: 15px; margin-bottom: 20px; }}
            .title {{ font-size: 24px; font-weight: bold; color: #F9FAFB; }}
            .price-box {{ background: #111827; border: 1px solid #3B82F6; padding: 20px; border-radius: 12px; margin-bottom: 20px; }}
            .price {{ font-size: 32px; font-weight: bold; color: #60A5FA; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; background: #111827; border-radius: 8px; overflow: hidden; }}
            th, td {{ padding: 12px; border-bottom: 1px solid #1F2937; text-align: left; }}
            th {{ background: #1F2937; color: #94A3B8; font-size: 12px; text-transform: uppercase; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">🏠 AI Real Estate Valuation Report</div>
            <div style="color: #94A3B8;">Model: Random Forest Regressor | Dataset: Ames Housing</div>
        </div>
        <div class="price-box">
            <div style="color: #94A3B8; text-transform: uppercase; font-size: 12px;">Estimated Market Value</div>
            <div class="price">£{price:,.2f}</div>
            <div style="margin-top: 8px; color: #94A3B8;">Unit Price: £{price_per_sqft:,.2f} / sq ft | Classification: {grade}</div>
        </div>
        <h3 style="color: #F9FAFB;">Property Feature Summary</h3>
        <table>
            <tr><th>Feature</th><th>Value</th></tr>
            <tr><td>Overall Quality</td><td>{input_values['OverallQual']} / 10</td></tr>
            <tr><td>Living Area</td><td>{input_values['GrLivArea']:,} sq ft</td></tr>
            <tr><td>Lot Area</td><td>{input_values['LotArea']:,} sq ft</td></tr>
            <tr><td>Garage Capacity</td><td>{input_values['GarageCars']} Cars</td></tr>
            <tr><td>Basement Area</td><td>{input_values['TotalBsmtSF']:,} sq ft</td></tr>
            <tr><td>Year Built</td><td>{input_values['YearBuilt']}</td></tr>
            <tr><td>Full Bathrooms</td><td>{input_values['FullBath']}</td></tr>
            <tr><td>Bedrooms</td><td>{input_values['BedroomAbvGr']}</td></tr>
            <tr><td>Total Rooms</td><td>{input_values['TotRmsAbvGrd']}</td></tr>
            <tr><td>Fireplaces</td><td>{input_values['Fireplaces']}</td></tr>
        </table>
    </body>
    </html>
    """

# -----------------------------------------------------------------------------
# Main Application Initialization
# -----------------------------------------------------------------------------
apply_dark_theme_css()
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

# -----------------------------------------------------------------------------
# ML Inference Engine (100% UNTOUCHED LOGIC)
# -----------------------------------------------------------------------------
input_data = pd.DataFrame(0, index=[0], columns=columns)

input_data["OverallQual"] = input_values["OverallQual"]
input_data["OverallCond"] = input_values["OverallCond"]

input_data["GrLivArea"] = input_values["GrLivArea"]
input_data["LotArea"] = input_values["LotArea"]
input_data["LotFrontage"] = input_values["LotFrontage"]

input_data["GarageCars"] = input_values["GarageCars"]
input_data["GarageArea"] = input_values["GarageArea"]

input_data["TotalBsmtSF"] = input_values["TotalBsmtSF"]
input_data["BsmtFullBath"] = input_values["BsmtFullBath"]

input_data["YearBuilt"] = input_values["YearBuilt"]
input_data["YearRemodAdd"] = input_values["YearRemodAdd"]

input_data["FullBath"] = input_values["FullBath"]
input_data["HalfBath"] = input_values["HalfBath"]

input_data["BedroomAbvGr"] = input_values["BedroomAbvGr"]
input_data["KitchenAbvGr"] = input_values["KitchenAbvGr"]
input_data["TotRmsAbvGrd"] = input_values["TotRmsAbvGrd"]

input_data["Fireplaces"] = input_values["Fireplaces"]

input_data["1stFlrSF"] = input_values["1stFlrSF"]
input_data["2ndFlrSF"] = input_values["2ndFlrSF"]

input_data["WoodDeckSF"] = input_values["WoodDeckSF"]
input_data["OpenPorchSF"] = input_values["OpenPorchSF"]

# Real-time Prediction Call
prediction = model.predict(input_data)
predicted_price = float(prediction[0])
price_per_sqft = predicted_price / input_values["GrLivArea"] if input_values["GrLivArea"] > 0 else 0
property_grade, grade_color = get_property_grade(input_values["OverallQual"])

# Interactive Derived Financial Calculations
lower_estimate = predicted_price * 0.95
upper_estimate = predicted_price * 1.05
est_mortgage = (predicted_price * 0.80 * (0.065/12) * ((1 + 0.065/12)**360)) / (((1 + 0.065/12)**360) - 1)

# -----------------------------------------------------------------------------
# Top Hero Header (Without Streamlit Toolbar)
# -----------------------------------------------------------------------------
st.markdown("""
<div class="saas-top-bar">
    <div class="hero-title">HOUSE PREDICTION</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Top Navigation Bar (Valuation Calculator vs Compare 2 Homes)
# -----------------------------------------------------------------------------
nav_col1, nav_col2 = st.columns(2)
with nav_col1:
    if st.button("🏠 Valuation Calculator", use_container_width=True, type="primary" if st.session_state.get("current_page") in ["inputs", "results"] else "secondary"):
        st.session_state["current_page"] = "inputs"
        st.rerun()
with nav_col2:
    if st.button("⚔️ Compare 2 Properties", use_container_width=True, type="primary" if st.session_state.get("current_page") == "compare" else "secondary"):
        st.session_state["current_page"] = "compare"
        st.rerun()

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Multi-Page Navigation Logic (Inputs Page vs Results Page vs Compare Page)
# -----------------------------------------------------------------------------
if st.session_state.get("current_page", "inputs") == "inputs":
    # -------------------------------------------------------------------------
    # PAGE 1: House Configuration Inputs
    # -------------------------------------------------------------------------

        
    # Presets & Quick Action Bar
    btn_c1, btn_c2, btn_c3, btn_c4, btn_c5 = st.columns(5)
    with btn_c1:
        if st.button("🪙 Budget", use_container_width=True, help="Set Budget Home inputs"):
            set_preset("Budget")
            st.rerun()
    with btn_c2:
        if st.button("🏡 Family", use_container_width=True, help="Set Family Home inputs"):
            set_preset("Family")
            st.rerun()
    with btn_c3:
        if st.button("🏰 Luxury", use_container_width=True, help="Set Luxury Villa inputs"):
            set_preset("Luxury")
            st.rerun()
    with btn_c4:
        if st.button("🎲 Random", use_container_width=True, help="Generate random sample property"):
            randomize_inputs()
            st.rerun()
    with btn_c5:
        if st.button("🔄 Reset", use_container_width=True, help="Reset to default inputs"):
            reset_inputs()
            st.rerun()

    st.markdown("<hr style='border-color: #1F2937; margin: 0.75rem 0;'>", unsafe_allow_html=True)

    # 2 Interactive Sub-columns
    in_col1, in_col2 = st.columns(2)

    with in_col1:
        st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; margin-bottom: 0.4rem;'>🏗️ Quality & Built</div>", unsafe_allow_html=True)
        
        st.slider(
            "⭐ Overall Quality (1-10)",
            min_value=1,
            max_value=10,
            key="key_OverallQual",
            help="Rates material and finish quality of the house"
        )
        st.slider(
            "🏚️ Overall Condition (1-10)",
            min_value=1,
            max_value=10,
            key="key_OverallCond",
        )
        st.number_input(
            "🏠 Year Built",
            min_value=1800,
            max_value=2025,
            key="key_YearBuilt",
            help="Original construction year"
        )
        st.number_input(
        "🔨 Year Remodeled",
        min_value=1800,
        max_value=2025,
        key="key_YearRemodAdd",
        )
        
        st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; margin-top: 0.75rem; margin-bottom: 0.4rem;'>📏 Dimensions & Area</div>", unsafe_allow_html=True)
        
        st.number_input(
            "📐 Living Area (sq ft)",
            min_value=300,
            max_value=6000,
            step=50,
            key="key_GrLivArea",
            help="Above grade living area in sq ft"
        )
        st.number_input(
            "🌿 Lot Area (sq ft)",
            min_value=1000,
            max_value=250000,
            step=500,
            key="key_LotArea",
            help="Total lot area in sq ft"
        )
        st.number_input(
        "📏 Lot Frontage (ft)",
        min_value=0,
        max_value=300,
        key="key_LotFrontage",
        )
        st.number_input(
            "🧱 Basement Area (sq ft)",
            min_value=0,
            max_value=4000,
            step=50,
            key="key_TotalBsmtSF",
            help="Total basement square feet"
        )
        st.number_input(
        "🏢 First Floor Area",
        min_value=0,
        max_value=4000,
        key="key_1stFlrSF",
        )
        st.number_input(
            "🏢 Second Floor Area",
            min_value=0,
            max_value=3000,
            key="key_2ndFlrSF",
        )

        st.number_input(
            "🪵 Wood Deck Area",
            min_value=0,
            max_value=1000,
            key="key_WoodDeckSF",
        )

        st.number_input(
            "🌤️ Open Porch Area",
            min_value=0,
            max_value=1000,
            key="key_OpenPorchSF",
        )

    with in_col2:
        st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; margin-bottom: 0.4rem;'>🛌 Rooms & Layout</div>", unsafe_allow_html=True)
        
        st.number_input(
            "🛏️ Bedrooms",
            min_value=1,
            max_value=10,
            key="key_BedroomAbvGr",
            help="Bedrooms above ground level"
        )
        st.number_input(
            "🚿 Full Bathrooms",
            min_value=0,
            max_value=5,
            key="key_FullBath",
            help="Full bathrooms above ground"
        )
        st.number_input(
        "🚿 Basement Full Bath",
        min_value=0,
        max_value=3,
        key="key_BsmtFullBath",
        )

        st.number_input(
            "🚽 Half Bath",
            min_value=0,
            max_value=3,
            key="key_HalfBath",
        )

        st.number_input(
            "🍳 Kitchens",
            min_value=0,
            max_value=3,
            key="key_KitchenAbvGr",
        )
        st.number_input(
            "🚪 Total Rooms",
            min_value=2,
            max_value=15,
            key="key_TotRmsAbvGrd",
            help="Total rooms above ground"
        )
        
        st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; margin-top: 0.75rem; margin-bottom: 0.4rem;'>🚗 Garage & Amenities</div>", unsafe_allow_html=True)
        
        st.number_input(
            "🚗 Garage Capacity (Cars)",
            min_value=0,
            max_value=5,
            key="key_GarageCars",
            help="Size of garage in car capacity"
        )
        st.number_input(
        "🚘 Garage Area (sq ft)",
        min_value=0,
        max_value=2000,
        key="key_GarageArea",
        )
        st.number_input(
            "🔥 Fireplaces",
            min_value=0,
            max_value=4,
            key="key_Fireplaces",
            help="Number of fireplaces"
        )



    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    if st.button("✨ Calculate Valuation & Predict Price 🚀", use_container_width=True, type="primary"):
        st.session_state["current_page"] = "results"
        st.rerun()

elif st.session_state.get("current_page") == "results":
    # -------------------------------------------------------------------------
    # PAGE 2: Valuation Prediction & Detailed Summary Report
    # -------------------------------------------------------------------------
    nav_c1, nav_c2 = st.columns([0.75, 0.25])
    with nav_c1:
        st.markdown("<div style='font-size: 1.15rem; font-weight: 700; color: #F9FAFB; margin-bottom: 0.75rem;'>📊 Valuation Appraisal & Prediction Report</div>", unsafe_allow_html=True)
    with nav_c2:
        if st.button("⚙️ Edit House Inputs", use_container_width=True, type="secondary"):
            st.session_state["current_page"] = "inputs"
            st.rerun()

    # 1. Prediction Hero Card
    st.markdown(f"""
    <div class="prediction-hero-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
            <div>
                <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #94A3B8; letter-spacing: 0.06em;">
                    💰 Live Model Prediction
                </div>
                <div class="prediction-price">£{predicted_price:,.2f}</div>
            </div>
            <span class="live-badge"><span class="pulse-dot"></span> Active Prediction</span>
        </div>
        <div style="display: flex; gap: 1.2rem; margin-top: 0.6rem; font-size: 0.85rem; color: #94A3B8; flex-wrap: wrap;">
            <span>📐 Unit Price: <b style="color: #F9FAFB;">£{price_per_sqft:,.2f} / sq ft</b></span>
            <span>🏷️ Classification: <b style="color: {grade_color};">{property_grade}</b></span>
        </div>
        <div style="margin-top: 0.75rem; padding-top: 0.65rem; border-top: 1px solid rgba(59, 130, 246, 0.2); display: flex; justify-content: space-between; font-size: 0.8rem; color: #94A3B8;">
            <span>Est. Range (±5%): <b style="color: #60A5FA;">£{lower_estimate:,.0f} – £{upper_estimate:,.0f}</b></span>
            <span>Est. Monthly Mortgage: <b style="color: #34D399;">~£{est_mortgage:,.0f} / mo</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. House Summary Card Grid
    st.markdown("<div style='font-size: 0.95rem; font-weight: 700; color: #F9FAFB; margin-bottom: 0.6rem;'>📋 Property Details Summary</div>", unsafe_allow_html=True)

    sg1, sg2 = st.columns(2)
    with sg1:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-icon">⭐</div>
            <div>
                <div class="summary-title">Overall Quality</div>
                <div class="summary-value">{input_values['OverallQual']} / 10</div>
            </div>
        </div>
        <div style="height: 8px;"></div>
        <div class="summary-card">
            <div class="summary-icon">📐</div>
            <div>
                <div class="summary-title">Living Area</div>
                <div class="summary-value">{input_values['GrLivArea']:,} sq ft</div>
            </div>
        </div>
        <div style="height: 8px;"></div>
        <div class="summary-card">
            <div class="summary-icon">🌿</div>
            <div>
                <div class="summary-title">Lot Area</div>
                <div class="summary-value">{input_values['LotArea']:,} sq ft</div>
            </div>
        </div>
        <div style="height: 8px;"></div>
        <div class="summary-card">
            <div class="summary-icon">🧱</div>
            <div>
                <div class="summary-title">Basement Area</div>
                <div class="summary-value">{input_values['TotalBsmtSF']:,} sq ft</div>
            </div>
        </div>
        <div style="height: 8px;"></div>
        <div class="summary-card">
            <div class="summary-icon">🚗</div>
            <div>
                <div class="summary-title">Garage Capacity</div>
                <div class="summary-value">{input_values['GarageCars']} Cars</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sg2:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-icon">🏠</div>
            <div>
                <div class="summary-title">Year Built</div>
                <div class="summary-value">{input_values['YearBuilt']}</div>
            </div>
        </div>
        <div style="height: 8px;"></div>
        <div class="summary-card">
            <div class="summary-icon">🛏️</div>
            <div>
                <div class="summary-title">Bedrooms</div>
                <div class="summary-value">{input_values['BedroomAbvGr']}</div>
            </div>
        </div>
        <div style="height: 8px;"></div>
        <div class="summary-card">
            <div class="summary-icon">🚿</div>
            <div>
                <div class="summary-title">Full Bathrooms</div>
                <div class="summary-value">{input_values['FullBath']}</div>
            </div>
        </div>
        <div style="height: 8px;"></div>
        <div class="summary-card">
            <div class="summary-icon">🚪</div>
            <div>
                <div class="summary-title">Total Rooms</div>
                <div class="summary-value">{input_values['TotRmsAbvGrd']}</div>
            </div>
        </div>
        <div style="height: 8px;"></div>
        <div class="summary-card">
            <div class="summary-icon">🔥</div>
            <div>
                <div class="summary-title">Fireplaces</div>
                <div class="summary-value">{input_values['Fireplaces']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    if st.button("⬅️ Modify House Configuration & Recalculate", use_container_width=True, type="primary"):
        st.session_state["current_page"] = "inputs"
        st.rerun()

elif st.session_state.get("current_page") == "compare":
    # -------------------------------------------------------------------------
    # PAGE 3: Compare Two Properties Side-by-Side
    # -------------------------------------------------------------------------
    st.markdown("<div style='font-size: 1.2rem; font-weight: 800; color: #F9FAFB; margin-bottom: 0.85rem;'>⚔️ Side-by-Side Property Comparison</div>", unsafe_allow_html=True)
    
    col_A, col_B = st.columns(2)
    
    # ------------------ PROPERTY A INPUTS ------------------
    with col_A:
        st.markdown("""
        <div class="dark-card" style="border-left: 4px solid #3B82F6;">
            <div style="font-size: 1.05rem; font-weight: 700; color: #60A5FA; margin-bottom: 0.6rem;">🏠 Property A</div>
        """, unsafe_allow_html=True)
        
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
                
        st.markdown("<hr style='border-color: #1F2937; margin: 0.6rem 0;'>", unsafe_allow_html=True)
        
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
        
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------ PROPERTY B INPUTS ------------------
    with col_B:
        st.markdown("""
        <div class="dark-card" style="border-left: 4px solid #10B981;">
            <div style="font-size: 1.05rem; font-weight: 700; color: #34D399; margin-bottom: 0.6rem;">🏡 Property B</div>
        """, unsafe_allow_html=True)
        
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
                
        st.markdown("<hr style='border-color: #1F2937; margin: 0.6rem 0;'>", unsafe_allow_html=True)
        
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
        
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------ PREDICTION CALCULATION ------------------
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
    
    # ------------------ COMPARISON RESULTS BANNER ------------------
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 1.15rem; font-weight: 800; color: #F9FAFB; margin-bottom: 0.6rem;'>📊 Side-by-Side Valuation Comparison Results</div>", unsafe_allow_html=True)
    
    res_c1, res_c2 = st.columns(2)
    with res_c1:
        st.markdown(f"""
        <div class="dark-card" style="border: 1px solid #3B82F6;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">🏠 Property A Estimated Value</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #60A5FA;">£{pred_A:,.2f}</div>
            <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 0.3rem;">Unit Price: £{pred_A / values_A['GrLivArea']:,.2f} / sq ft</div>
        </div>
        """, unsafe_allow_html=True)
        
    with res_c2:
        st.markdown(f"""
        <div class="dark-card" style="border: 1px solid #10B981;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">🏡 Property B Estimated Value</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #34D399;">£{pred_B:,.2f}</div>
            <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 0.3rem;">Unit Price: £{pred_B / values_B['GrLivArea']:,.2f} / sq ft</div>
        </div>
        """, unsafe_allow_html=True)

    # Difference Summary Box
    if diff > 0:
        diff_text = f"💡 <b>Property B</b> is valued at <b style='color: #34D399;'>+£{diff:,.2f} (+{pct_diff:.1f}%) higher</b> than Property A."
        diff_border = "#10B981"
    elif diff < 0:
        diff_text = f"💡 <b>Property A</b> is valued at <b style='color: #60A5FA;'>+£{abs(diff):,.2f} (+{abs(pct_diff):.1f}%) higher</b> than Property B."
        diff_border = "#3B82F6"
    else:
        diff_text = "💡 Both properties have equal predicted valuation."
        diff_border = "#94A3B8"
        
    st.markdown(f"""
    <div style="background: rgba(17, 24, 39, 0.8); border: 1px solid {diff_border}; padding: 0.95rem 1.25rem; border-radius: 12px; font-size: 0.95rem; color: #F9FAFB; margin-bottom: 1rem;">
        {diff_text}
    </div>
    """, unsafe_allow_html=True)

    # ------------------ FEATURE MATRIX TABLE ------------------
    table_header = '<div class="dark-card" style="padding: 1.25rem;"><div style="font-size: 1.05rem; font-weight: 700; color: #F9FAFB; margin-bottom: 1rem;">📋 Feature Breakdown Comparison Matrix</div><table style="width: 100%; border-collapse: collapse; font-size: 0.92rem;"><thead><tr style="border-bottom: 2px solid #374151; color: #94A3B8; text-align: left;"><th style="padding: 0.75rem 1rem; width: 35%;">Feature</th><th style="padding: 0.75rem 1rem; width: 25%; color: #60A5FA;">Property A</th><th style="padding: 0.75rem 1rem; width: 25%; color: #34D399;">Property B</th><th style="padding: 0.75rem 1rem; width: 15%; text-align: right;">Comparison</th></tr></thead><tbody>'
    
    matrix_features = [
        ("⭐ Overall Quality", val_A_qual, val_B_qual, "/ 10"),
        ("📐 Living Area", f"{val_A_area:,}", f"{val_B_area:,}", "sq ft"),
        ("🏠 Year Built", val_A_built, val_B_built, ""),
        ("🛏️ Bedrooms", val_A_bed, val_B_bed, "Bedrooms"),
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
            comp_badge = "<span style='color: #60A5FA; font-weight: 700;'>A is higher</span>"
        elif numB > numA:
            comp_badge = "<span style='color: #34D399; font-weight: 700;'>B is higher</span>"
        else:
            comp_badge = "<span style='color: #94A3B8;'>Equal</span>"
            
        rows_html += f"<tr style='border-bottom: 1px solid #1F2937;'><td style='padding: 0.75rem 1rem; color: #F9FAFB; font-weight: 600;'>{label}</td><td style='padding: 0.75rem 1rem; color: #94A3B8;'>{valA} {unit}</td><td style='padding: 0.75rem 1rem; color: #94A3B8;'>{valB} {unit}</td><td style='padding: 0.75rem 1rem; text-align: right;'>{comp_badge}</td></tr>"
        
    full_table_html = table_header + rows_html + "</tbody></table></div>"
    st.markdown(full_table_html, unsafe_allow_html=True)

# streamlit run app.py