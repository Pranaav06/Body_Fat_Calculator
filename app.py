import streamlit as st
import numpy as np
import joblib

from body_fat_calculator import body_fat_7_site, body_fat_12_site

# -----------------------------
# LOAD MODEL & ENCODER
# -----------------------------
model = joblib.load("body_fat_model.pkl")
gender_encoder = joblib.load("gender_encoder.pkl")

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(
    page_title="Body Fat Percentage Calculator",
    page_icon="💪",
    layout="centered"
)

st.title("💪 Body Fat Percentage Calculator")
st.write("7-Site / 12-Site Skinfold Method")

st.divider()

# -----------------------------
# INPUTS
# -----------------------------
age = st.number_input(
    "Age (years)",
    min_value=10,
    max_value=80,
    value=20
)

gender = st.radio(
    "Gender",
    ["Male", "Female"]   # ✅ Capitalized
)

method = st.radio(
    "Measurement Method",
    [7, 12],
    format_func=lambda x: f"{x}-Site Method"
)

sum_skinfold_mm = st.number_input(
    "Sum of Skinfolds (mm)",
    min_value=10.0,
    max_value=300.0,
    value=198.0
)

st.divider()

# -----------------------------
# SAFE ML RANGES
# -----------------------------
SAFE_RANGE_7 = (60, 160)
SAFE_RANGE_12 = (40, 120)

# -----------------------------
# PREDICTION
# -----------------------------
if st.button("Predict Body Fat %"):

    gender_lower = gender.lower()

    use_formula = False

    if method == 7:
        if not (SAFE_RANGE_7[0] <= sum_skinfold_mm <= SAFE_RANGE_7[1]):
            use_formula = True
    else:
        if not (SAFE_RANGE_12[0] <= sum_skinfold_mm <= SAFE_RANGE_12[1]):
            use_formula = True

    # ---- Formula fallback (CORRECT SCIENCE)
    if use_formula:
        if method == 7:
            prediction = body_fat_7_site(sum_skinfold_mm, age, gender_lower)
        else:
            prediction = body_fat_12_site(sum_skinfold_mm, age, gender_lower)
    else:
        gender_encoded = gender_encoder.transform([gender_lower])[0]
        X = np.array([[sum_skinfold_mm, age, gender_encoded, method]])
        prediction = model.predict(X)[0]

    st.success(f"Estimated Body Fat Percentage: **{prediction:.2f}%**")

# -----------------------------
# FOOTER
# -----------------------------
st.caption("Built with Python • Scikit-learn • Streamlit")
