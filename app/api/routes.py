from fastapi import APIRouter

from app.schemas.prediction import CognitiveLoadInput
from app.services.prediction_service import predict_cognitive_load


router = APIRouter()


@router.get("/")
def root():
    return {"message": "Cognitive Load Prediction API is running"}


@router.post("/predict")
def predict(data: CognitiveLoadInput):
    return predict_cognitive_load(data)
