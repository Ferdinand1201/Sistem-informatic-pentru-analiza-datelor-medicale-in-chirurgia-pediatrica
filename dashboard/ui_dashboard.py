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

    if "pews" not in data.columns:
        data["pews"] = None

    if "risk_level" not in data.columns:
        data["risk_level"] = "N/A"

    data = data.sort_values(by=["timestamp", "patient_id"])

except FileNotFoundError:
    st.warning("⚠️ Fișierul de date nu a fost găsit.")
    st.stop()

# Afișează tabelul complet
st.subheader("📋 Tabel date vitale înregistrate")

def style_alert(val, column):
    if column == "heart_rate":
        if val > 180:
            return "background-color: #ff4d4d; color: white"
        elif val > 160:
            return "background-color: #ffe066; color:black"

    elif column == "spo2":
        if val < 90:
            return "background-color: #ff4d4d; color: white"
        elif val < 94:
            return "background-color: #ffe066; color:black"

    elif column == "temperature":
        if val > 38:
            return "background-color: #ffe066; color:black"
        elif val > 39.5:
            return "background-color: #ff4d4d; color: white"


    elif column == "pews" and pd.notna(val):
        if val >= 4:
            return "background-color: #ff4d4d; color: white"
        elif val >= 2:
            return "background-color: #ffe066; color:black"

    elif column == "risk_level":
        if val == "Ridicat":
            return "background-color: #ff4d4d; color: white"
        elif val == "Mediu":
            return "background-color: #ffe066; color:black"
        elif val == "Scăzut":
            return ""

    return ""

styled_data = data.style \
    .map(lambda val: style_alert(val, "heart_rate"), subset=["heart_rate"]) \
    .map(lambda val: style_alert(val, "spo2"), subset=["spo2"]) \
    .map(lambda val: style_alert(val, "temperature"), subset=["temperature"]) \
    .map(lambda val: style_alert(val, "pews"), subset=["pews"]) \
    .map(lambda val: style_alert(val, "risk_level"), subset=["risk_level"])

st.dataframe(styled_data, use_container_width=True)

# Detectează alerte clasice
alerts = data[
    (data["risk_level"] == "Ridicat")
]

if not alerts.empty:
    alerts = alerts.sort_values(by=["timestamp", "patient_id"])
    st.error(f"⚠ {len(alerts)} ALERTE VITALE DETECTATE!")

    st.subheader("Tabel alerte detectate")

    def highlight_alert(val, column):
        return style_alert(val, column) if column != "risk_level" else ""

    alert_style = alerts.style \
        .map(lambda val: highlight_alert(val, "heart_rate"), subset=["heart_rate"]) \
        .map(lambda val: highlight_alert(val, "spo2"), subset=["spo2"]) \
        .map(lambda val: highlight_alert(val, "temperature"), subset=["temperature"]) \
        .map(lambda val: highlight_alert(val, "pews"), subset=["pews"])

    st.dataframe(alert_style, use_container_width=True)

else:
    st.info("🟢 Niciun pacient nu este marcat cu risc crescut conform PEWS.")

# Linie de separare
st.markdown("---")

# Grafic Heart Rate
fig_hr = px.line(data, x="timestamp", y="heart_rate", color="patient_id", title="📊 Evoluție Heart Rate")
st.plotly_chart(fig_hr, use_container_width=True)

# Grafic Temperatură
if data["temperature"].notna().any():
    fig_temp = px.line(data, x="timestamp", y="temperature", color="patient_id", title="🌡️ Evoluție Temperatură")
    st.plotly_chart(fig_temp, use_container_width=True)

# Grafic SpO2
if data["spo2"].notna().any():
    fig_spo2 = px.line(data, x="timestamp", y="spo2", color="patient_id", title="🫁 Evoluție SpO₂")
    st.plotly_chart(fig_spo2, use_container_width=True)

# Histogramă scor PEWS
if "pews" in data.columns and data["pews"].notna().any():
    fig_pews = px.histogram(data, x="pews", nbins=6, title="📊 Distribuție scor PEWS", text_auto=True)
    st.plotly_chart(fig_pews, use_container_width=True)

# Histogramă nivel de risc simbolic
if "risk_level" in data.columns:
    fig_risk_level = px.histogram(data, x="risk_level", color="risk_level", title="📊 Distribuție nivel de risc (PEWS)", text_auto=True)
    st.plotly_chart(fig_risk_level, use_container_width=True)
