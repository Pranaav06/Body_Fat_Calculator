import streamlit as st
from bodyfat import calculate_body_fat

st.set_page_config(
    page_title="Body Fat Percentage Calculator",
    page_icon="💪",
    layout="centered"
)

st.title("💪 Body Fat Percentage Calculator")
st.write("Professional skinfold-based calculation")

st.divider()

age = st.number_input("Age (years)", 10, 80, 19)
gender = st.radio("Gender", ["Male", "Female"])
athlete = st.radio("Are you an athlete?", ["Yes", "No"])
method = st.radio("Measurement Method", ["7-site", "12-site"])
sum_mm = st.number_input("Sum of Skinfolds (mm)", 10.0, 300.0, 198.0)

st.divider()

if st.button("Calculate Body Fat %"):
    try:
        result = calculate_body_fat(
            method=method,
            sum_mm=sum_mm,
            age=age,
            gender=gender.lower(),
            athlete=(athlete == "Yes")
        )
        st.success(f"Estimated Body Fat Percentage: **{result:.2f}%**")
    except ValueError as e:
        st.error(str(e))

st.caption("Based on validated sports science equations")
