import streamlit as st
import pickle
import numpy as np
import plotly.express as px
import os
import requests


def ensure_file(path: str, secret_key: str | None = None) -> bool:
    """Ensure `path` exists locally; if not and a URL secret is provided,
    download it. Returns True if the file is available locally.
    """
    if os.path.exists(path):
        return True
    if secret_key is None:
        return False
    try:
        url = st.secrets.get(secret_key)
    except Exception:
        url = None
    if not url:
        return False
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        with open(path, "wb") as f:
            f.write(resp.content)
        return True
    except Exception:
        return False


# Ensure model files exist (optionally set MODEL_URL and ENCODERS_URL in Streamlit secrets)
if not ensure_file("Health_risk_predictor.pkl", "MODEL_URL"):
    st.error(
        "Model file `Health_risk_predictor.pkl` not found.\n"
        "Add the file to your repo or set `MODEL_URL` in Streamlit secrets to a direct download URL."
    )
    st.stop()

if not ensure_file("label_encoders.pkl", "ENCODERS_URL"):
    st.error(
        "Encoders file `label_encoders.pkl` not found.\n"
        "Add the file to your repo or set `ENCODERS_URL` in Streamlit secrets to a direct download URL."
    )
    st.stop()

model = pickle.load(open("Health_risk_predictor.pkl", 'rb'))


encoders = pickle.load(open("label_encoders.pkl", "rb"))

st.title("Healt Risk Predictor")

age=st.slider("Age",18,80,22)
diet=st.selectbox("Diet Quality", ['Poor', 'Average', 'Good'])
exercise=st.slider("Exersice Day per week",0,7,3)
sleep=st.slider("Sleep Hours",3,12,6)
stress=st.selectbox("Stress level",['Low', 'Medium', 'High'])
bmi=st.number_input("BMI",10.0,40.0,22.0)
smoking=st.selectbox("Smoking", ["Yes", "No"])
alcohol=st.selectbox("Alcohol consumption",['Low', 'Medium', 'High'])
family_history=st.selectbox("Family History of Disease",["Yes", "No"])


if st.button("Predict Risk"):
    input_data=[
                age,
                encoders['diet'].transform([diet])[0],
                exercise,
                sleep,
                encoders['stress'].transform([stress])[0],
                bmi,
                encoders['smoking'].transform([smoking])[0],
                encoders['alcohol'].transform([alcohol])[0],
                encoders['family_history'].transform([family_history])[0],
                ]
    
    prediction=model.predict([input_data])
    probs=model.predict([input_data])

    risk_label= encoders['risk_level'].inverse_transform([prediction[0]])[0]

    st.success(risk_label)

    # Map categorical factors to human-friendly numeric scores for charting
    diet_score_map = {"Poor": 1, "Average": 2, "Good": 3}
    stress_score_map = {"Low": 1, "Medium": 2, "High": 3}

    factors = {
        "Diet": diet_score_map.get(diet, encoders['diet'].transform([diet])[0]),
        "Excercise": exercise,
        "Sleep": sleep,
        "Stress": stress_score_map.get(stress, encoders['stress'].transform([stress])[0]),
        "BMI": bmi,
    }

    bar_fig=px.bar(
        x=list(factors.keys()),

        y=list(factors.values()),

        labels={"x":"Factors","y":"value"},

        title="Your Lifestyle Factors"
    )

    st.plotly_chart(bar_fig)