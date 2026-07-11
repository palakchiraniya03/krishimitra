import json
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge

# ============================================================
# STEP 1: Load exported Firebase data
# ============================================================
with open("history_data.json", "r") as f:
    data = json.load(f)

print("Total entries loaded:", len(data))

moisture_readings = []
for key, entry in data.items():
    if "moisture" in entry:
        moisture_readings.append(entry["moisture"])

print("Moisture entries found:", len(moisture_readings))
print("First 10 readings:", moisture_readings[:10])

# ============================================================
# STEP 1b: Preprocessing — remove suspicious sensor-error readings
# ============================================================
# A reading of exactly 0 is very likely a sensor disconnect/error,
# not genuine "completely dry" soil — real moisture rarely hits a
# hard 0 in one step then jumps back to 100 the next reading.
raw_count = len(moisture_readings)
moisture_readings = [m for m in moisture_readings if m > 0]
print(f"Removed {raw_count - len(moisture_readings)} suspicious zero-readings (likely sensor errors)")
print("Moisture entries after cleaning:", len(moisture_readings))

# ============================================================
# STEP 1c: Exploratory Data Analysis (EDA)
# ============================================================
print("\n--- Exploratory Data Analysis ---")
print("Number of readings:", len(moisture_readings))
print("Min:", min(moisture_readings), "| Max:", max(moisture_readings))
print("Mean:", round(np.mean(moisture_readings), 2), "| Std Dev:", round(np.std(moisture_readings), 2))
print("Median:", np.median(moisture_readings))

plt.figure(figsize=(10, 4))
plt.plot(moisture_readings, marker="o", color="teal", markersize=4)
plt.xlabel("Reading Index (time order)")
plt.ylabel("Moisture (%)")
plt.title("Raw Moisture Readings Over Time (after cleaning)")
plt.grid(alpha=0.3)
plt.savefig("eda_moisture_over_time.png")
print("EDA time-series chart saved as eda_moisture_over_time.png")

plt.figure(figsize=(8, 4))
plt.hist(moisture_readings, bins=10, color="coral", edgecolor="black")
plt.xlabel("Moisture (%)")
plt.ylabel("Frequency")
plt.title("Distribution of Moisture Readings")
plt.savefig("eda_moisture_distribution.png")
print("EDA distribution chart saved as eda_moisture_distribution.png")

window_size = 5

def build_dataset(readings, threshold, window_size):
    """
    Converts a raw time-ordered list of moisture readings into a
    supervised learning dataset using a sliding window.
    X = [last_value, trend] for each window
    y = number of steps until moisture crosses the threshold
    """
    X, y = [], []
    for i in range(len(readings) - window_size):
        window = readings[i : i + window_size]
        steps_ahead = None
        for j in range(i + window_size, len(readings)):
            if readings[j] <= threshold:
                steps_ahead = j - (i + window_size)
                break
        if steps_ahead is not None:
            last_value = window[-1]
            trend = window[-1] - window[0]
            X.append([last_value, trend])
            y.append(steps_ahead)
    return np.array(X), np.array(y)

# ============================================================
# STEP 2: Detailed analysis on Wheat (primary crop, generates chart)
# ============================================================
print("\n--- Detailed Analysis: Wheat (threshold=40) ---")

X_array, y_array = build_dataset(moisture_readings, threshold=40, window_size=window_size)
print("Training examples created:", len(X_array))

# --- Feature scaling ---
scaler = StandardScaler()
X_array_scaled = scaler.fit_transform(X_array)

X_train, X_test, y_train, y_test = train_test_split(
    X_array_scaled, y_array, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
print("Training examples:", len(X_train), "| Testing examples:", len(X_test))

predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print("Mean Absolute Error:", round(mae, 2), "steps")

plt.figure(figsize=(8, 5))
plt.scatter(range(len(y_test)), y_test, label="Actual", color="green", s=80)
plt.scatter(range(len(y_test)), predictions, label="Predicted", color="orange", s=80)
plt.xlabel("Test Example")
plt.ylabel("Steps Until Threshold Crossed")
plt.title("Predicted vs Actual Watering Need (Wheat)")
plt.legend()
plt.savefig("prediction_results.png")
print("Chart saved as prediction_results.png")

baseline_prediction = np.mean(y_train)
baseline_mae = mean_absolute_error(y_test, [baseline_prediction] * len(y_test))
print("Baseline (always predict average):", round(baseline_mae, 2), "steps")

# --- Feature importance (valid now that features are scaled) ---
print("\n--- Feature Importance (scaled coefficients) ---")
print("last_value importance:", round(model.coef_[0], 3))
print("trend importance:", round(model.coef_[1], 3))
print("(Comparable directly since both features are on the same scale)")

# ============================================================
# STEP 2a-2: Model comparison — Ridge Regression
# ============================================================
from sklearn.linear_model import Ridge

ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train, y_train)
ridge_predictions = ridge_model.predict(X_test)
ridge_mae = mean_absolute_error(y_test, ridge_predictions)

