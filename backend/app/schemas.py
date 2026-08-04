from pydantic import BaseModel

class SensorData(BaseModel):
    crop: str
    moisture: float
    temperature: float
    humidity: float
    pumpStatus: str

class PredictionRequest(BaseModel):
    crop: str
    moisture: float

class ChatRequest(BaseModel):
    question: str
    crop: str
    moisture: float
    temperature: float
    humidity: float
    pumpStatus: str
    threshold: float

    isRaining: bool
    forecastRainProbability: float