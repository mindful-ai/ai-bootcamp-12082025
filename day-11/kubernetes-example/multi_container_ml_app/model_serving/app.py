from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Model Serving", version="1.0.0")

class FeaturesRequest(BaseModel):
    features: List[float]

class PredictionResponse(BaseModel):
    prediction: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
def predict(payload: FeaturesRequest):
    # Simple example model: sum the features
    pred = float(sum(payload.features))
    return {"prediction": pred}
