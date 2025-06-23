import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.ml_model import predict_risk
from utils.web3_utils import log_event

st.set_page_config(page_title="Monitorizare Vitală", layout="wide")
st.title(" Monitorizare Chirurgie Pediatrică")

# Încarcă datele
try:
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "vitals_sample.csv"))
    data = pd.read_csv(csv_path)
except FileNotFoundError:
    st.warning(" Fișierul de date nu a fost găsit.")
    st.stop()
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

data["risc_ai"] = data.apply(
    lambda row: predict_risk(row["heart_rate"], row["spo2"], row["temperature"]),
        axis=1
)

def play_alert_sound():

    st.markdown("""
        <audio autoplay>
            <source src="alert-109578.mp3" type="audio/mpeg">
        </audio>
    """, unsafe_allow_html=True)

    # Backup silențios dacă autoplay e blocat
    with st.expander("🔊 Dacă nu se aude automat, poți reda manual:"):
        st.audio("alert-109578.mp3", format="audio/mp3")


# Afișează tabelul complet
st.subheader(" Tabel date vitale înregistrate")

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
            return "background-color: #ffe066; color: black"
        elif val == "Scăzut":
            return ""
    elif column == "risc_ai":
            return "background-color: #ffcccc; color: black"

    return ""

styled_data = data.style \
    .map(lambda val: style_alert(val, "heart_rate"), subset=["heart_rate"]) \
    .map(lambda val: style_alert(val, "spo2"), subset=["spo2"]) \
    .map(lambda val: style_alert(val, "temperature"), subset=["temperature"]) \
    .map(lambda val: style_alert(val, "pews"), subset=["pews"]) \
    .map(lambda val: style_alert(val, "risk_level"), subset=["risk_level"]) \
    .map(lambda val: style_alert(val, "risc_ai"), subset=["risc_ai"])
st.dataframe(styled_data, use_container_width=True)

# Detectează alerte clasice
alerts = data[
    (data["risk_level"] == "Ridicat")
]

if not alerts.empty:
    alerts = alerts.sort_values(by=["timestamp", "patient_id"])
    st.error(f" {len(alerts)} ALERTE VITALE DETECTATE!")
    for idx, row in alerts.iterrows():
        st.write(f"{row['patient_id']} – HR: {row['heart_rate']}, SpO₂: {row['spo2']}, Temp: {row['temperature']}")
        log_event(row["patient_id"], "ALERT_TRIGGERED")  # 👈 logare în "blockchain"
    play_alert_sound()

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
    st.info(" Niciun pacient nu este marcat cu risc crescut conform PEWS.")


risc_ai_alerts = data[data["risc_ai"] == 1]

if not risc_ai_alerts.empty:
    st.warning(f"{len(risc_ai_alerts)} pacienți detectați cu risc de AI")
    st.subheader("Tabel pacienți detectați cu risc AI")
    st.dataframe(risc_ai_alerts[["patient_id", "heart_rate", "spo2", "temperature", "timestamp", "risc_ai"]])
else:
    st.success("AI nu a detectat pacienți cu risc ridicat.")


# Linie de separare
st.markdown("---")

# Grafic Heart Rate
fig_hr = px.line(data, x="timestamp", y="heart_rate", color="patient_id", title=" Evoluție Heart Rate")
st.plotly_chart(fig_hr, use_container_width=True)

# Grafic Temperatură
if data["temperature"].notna().any():
    fig_temp = px.line(data, x="timestamp", y="temperature", color="patient_id", title="Evoluție Temperatură")
    st.plotly_chart(fig_temp, use_container_width=True)

# Grafic SpO2
if data["spo2"].notna().any():
    fig_spo2 = px.line(data, x="timestamp", y="spo2", color="patient_id", title="Evoluție SpO₂")
    st.plotly_chart(fig_spo2, use_container_width=True)

# Histogramă scor PEWS
if "pews" in data.columns and data["pews"].notna().any():
    fig_pews = px.histogram(data, x="pews", nbins=6, title=" Distribuție scor PEWS(Pediatric Early Warning Score)", text_auto=True)
    st.plotly_chart(fig_pews, use_container_width=True)

# Histogramă nivel de risc simbolic
if "risk_level" in data.columns:
    fig_risk_level = px.histogram(data, x="risk_level", color="risk_level", title=" Distribuție nivel de risc (PEWS)", text_auto=True)
    st.plotly_chart(fig_risk_level, use_container_width=True)

#  Export JSON complet pentru analiză în R
if st.button(" Exportă toate datele în JSON pentru R"):
    export_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "export_r.json"))
    data.to_json(export_path, orient="records", lines=True)
    st.success(" Fișierul complet a fost exportat în 'data/export_r.json'")

if st.button(" Exportă datele în CSV pentru JASP"):
    export_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "export_jasp.csv"))
    data.to_csv(export_csv_path, index=False)
    st.success(" Fișierul CSV a fost exportat în 'data/export_jasp.csv'")
