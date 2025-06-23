from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
import pandas as pd
import os
from fastapi import FastAPI
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from app.auth import create_access_token, fake_users_db, role_required
from app.ml_model import predict_risk
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", scheme_name="JWT")

app = FastAPI()

# Setare manuală de OpenAPI (opțional, dar util)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Sistem Chirurgie Pediatrică",
        version="1.0.0",
        description="API pentru colectarea și protejarea datelor medicale",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Asigurăm că folderul data/ există
os.makedirs("data", exist_ok=True)

# Dacă există deja fișierul CSV, îl încărcăm în memorie
csv_path = "data/vitals_sample.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame()


# Schema pentru datele vitale
class VitalData(BaseModel):
    patient_id: str
    heart_rate: int
    spo2: float
    temperature: float
    timestamp: str

def compute_pews(hr: int, spo2: float, temp: float) -> int:
    score = 0

    # Heart Rate
    if hr > 180:
        score += 2
    elif hr > 160:
        score += 1

    # SpO2
    if spo2 < 90:
        score += 2
    elif spo2 < 94:
        score += 1

    # Temperatură
    if temp > 38.5:
        score += 1

    return score
@app.post("/submit")
def submit_vitals(data: VitalData):
    global df
    entry = data.dict()

    # Adăugăm predicția de risc AI
    risk_score = predict_risk(entry["heart_rate"], entry["spo2"], entry["temperature"])
    entry["risk"] = risk_score

    # Adăugăm scorul PEWS
    pews_score = compute_pews(entry["heart_rate"], entry["spo2"], entry["temperature"])
    entry["pews"] = pews_score

    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)

    return {
        "message": "Date înregistrate.",
        "risk": "RIDICAT" if risk_score else "SCĂZUT",
        "pews_score": pews_score
    }


# Endpoint pentru login
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/token")
def login(username: str = Form(...), password: str = Form(...)):
    user = fake_users_db.get(username)
    if not user or not pwd_context.verify(password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(data={"sub": username, "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}
# Endpoint protejat cu roluri
@app.get("/vitals-secured")
def view_last_vitals(user=Depends(role_required(["doctor", "nurse"]))):
    return df.tail(5).to_dict()

@app.get("/export/json")
def export_json(user=Depends(role_required(["doctor", "nurse", "researcher"]))):
    try:
        df.to_json("data/export_r.json", orient="records", lines=True)
        return {"message": "Export JSON pentru R salvat în data/export_r.json"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eroare export: {str(e)}")

@app.get("/export/csv")
def export_csv(user=Depends(role_required(["doctor", "nurse", "researcher"]))):
    try:
        df.to_csv("data/export_jasp.csv", index=False)
        return {"message": "Export CSV pentru JASP salvat în data/export_jasp.csv"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eroare export: {str(e)}")

