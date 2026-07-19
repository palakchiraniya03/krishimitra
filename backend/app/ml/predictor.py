from typing import Dict


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

    def predict(self, crop: str, moisture: float) -> Dict:
        crop = crop.lower()

        if crop not in self.crop_thresholds:
            return {
                "error": f"Unknown crop: {crop}"
            }

        threshold = self.crop_thresholds[crop]

        needs_irrigation = moisture < threshold

        return {
            "crop": crop,
            "current_moisture": moisture,
            "threshold": threshold,
            "needs_irrigation": needs_irrigation,
        }