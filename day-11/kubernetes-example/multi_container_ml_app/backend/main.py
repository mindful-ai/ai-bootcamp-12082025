from typing import List
import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MODEL_SERVING_URL = os.getenv("MODEL_SERVING_URL", "http://model_serving:5001/predict")
LOGGER_URL = os.getenv("LOGGER_URL", "http://logger:5003/log")

app = FastAPI(title="Backend API", version="1.0.0")

class FeaturesRequest(BaseModel):
    features: List[float]

class PredictionResponse(BaseModel):
    prediction: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
def get_prediction(payload: FeaturesRequest):
    try:
        # forward to model serving
        response = requests.post(MODEL_SERVING_URL, json={"features": payload.features}, timeout=5)
        response.raise_for_status()
        data = response.json()

        # optional logging
        try:
            requests.post(LOGGER_URL, json={"event": "prediction", "features": payload.features, "result": data}, timeout=2)
        except Exception:
            pass

        return data
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
