from fastapi import FastAPI

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