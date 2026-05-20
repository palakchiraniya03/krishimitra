# KrishiMitra 🌱 — Smart Irrigation System

> An IoT-based smart irrigation system that automates crop watering using real-time soil moisture data, weather intelligence, and a multilingual mobile app — reducing manual intervention by **~60%** in pilot testing.

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
│  │ Moisture    │    │ Smart alerts │    │ Wheat, Rice,  │  │
│  │ over time   │    │ pump + water │    │ Cotton, Maize │  │
│  │ chart       │    │ reminders    │    │ Barley, Sugar │  │
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
```

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
- Supports 6 crops: Wheat, Rice, Barley, Sugarcane, Cotton, Maize
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

## Supported Crops

| Crop | Default Moisture Threshold |
|---|---|
| 🌾 Wheat | 40% |
| 🌾 Rice | 70% |
| 🌾 Barley | 35% |
| 🎋 Sugarcane | 60% |
| 🌿 Cotton | 45% |
| 🌽 Maize | 50% |

---

## Team

Built in collaboration with **Divyam Jain**, **Aryan Shahi**, and **Diya Toshniwal**
for the **IEEE Techfiesta Hackathon at PICT Pune** and **Resonance Hackathon, VIT** *(Finalist — IoT Domain)*.

---