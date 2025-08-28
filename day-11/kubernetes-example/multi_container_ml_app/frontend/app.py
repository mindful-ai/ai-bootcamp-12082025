import os
import streamlit as st
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:5002/predict")

st.set_page_config(page_title="ML Prediction App", page_icon="🤖")
st.title("Machine Learning Prediction App")

features = st.text_input("Enter features (comma-separated)", "")

if st.button("Predict"):
    try:
        if not features.strip():
            st.warning("Please enter some numbers.")
        else:
            features_list = [float(x.strip()) for x in features.split(",") if x.strip() != ""]
            resp = requests.post(BACKEND_URL, json={"features": features_list}, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            prediction = data.get("prediction")
            st.success(f"Prediction: {prediction}")
    except Exception as e:
        st.error(f"Error: {e}")
