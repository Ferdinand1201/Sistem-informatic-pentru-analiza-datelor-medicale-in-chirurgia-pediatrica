# app/ml_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

MODEL_PATH = "app/risk_model.pkl"

def train_model(force=False):
    if not force and os.path.exists(MODEL_PATH):
        print(" Modelul deja există. Nu se reantrenează.")
        return

    data = pd.read_csv("data/vitals_sample.csv")
    data["risk"] = ((data["heart_rate"] > 180) |
                    (data["spo2"] < 90) |
                    (data["temperature"] > 38.5)).astype(int)

    X = data[["heart_rate", "spo2", "temperature"]]
    y = data["risk"]

    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    print(" Model AI antrenat și salvat.")


def predict_risk(heart_rate, spo2, temperature):
    if not os.path.exists(MODEL_PATH):
        train_model()

    model = joblib.load(MODEL_PATH)
    X = pd.DataFrame([[heart_rate, spo2, temperature]],
                     columns=["heart_rate", "spo2", "temperature"])
    return int(model.predict(X)[0])
