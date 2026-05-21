#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include <time.h>

// WiFi
#define WIFI_SSID "YOUR_WIFI_NAME"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// Firebase
#define API_KEY "YOUR_FIREBASE_API_KEY"
#define DATABASE_URL "YOUR_DATABASE_URL"
#define DATABASE_SECRET "YOUR_DATABASE_SECRET"

// Pins
#define MOISTURE_PIN 34

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

void setup() {
  Serial.begin(115200);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("\nConnected!");

  // Sync real time via NTP
  configTime(19800, 0, "pool.ntp.org", "time.nist.gov");
  Serial.print("Syncing time");
  while (time(nullptr) < 1000000000) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("\nTime synced!");

  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;
  config.signer.tokens.legacy_token = DATABASE_SECRET;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void loop() {
  // Read soil moisture
  int moistureRaw = analogRead(MOISTURE_PIN);
  int moisture = map(moistureRaw, 4095, 0, 0, 100);

  // Get real timestamp
  time_t now = time(nullptr);
  unsigned long timestamp = (unsigned long)now * 1000;

  Serial.print("Moisture: ");
  Serial.println(moisture);
  Serial.print("Timestamp: ");
  Serial.println(timestamp);

  // Send moisture to Firebase
  if (Firebase.RTDB.setInt(&fbdo, "/plant/moisture", moisture)) {
    Serial.println("Moisture sent");
  } else {
    Serial.println(fbdo.errorReason());
  }

  // Log to history with real timestamp
  String path = "/history/" + String(timestamp);
  Firebase.RTDB.setInt(&fbdo, path + "/moisture", moisture);
  Firebase.RTDB.setInt(&fbdo, path + "/timestamp", timestamp);

  delay(5000);
}