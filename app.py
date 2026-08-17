import streamlit as st
import joblib
import pandas as pd
import time

# --- 1. Page Configuration ---
st.set_page_config(page_title="AutoPrice Pro", page_icon="🏎️", layout="centered")


# --- 2. Load Pipeline ---
@st.cache_resource
def load_model():
    return joblib.load("full_car_pipeline.pkl")


pipeline = load_model()

# --- 3. CSS for Top-Down Rain Animation ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1f4068 0%, #162447 50%, #1b1b2f 100%); color: #ffffff; }
    .block-container { 
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(12px); 
        border-radius: 20px; padding: 3rem; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); 
    }

    @keyframes rain {
        0% { transform: translateY(-100px); }
        100% { transform: translateY(600px); }
    }
    .car-icon { position: fixed; font-size: 2.5rem; animation: rain 2s linear forwards; }
    </style>
""", unsafe_allow_html=True)

# --- 4. UI Layout ---
st.markdown('<h1 style="text-align: center; color: #e43f5a;">🏎️ AutoPrice Pro</h1>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    brand = st.selectbox("Brand", ["Toyota", "Ford", "BMW", "Mercedes-Benz", "Chevrolet", "Honda"])
    model_year = st.number_input("Year", 1990, 2026, 2020)
    milage = st.number_input("Mileage", 0, 500000, 50000)
with col2:
    transmission = st.selectbox("Transmission", ["Automatic", "Manual"])
    fuel_type = st.selectbox("Fuel Type", ["Gasoline", "Hybrid", "Diesel", "E85 Flex Fuel"])
    accident = st.selectbox("Accident", ["None reported", "At least one accident reported"])

# --- 5. Prediction & Animation ---
if st.button("🚀 Predict Price", use_container_width=True, type="primary"):
    with st.spinner('Analyzing...'):
        # حساب الميزات
        car_age = max(1, 2026 - model_year)
        milage_per_year = milage / car_age

        input_data = pd.DataFrame({
            'model_year': [model_year], 'milage': [milage], 'car_age': [car_age],
            'milage_per_year': [milage_per_year], 'brand': [brand], 'model': ["Other"],
            'fuel_type': [fuel_type], 'engine': ["Other"], 'transmission': [transmission],
            'ext_col': ["Other"], 'int_col': ["Other"], 'accident': [accident], 'clean_title': ["Yes"]
        })

        prediction = pipeline.predict(input_data)[0]

    # عرض العربيات (Top-down view)
    st.markdown(f"""
        <div class="car-icon" style="top: 0; left: 10%;">🏎️</div>
        <div class="car-icon" style="top: -50px; left: 30%;">🚙</div>
        <div class="car-icon" style="top: -20px; left: 50%;">🚗</div>
        <div class="car-icon" style="top: -80px; left: 70%;">🏎️</div>
        <div class="car-icon" style="top: -30px; left: 90%;">🚙</div>
    """, unsafe_allow_html=True)

    st.success("✅ Analysis Complete!")
    st.markdown(f"<h1 style='text-align: center; color: #ff6584;'>${prediction:,.2f}</h1>", unsafe_allow_html=True)