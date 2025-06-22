from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()
df = pd.DataFrame()

class VitalData(BaseModel):
    patient_id: str
    heart_rate: int
    spo2: float
    temperature: float
    timestamp: str

@app.post("/submit")
def submit_vitals(data: VitalData):
    global df
    df = pd.concat([df, pd.DataFrame([data.dict()])], ignore_index=True)
    return {"message": "Date înregistrate"}
