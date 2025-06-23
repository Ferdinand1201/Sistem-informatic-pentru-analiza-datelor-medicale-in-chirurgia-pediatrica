import pandas as pd
import random
from datetime import datetime, timedelta
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))
from ml_model import train_model


output_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "vitals_sample.csv")
)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

def compute_pews(hr, spo2, temp):
    score = 0
    if hr > 180:
        score += 2
    elif hr > 160:
        score += 1

    if spo2 < 90:
        score += 2
    elif spo2 < 94:
        score += 1

    if temp > 39.5:
        score += 2
    elif temp > 38:
        score += 1

    return score

n_pacienti = 10
masuratori_per_pacient = 6
start_time = datetime(2025, 6, 23, 10, 0)

rows = []
for i in range(n_pacienti):
    patient_id = f"P{str(i+1).zfill(3)}"
    timestamp = start_time
    for _ in range(masuratori_per_pacient):
        hr = random.randint(130, 200)
        spo2 = round(random.uniform(85.0, 100.0), 1)
        temp = round(random.uniform(36.0, 40.0), 1)
        pews = compute_pews(hr, spo2, temp)

        if pews >= 4:
            risk_level = "Ridicat"
        elif pews >= 2:
            risk_level = "Mediu"
        else:
            risk_level = "Scăzut"

        rows.append([
            patient_id, hr, spo2, temp,
            timestamp.strftime("%Y-%m-%d %H:%M"),
            pews, risk_level
        ])
        timestamp += timedelta(minutes=10)

df = pd.DataFrame(rows, columns=[
    "patient_id", "heart_rate", "spo2", "temperature", "timestamp", "pews", "risk_level"
])
df["timestamp"] = pd.to_datetime(df["timestamp"])

df["patient_num"] = df["patient_id"].str.extract(r'(\d+)').astype(int)
df = df.sort_values(by=["timestamp", "patient_num"])
df = df.drop(columns=["patient_num"])

df.to_csv(output_path, index=False)
print("✅ Fișierul 'vitals_sample.csv' a fost generat cu succes.")

# === Antrenare model ===
train_model(force=True)
print("✅ Modelul AI a fost antrenat și salvat.")
