# 🏥 Sistem Chirurgie Pediatrică – Proiect Colectiv

Acest proiect reprezintă o aplicație informatică destinată colectării, gestionării și analizei datelor medicale primare în contextul urgențelor chirurgicale pediatrice.

## 🎯 Scopul proiectului

- Colectarea datelor clinice (HR, SpO₂, temperatură)
- Alertare automată la depășirea pragurilor critice
- Acces diferențiat pe roluri (medic, asistent, cercetător)
- Exportul datelor pentru analiză statistică în R și JASP
- Logarea acțiunilor în blockchain

## ⚙️ Tehnologii utilizate

- **Backend**: FastAPI + Pandas
- **Frontend**: Streamlit + Plotly
- **Autentificare**: JWT + bcrypt
- **Analiză externă**: R + jsonlite
- **Stocare**: DB SQLite, CSV local
- **Blockchain**: Web3.py

## Persistența datelor 

Aplicația utilizează un sistem mixt de stocare a datelor medicale: 
# Bază de date locală SQLite (data/vitals.db):

-Conține toate înregistrările trimise prin API sau generate automat

-Este utilizată pentru interogări rapide și stocare permanentă

-Se accesează intern cu SQLAlchemy

# Fișier CSV sincronizat (data/vitals_sample.csv):

-Se actualizează automat la fiecare inserare

-Este folosit de dashboard-ul Streamlit pentru afișare

-Poate fi exportat și analizat în JASP sau Excel

## 🚀 Cum rulezi proiectul

## 1. Clonează repo:
```plaintext

git clone https://github.com/USERNAME/proiect-chirurgie-pediatrica.git
cd proiect-chirurgie-pediatrica
```

## 2. Activează mediul virtual:
```plaintext

python -m venv venv
venv\Scripts\activate
```

## 3. Instalează dependințele:
```plaintext

pip install -r requirements.txt
```

## 4. Rulează serverul FastAPI:
```plaintext

uvicorn app.main:app --reload
```

## 5. Accesează documentația API:
```plaintext

http://localhost:8000/docs
```

## 6. Rulează dashboardul:
```plaintext
python streamlit run dashboard/ui_dashboard.py
```
# Autentificare
```plaintext

medic / 1234 → acces complet

asistent / 4321 → vizualizare

Token JWT se generează la /token și se folosește pentru autorizare
```

# Export + analiză în R

```plaintext
Apelează:

GET /export/json

```
În analiza.R:
```plaintext

library(jsonlite)
df <- stream_in(file("data/export_r.json"))
```

## 📁 Structura proiectului

```plaintext

proiect_chirurgie_pediatrica/
├── app/
│   ├── main.py
│   └── auth.py
├── dashboard/
│   └── ui_dashboard.py
├── data/
│   ├── vitals_sample.csv
│   └── export_r.json
├── r-analysis/
│   └── analiza.R
├── README.md
```


