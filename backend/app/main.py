from fastapi import FastAPI, HTTPException
from app.crop_data import CROP_KNOWLEDGE
from fastapi.middleware.cors import CORSMiddleware
from app.ml.predictor import IrrigationPredictor
from app.schemas import SensorData, PredictionRequest, ChatRequest
from app.rag import generate_rag_response
app = FastAPI(
    title="KrishiMitra AI Service",
    description="Backend service for irrigation prediction and AI-powered crop assistance.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "https://krishimitra-mocha.vercel.app",
        "https://krishimitra-8ay644fkw-palak-chiraniya.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
predictor = IrrigationPredictor()

@app.get("/")
def root():
    return {
        "service": "KrishiMitra AI Backend",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/crop/{crop_id}")
def get_crop(crop_id: str):
    crop = CROP_KNOWLEDGE.get(crop_id.lower())

    if crop is None:
        raise HTTPException(
            status_code=404,
            detail=f"Crop '{crop_id}' not found."
        )

    return {
        "id": crop_id.lower(),
        **crop
    }

@app.post("/predict")
def predict(request: PredictionRequest):
    result = predictor.predict(
        crop=request.crop,
        moisture=request.moisture,
    )

    return result

@app.post("/chat")
def chat(request: ChatRequest):
    return generate_rag_response(
        question=request.question,
        crop=request.crop,
        moisture=request.moisture,
        temperature=request.temperature,
        humidity=request.humidity,
        pump_status=request.pumpStatus,
        threshold=request.threshold,

        is_raining=request.isRaining,
        forecast_rain_probability=request.forecastRainProbability,
    )