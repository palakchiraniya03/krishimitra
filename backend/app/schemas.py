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