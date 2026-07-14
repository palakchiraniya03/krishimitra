# KrishiMitra 🌱 — Smart Irrigation System

> An IoT-based smart irrigation system that automates crop watering using real-time soil moisture data, weather intelligence, and a multilingual mobile app — reducing manual intervention by **~60%** in pilot testing.

---

## 📸 Screenshots

## 📸 Screenshots

### App Interface
| Dashboard | Actions | Crop Select |
|---|---|---|
| ![Dashboard](public/screenshot-dashboard.png) | ![Actions](public/screenshot-actions.png) | ![Crops](public/screenshot-crops.png) |

| History | Settings |
|---|---|
| ![History](public/screenshot-history.png) | ![Settings](public/screenshot-settings.png) |

### Multilingual Support
| Dashboard (Hindi) | Crop Select (Marathi) |
|---|---|
| ![Hindi](public/screenshot-dashboard-hindi.png) | ![Marathi](public/screenshot-crops-marathi.png) |

### Hardware Setup
| ESP32 + Soil Moisture Sensor |
|---|
| ![Hardware](public/hardware-setup-1.jpg) |
---
## 📌 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Firebase Database Schema](#firebase-database-schema)
- [Supported Crops](#supported-crops)
- [Team](#team)

---

## Overview

KrishiMitra is a full-stack IoT irrigation solution built for small and mid-scale farmers.The ESP32 microcontroller continuously reads soil moisture from a capacitive sensor and syncs data to Firebase Realtime Database. A React-based Progressive Web App (PWA) with an Android wrapper reads this data live and automatically controls a water pump — while also checking real-time rain forecasts via the OpenWeatherMap API to avoid unnecessary watering.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        HARDWARE LAYER                       │
│                                                             │
│   Soil Moisture Sensor ──┐                                  │
│   ──────────────────────┘──► ESP32 Microcontroller          │
│   Water Pump ◄───────────┘        │                        │
└───────────────────────────────────┼────────────────────────┘
                                    │ WiFi (HTTPS)
                                    ▼
┌─────────────────────────────────────────────────────────────┐
│                     FIREBASE REALTIME DB                    │
│                                                             │
│   /plant                                                    │
│     ├── moisture      (number)                              │
│     ├── temperature   (number)                              │
│     ├── humidity      (number)                              │
│     ├── pump          ("ON" | "OFF")                        │
│     ├── threshold     (number)                              │
│     ├── type          (crop ID string)                      │
│     └── place         (string)                              │
│   /history                                                  │
│     └── {timestamp}: { moisture, temperature, timestamp }   │
└───────────────────┬─────────────────────────────────────────┘
                    │ onValue() listener (real-time)
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND APP (React + Capacitor)       │
│                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │  Dashboard  │    │ ActionsScreen│    │ DeviceStatus  │  │
│  │             │    │              │    │               │  │
│  │ Live sensor │    │ Manual pump  │    │ Sensor health │  │
│  │ stats       │    │ ON/OFF       │    │ WiFi + battery│  │
│  │ Auto pump   │    │ Smart water  │    │ Last updated  │  │
│  │ logic       │    │ suggestion   │    │               │  │
│  └─────────────┘    └──────────────┘    └───────────────┘  │
│  ┌─────────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │HistoryScreen│    │Notifications │    │CropSelect     │  │
│  │             │    │              │    │               │  │
│  │ Moisture    │    │ Smart alerts │    │ 9 crops incl. │  │
│  │ over time   │    │ pump + water │    │ Wheat, Rice,  │  │
│  │ chart       │    │ reminders    │    │ Barley, etc.  │  │
│  └─────────────┘    └──────────────┘    └───────────────┘  │
└───────────────────┬─────────────────────────────────────────┘
                    │ fetch()
                    ▼
┌─────────────────────────────────────────────────────────────┐
│              OPENWEATHERMAP API                             │
│  GET /data/2.5/weather?lat={lat}&lon={lon}                  │
│  → Returns current weather condition                        │
│  → If rain detected → Auto pump paused                      │
└─────────────────────────────────────────────────────────────┘

### Auto Pump Logic Flow

```
Every time moisture or location updates:
    │
    ├──► Fetch weather for current GPS coordinates
    │
    ├── Is it raining?
    │     YES → Set pump OFF, show "Rain detected" banner
    │     NO  → Check moisture vs crop threshold
    │               moisture < threshold → Set pump ON
    │               moisture ≥ threshold → Set pump OFF
    │
    └──► Write pump status to Firebase → ESP32 reads → Pump actuates
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Microcontroller | ESP32 (Arduino framework) |
| Sensors | Soil Moisture Sensor|
| Backend / Database | Firebase Realtime Database |
| Authentication | Firebase Auth (Google OAuth) |
| Frontend Framework | React + TypeScript + Vite |
| UI Components | shadcn/ui + Tailwind CSS |
| Mobile Wrapper | Capacitor (Android APK) |
| Weather API | OpenWeatherMap (`/data/2.5/weather`) |
| State Management | Custom React hooks (`usePlantData`, `useLanguage`, `useLocation`) |
| Routing | React Router DOM |
| Icons | Lucide React |

---

## Features

### 🤖 Intelligent Auto-Irrigation
- Pump is controlled **automatically** based on two conditions combined:
  - Soil moisture reading vs crop-specific threshold
  - Real-time rain detection via GPS + OpenWeatherMap
- If it's raining, pump stays OFF regardless of moisture level

### 📊 Live Sensor Dashboard
- Real-time soil moisture % from ESP32 sensor
- Moisture progress bar showing level vs threshold at a glance
- Recent activity log with timestamps pulled from Firebase `/history`

### 🌾 Crop-Aware Thresholds
- Supports 9 crops: Wheat, Rice, Barley, Sugarcane, Cotton, Maize, Tomato, Onion, Soybean
- Each crop has a predefined optimal moisture threshold
- User can switch crops anytime; threshold updates automatically

### 💧 Manual Pump Control
- Override auto mode: turn pump ON or OFF manually from ActionsScreen
- Smart suggestion shown based on current moisture vs threshold
- Toast notifications confirm pump state changes

### 🔔 Smart Notifications
- Alerts when moisture drops below threshold
- Warning when pump is OFF but moisture is critically low
- "All good" confirmation when plant is well-watered

### 🌍 Multilingual Support
- Full UI available in **English**, **Hindi**, and **Marathi**
- Language preference stored in localStorage
- All screens, labels, and alerts are translated

### 📱 Android App
- Built as a PWA and wrapped with Capacitor for native Android APK
- Mobile-first UI with bottom navigation

---

## Project Structure

```
smart-plant-care/
├── src/
│   ├── pages/
│   │   ├── Dashboard.tsx         # Main screen: live stats, auto pump, activity log
│   │   ├── ActionsScreen.tsx     # Manual pump ON/OFF control
│   │   ├── DeviceStatus.tsx      # ESP32 connection, battery, WiFi status
│   │   ├── HistoryScreen.tsx     # Moisture over time chart
│   │   ├── NotificationsScreen.tsx
│   │   ├── CropSelectScreen.tsx  # Crop picker with images
│   │   ├── PlantDetails.tsx      # Per-plant stats and activity log
│   │   ├── LoginScreen.tsx       # Google OAuth login
│   │   └── SettingsScreen.tsx    # Language, privacy settings
│   ├── hooks/
│   │   ├── use-plant-data.ts     # Firebase listener + setPump()
│   │   ├── use-language.ts       # i18n translation hook
│   │   └── use-location.ts       # GPS coordinates hook
│   ├── lib/
│   │   ├── firebase.ts           # Firebase app, db, auth, GoogleProvider init
│   │   ├── crops.ts              # Crop definitions + thresholds
│   │   ├── i18n.ts               # All translations: EN / HI / MR
│   │   └── utils.ts
│   ├── components/
│   │   ├── MobileLayout.tsx
│   │   ├── BottomNav.tsx
│   │   └── ui/                   # shadcn/ui component library
│   └── assets/                   # Crop images, logos
├── android/                      # Capacitor Android project
├── public/
├── capacitor.config.ts
└── package.json
```

---

## Setup Instructions

### Prerequisites
- Node.js 18+
- Android Studio (for APK build)
- Firebase project with Realtime Database enabled
- OpenWeatherMap API key (free tier works)

### 1. Clone and install

```bash
git clone https://github.com/palakchiraniya03/krishimitra.git
cd krishimitra
npm install
```

### 2. Configure Firebase

Replace the config in `src/lib/firebase.ts` with your own Firebase project credentials:

```ts
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  databaseURL: "https://YOUR_PROJECT-default-rtdb.firebasedatabase.app",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};
```

### 3. Configure OpenWeatherMap

In `src/pages/Dashboard.tsx`, replace the API key:

```ts
const API_KEY = "YOUR_OPENWEATHERMAP_KEY";
```

### 4. Run the web app

```bash
npm run dev
```

### 5. Build Android APK

```bash
npm run build
npx cap sync android
npx cap open android
```
Then build the APK from Android Studio.

### 6. ESP32 Firmware

- Open `/firmware` folder in Arduino IDE
- Replace WiFi  SSID, password, and Firebase credentials in main.ino
- Flash to ESP32
- Sensor data will begin syncing to Firebase automatically

---

## Firebase Database Schema

```json
{
  "plant": {
    "moisture": 42,
          "pump": "OFF",
    "threshold": 50,
    "type": "wheat",
    "place": "Pune, Maharashtra"
  },
  "history": {
    "1716800000000": {
      "moisture": 38,
      "timestamp": 1716800000000
    }
  }
}
```

---
- [Supported Crops](#supported-crops)
- [Predictive Irrigation Model](#predictive-irrigation-model)
- [Team](#team)

## Supported Crops

| Crop | Default Moisture Threshold |
|---|---|
| 🌾 Wheat | 40% |
| 🌾 Rice | 70% |
| 🌾 Barley | 35% |
| 🎋 Sugarcane | 60% |
| 🌿 Cotton | 45% |
| 🌽 Maize | 50% |
| 🍅 Tomato | 55% |
| 🧅 Onion | 45% |
| 🌱 Soybean | 50% |
---

## Predictive Irrigation Model

Built a regression pipeline to predict the number of sensor readings until soil moisture crosses a crop-specific watering threshold, using real sensor data logged from the deployed ESP32, evaluated across all 9 crops supported by the app.

**Data & Preprocessing**: 56 real moisture readings extracted from Firebase history. 11 readings of exactly 0% were identified as likely sensor-disconnect errors and removed, leaving 45 clean readings. Temporal order was used as a proxy for time, due to a firmware timestamp bug present during earlier logging (see Known Limitations).

**Exploratory Data Analysis**: Cleaned readings ranged from 12% to 100% (mean 53.7%, median 45%, std dev 23.1), with no extreme skew — confirming the cleaning step removed clear sensor errors without over-trimming legitimate low readings.

**Approach**: Engineered 2 features per example (most recent reading, recent trend) using a sliding-window transformation of the time series. Features were standardized before training so coefficients are directly comparable as feature importance. Linear Regression and Ridge Regression were both trained and compared; Ridge showed no improvement over plain Linear Regression (MAE 0.84 for both), indicating regularization wasn't needed to control overfitting at this sample size.

**Cross-Validation Methodology**: Standard k-fold cross-validation risks data leakage here, since sliding windows overlap (consecutive windows share up to 4 of 5 readings) — randomly splitting overlapping windows across folds can let the model indirectly "see" near-duplicate test data during training. To avoid this, `TimeSeriesSplit` was used instead, which always trains on earlier readings and evaluates on later ones, preserving temporal order and avoiding leakage.

**Feature Importance** (scaled coefficients, Wheat): `last_value` = 0.659, `trend` = -0.441 — the model relies more heavily on the current moisture level than on the recent rate of change.

**Results** (TimeSeriesSplit cross-validated MAE, in readings):

| Crop | MAE | Examples | Crop | MAE | Examples |
|---|---|---|---|---|---|
| Sugarcane (60%) | 0.09 | 30 | Cotton (45%) | 0.52 | 30 |
| Tomato (55%) | 0.09 | 30 | Onion (45%) | 0.52 | 30 |
| Maize (50%) | 0.13 | 30 | Wheat (40%) | 1.14 | 30 |
| Soybean (50%) | 0.13 | 30 | Barley (35%) | 3.15 | 30 |
| Rice (70%) | 0.38 | 40 | | | |

**Data quality vs. quantity trade-off**: Removing suspected sensor-error readings reduced the Wheat training set from 46 to 30 examples. Several crops show very low MAE (0.09–0.13) on only ~24-30 training examples — at this sample size, such low error is more plausibly explained by limited test-set diversity than strong genuine model skill, even after correcting the cross-validation methodology. This is disclosed rather than presented as a strong result.

**Error Analysis**: Residual analysis on Wheat showed a small negative mean residual (-0.168) and a residual standard deviation of 1.028, indicating fairly imprecise but roughly unbiased predictions. A window-size sensitivity check (sizes 3, 5, 7), re-run with the corrected TimeSeriesSplit methodology, found window size 5 performed best (MAE 1.14 vs. 1.45 and 1.16).

**On data augmentation**: Synthetic data augmentation was considered but intentionally not used, since synthetically generated points risk introducing patterns that don't reflect genuine sensor behavior in a small, noisy real-world time series — a legitimate use case for it exists more in image/text data.

**Key finding**: Prediction accuracy varies by crop threshold, with a general (though noisy, given sample size) tendency for higher-threshold crops to be more predictable than lower-threshold ones — likely because higher thresholds require shorter-horizon predictions with less time for trend uncertainty to compound.

**Limitations**: Dataset size (24-40 examples per crop after cleaning) is small even by small-dataset ML standards, and several very-low-MAE results likely reflect limited test-set diversity rather than strong generalization. **Future direction**: This pipeline is batch/offline — it trains on a static export of accumulated Firebase history. Since sensor data is inherently a continuous stream, an online/incremental learning approach (e.g., using the River library) would be a more natural production fit, updating the model as each new reading arrives rather than requiring periodic manual re-export and retraining. Demonstrates a complete ML evaluation pipeline (EDA, preprocessing, feature scaling, feature importance, model comparison, leakage-aware cross-validation, baseline comparison, residual diagnostics, hyperparameter sensitivity, and per-crop generalization analysis) on real hardware-collected data, with explicit acknowledgment of where results should be interpreted cautiously.

![Prediction Results](ml-model/prediction_results.png)
![Prediction vs Actual Reference](ml-model/prediction_vs_actual_reference.png)
![Residual Plot](ml-model/residual_plot.png)
![EDA Moisture Over Time](ml-model/eda_moisture_over_time.png)
![EDA Moisture Distribution](ml-model/eda_moisture_distribution.png)

## Team

Built in collaboration with **Divyam Jain**, **Aryan Shahi**, and **Diya Toshniwal**
for the **IEEE Techfiesta Hackathon at PICT Pune** and **Resonance Hackathon, VIT** *(Finalist — IoT Domain)*.

---

## Known Limitations & In Progress

- **Timestamp overflow fix**: A 32-bit integer overflow bug in the ESP32 firmware's timestamp logic (affecting `/history` entries) has been identified and fixed in code — corrected to use 64-bit arithmetic and proper Firebase double storage. The fix has been independently verified at the logic level (confirmed correct 13-digit millisecond output via isolated testing), but full end-to-end verification via hardware flash and live Firebase write is pending ESP32 access.
- **Firebase project access**: The Firebase project is currently owned under a teammate's Google account; full console-level testing access is pending being added as a project member.
- **Predictive irrigation model**: Completed — see [Predictive Irrigation Model](#predictive-irrigation-model) section above.
