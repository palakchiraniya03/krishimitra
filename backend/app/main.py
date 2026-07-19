from fastapi import FastAPI, HTTPException
from app.crop_data import CROP_KNOWLEDGE

app = FastAPI(
    title="KrishiMitra AI Service",
    description="Backend service for irrigation prediction and AI-powered crop assistance.",
    version="1.0.0",
)

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