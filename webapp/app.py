import streamlit as st
import pandas as pd

model = pd.read_pickle("models/battery_model.pkl")

st.title("Battery Life Prediction App")
st.markdown("Enter your phone's parameters to estimate remaining battery life:")

start_pct = st.slider("Start Battery Percentage (%)", 0, 100, 100)
health_pct = st.slider("Battery Health (%)", 0, 100, 100)
capacity = st.number_input("Battery Capacity (mAh)", min_value=100, value=3000)
brightness = st.slider("Screen Brightness (%)", 0, 100, 50)
app_count = st.number_input("Number of Active Apps", min_value=0, value=0, step=1)

if st.button("Estimate Battery Life"):

    input_features = [[start_pct, health_pct, capacity, brightness, app_count, 0]]

    predicted_seconds = model.predict(input_features)

    remaining_sec = round(float(predicted_seconds[0]) * 3600)

    hours = remaining_sec // 3600
    minutes = (remaining_sec % 3600) // 60
    st.write(f"**Estimated Remaining Battery Life:** {hours}h {minutes}m ({remaining_sec} seconds)")

# streamlit run webapp/app.py