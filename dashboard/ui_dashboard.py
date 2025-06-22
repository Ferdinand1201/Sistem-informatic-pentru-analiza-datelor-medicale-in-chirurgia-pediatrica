import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Monitorizare Vitală", layout="wide")
st.title("📈 Monitorizare Chirurgie Pediatrică")

# Încarcă datele
try:
    csv_path = os.path.abspath("data/vitals_sample.csv")
    data = pd.read_csv(csv_path)

    # Conversii sigure
    data["heart_rate"] = pd.to_numeric(data["heart_rate"], errors="coerce")
    data["spo2"] = pd.to_numeric(data["spo2"], errors="coerce")
    data["temperature"] = pd.to_numeric(data["temperature"], errors="coerce")
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")

    # Sortează după timp (pentru grafic corect)
    data = data.sort_values("timestamp")

except FileNotFoundError:
    st.warning("⚠️ Fișierul de date nu a fost găsit.")
    st.stop()

# DEBUG: afișare tabel complet
st.dataframe(data)

# Detectează alerte
alerts = data[
    (data["heart_rate"] > 180) |
    (data["spo2"] < 90) |
    (data["temperature"] > 38.5)
]

# Afișează alertele
if not alerts.empty:
    st.error(f"⚠ {len(alerts)} ALERTĂ/ALERTE DETECTATE!")
    st.dataframe(alerts, use_container_width=True)
else:
    st.success("✅ Nu au fost detectate anomalii în datele vitale.")

# Linie de separare
st.markdown("---")

# Grafic Heart Rate
fig_hr = px.line(data, x="timestamp", y="heart_rate", color="patient_id", title="Evoluție Heart Rate")
st.plotly_chart(fig_hr, use_container_width=True)

# Grafic Temperatură
if "temperature" in data.columns and data["temperature"].notna().any():
    fig_temp = px.line(data, x="timestamp", y="temperature", color="patient_id", title="Evoluție Temperatură")
    st.plotly_chart(fig_temp, use_container_width=True)

# Grafic SpO2
if "spo2" in data.columns and data["spo2"].notna().any():
    fig_spo2 = px.line(data, x="timestamp", y="spo2", color="patient_id", title="Evoluție SpO₂")
    st.plotly_chart(fig_spo2, use_container_width=True)
