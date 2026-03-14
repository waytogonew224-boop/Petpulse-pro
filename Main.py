from fastapi import FastAPI
from pydantic import BaseModel, Field
import numpy as np
import os

app = FastAPI(title="PetPulse Pro Omega Engine")

# This helps protect your data
SALT = os.getenv("DATA_SALT", "ludhiana_secure_2026")

class VitalPacket(BaseModel):
    pet_uuid: str
    weight_kg: float
    v: float = Field(..., ge=0, le=1) 
    r: float = Field(..., ge=0, le=1) 
    p: float = Field(..., ge=0, le=1) 
    temp: float = Field(..., ge=30, le=45)
    hrv: float = Field(..., ge=0, le=1)

@app.get("/")
def home():
    return {"status": "online", "engine": "Omega v11.0", "message": "PetPulse Brain is Ready"}

@app.post("/v1/sync")
async def sync_vitals(packet: VitalPacket):
    # Formula Omega v11.0
    hrv_min = 0.25 if packet.weight_kg < 12 else 0.45
    thermal_factor = 1 / (1 + np.exp(0.8 * (packet.temp - 39.5)))
    score = (packet.v * 0.3 + (packet.r * thermal_factor) * 0.3 + packet.hrv * 0.4) * (1 - packet.p)
    
    return {
        "omega_score": round(float(score), 4),
        "status": "STABLE" if score > 0.5 else "RISK_DETECTED"
    }

  
