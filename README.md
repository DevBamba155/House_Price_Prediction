# 🏠 House Price Prediction Web Application

An interactive, AI-powered Machine Learning Web Application built with **Streamlit**, **scikit-learn**, and **Pandas** to estimate house sales prices based on property features, quality parameters, square footage, and amenities.

---

## 🌟 Key Features

- **Interactive Feature Inputs**: Select overall property quality, total living area, lot size, garage specs, basement dimensions, and room counts.
- **Machine Learning Powered**: Uses an trained **Random Forest Regressor** model to accurately predict house prices.
- **Live Visualizations & Analysis**: Explore feature impacts, price distributions, and dataset statistics.
- **Modern UI**: Tailored Streamlit layout with custom styling and intuitive control panels.

---

## 📁 Repository Structure

```
House_Price_Prediction/
│
├── app.py                      # Main Streamlit web application interface
├── requirements.txt            # Python dependencies for production & deployment
├── README.md                   # Project documentation
│
├── models/
│   ├── house_price_model.pkl   # Trained Machine Learning model
│   └── model_columns.pkl       # Serialized feature column order
│
├── src/
│   └── preprocessing.py        # Data cleaning, feature engineering, and model training script
│
└── data/
    ├── train.csv               # Ames Housing training dataset
    ├── test.csv                # Ames Housing testing dataset
    └── submission.csv          # Sample predictions file
```

---

## 🚀 Local Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/DevBamba155/House_Price_Prediction.git
cd House_Price_Prediction
```

### 2. Create and Activate Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```

The app will open automatically in your local browser at `http://localhost:8501`.

---

## 🌐 Cloud Deployment

This app is ready to deploy on **Streamlit Community Cloud**, **Render**, or **Hugging Face Spaces**:

1. Fork or push this repository to your GitHub account (`DevBamba155/House_Price_Prediction`).
2. Log into [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app**, select `House_Price_Prediction` repository, set Main file path to `app.py`, and click **Deploy**!

---

## 📊 Dataset & Model Info

- **Dataset**: Ames Housing Dataset (80+ property attributes)
- **Primary Model**: Random Forest Regressor
- **Metrics Evaluation**: Evaluated using Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and $R^2$ Score.
