# 🏥 Sistem Chirurgie Pediatrică – Proiect Colectiv

Acest proiect reprezintă o aplicație informatică destinată colectării, gestionării și analizei datelor medicale primare în contextul urgențelor chirurgicale pediatrice.

## 🎯 Scopul proiectului

- Colectarea automată/manuală a datelor clinice (HR, SpO₂, temperatură)
- Alertare automată la depășirea pragurilor critice
- Acces diferențiat pe roluri (medic, asistent, cercetător)
- Exportul datelor pentru analiză statistică în R
- (Opțional) Logarea acțiunilor în blockchain

## ⚙️ Tehnologii utilizate

- **Backend**: FastAPI + Pandas
- **Frontend**: Streamlit + Plotly
- **Autentificare**: JWT + bcrypt
- **Analiză externă**: R + jsonlite
- **Stocare**: CSV local
- *(Opțional: Solidity, Ganache, Web3.py)*

## 🚀 Cum rulezi proiectul

1. Clonează repo:
```bash
git clone https://github.com/USERNAME/proiect-chirurgie-pediatrica.git
cd proiect-chirurgie-pediatrica

Activează mediul virtual:

python -m venv venv
venv\Scripts\activate
Instalează dependințele:


pip install -r requirements.txt
Rulează serverul FastAPI:

uvicorn app.main:app --reload
Accesează documentația API:

http://localhost:8000/docs
Rulează dashboardul:

streamlit run dashboard/ui_dashboard.py

🔐 Autentificare
medic / 1234 → acces complet

asistent / 4321 → vizualizare

Token JWT se generează la /token și se folosește pentru autorizare

📤 Export + analiză în R
Apelează:

pgsql
Copiază
Editează
GET /export/json
În analiza.R:

r
Copiază
Editează
library(jsonlite)
df <- stream_in(file("data/export_r.json"))
📁 Structura proiectului
css
Copiază
Editează
proiect_chirurgie_pediatrica/
├── app/
│   ├── main.py
│   └── auth.py
├── dashboard/
│   └── ui_dashboard.py
├── data/
│   └── vitals_sample.csv
├── r-analysis/
│   └── analiza.R
├── README.md
👨‍💻 Autori
Nume 1 – @username

Nume 2 – ...