print("\n--- Model Comparison (Wheat) ---")
print("Linear Regression MAE:", round(mae, 2))
print("Ridge Regression MAE:", round(ridge_mae, 2))
print("(Ridge adds regularization — useful to check if it helps stabilize predictions given the small dataset)")

tscv = TimeSeriesSplit(n_splits=5)
cv_scores = cross_val_score(model, X_array_scaled, y_array, cv=tscv, scoring="neg_mean_absolute_error")
print("\nCross-validated MAE (5-fold):", round(-cv_scores.mean(), 2))
print("Individual fold scores:", [round(-s, 2) for s in cv_scores])

# ============================================================
# STEP 2b: Reference line + residual plot (diagnostic check)
# ============================================================
plt.figure(figsize=(8, 5))
plt.scatter(y_test, predictions, color="steelblue", s=80, alpha=0.7)
max_val = max(max(y_test), max(predictions))
plt.plot([0, max_val], [0, max_val], "r--", label="Perfect Prediction (y=x)")
plt.xlabel("Actual Steps Until Threshold")
plt.ylabel("Predicted Steps Until Threshold")
plt.title("Actual vs Predicted (Wheat) — with Reference Line")
plt.legend()
plt.savefig("prediction_vs_actual_reference.png")
print("Reference-line chart saved as prediction_vs_actual_reference.png")

residuals = y_test - predictions
plt.figure(figsize=(8, 5))
plt.scatter(predictions, residuals, color="purple", s=80, alpha=0.7)
plt.axhline(y=0, color="red", linestyle="--")
plt.xlabel("Predicted Value")
plt.ylabel("Residual (Actual - Predicted)")
plt.title("Residual Plot (Wheat)")
plt.savefig("residual_plot.png")
print("Residual plot saved as residual_plot.png")
print("Residual mean:", round(np.mean(residuals), 3), "| Residual std:", round(np.std(residuals), 3))

# ============================================================
# STEP 2c: Window size sensitivity check
# ============================================================
print("\n--- Window Size Sensitivity (Wheat, threshold=40) ---")
for ws in [3, 5, 7]:
    X_ws, y_ws = build_dataset(moisture_readings, threshold=40, window_size=ws)
    if len(X_ws) < 10:
        print(f"window_size={ws}: skipped, only {len(X_ws)} examples")
        continue
    X_ws_scaled = StandardScaler().fit_transform(X_ws)
    ws_model = LinearRegression()
    ws_tscv = TimeSeriesSplit(n_splits=5)
    ws_scores = cross_val_score(ws_model, X_ws_scaled, y_ws, cv=ws_tscv, scoring="neg_mean_absolute_error")
    print(f"window_size={ws}: {len(X_ws)} examples, cross-validated MAE = {round(-ws_scores.mean(), 2)}")

# ============================================================
# STEP 3: Generalization check across all 9 supported crops
# ============================================================
print("\n--- Generalization Across All Crops ---")

crop_thresholds = {
    "wheat": 40, "rice": 70, "barley": 35, "sugarcane": 60,
    "cotton": 45, "maize": 50, "tomato": 55, "onion": 45, "soybean": 50,
}

results = {}
for crop_name, threshold in crop_thresholds.items():
    X, y = build_dataset(moisture_readings, threshold, window_size)

    if len(X) < 10:
        print(f"{crop_name}: skipped, only {len(X)} examples (too few)")
        continue

    X_scaled = StandardScaler().fit_transform(X)
    crop_model = LinearRegression()
    crop_tscv = TimeSeriesSplit(n_splits=5)
    scores = cross_val_score(crop_model, X_scaled, y, cv=crop_tscv, scoring="neg_mean_absolute_error")
    avg_mae = round(-scores.mean(), 2)
    results[crop_name] = {"examples": len(X), "cv_mae": avg_mae}
    print(f"{crop_name}: {len(X)} examples, cross-validated MAE = {avg_mae}")

print("\nSummary across all crops:")
for crop, r in results.items():
    print(f"  {crop}: MAE={r['cv_mae']}, examples={r['examples']}")