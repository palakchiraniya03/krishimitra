from typing import Dict
import joblib
from pathlib import Path

class IrrigationPredictor:
    def __init__(self):
        self.crop_thresholds = {
            "wheat": 40,
            "rice": 70,
            "barley": 35,
            "sugarcane": 60,
            "cotton": 45,
            "maize": 50,
            "tomato": 55,
            "onion": 45,
            "soybean": 50,
        }
        model_path = Path(__file__).resolve().parents[3] / "ml-model" / "model.pkl"
        scaler_path = Path(__file__).resolve().parents[3] / "ml-model" / "scaler.pkl"

        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

    def predict(self, crop: str, moisture: float) -> Dict:
        crop = crop.lower()

        if crop not in self.crop_thresholds:
            return {
                "error": f"Unknown crop: {crop}"
            }

        threshold = self.crop_thresholds[crop]

        last_value = moisture
        trend = 0  # We don't have previous readings yet

        features = self.scaler.transform([[last_value, trend]])
        predicted_steps = float(self.model.predict(features)[0])

        needs_irrigation = moisture < threshold

        if needs_irrigation:
            recommendation = (
                "Soil moisture is below the recommended threshold. "
                "Irrigation is advised."
            )
        else:
            recommendation = (
                "Soil moisture is within the recommended range. "
                "No irrigation is needed right now."
            )

        return {
            "crop": crop,
            "current_moisture": moisture,
            "threshold": threshold,
            "predicted_steps_until_threshold": round(predicted_steps, 2),
            "needs_irrigation": needs_irrigation,
            "recommendation": recommendation,
        }