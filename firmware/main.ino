#include <WiFi.h>
#include <Firebase_ESP_Client.h>

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

  Serial.print("Moisture: ");
  Serial.println(moisture);

  // Send moisture to Firebase
  if (Firebase.RTDB.setInt(&fbdo, "/plant/moisture", moisture)) {
    Serial.println("Moisture sent");
  } else {
    Serial.println(fbdo.errorReason());
  }

  // Log to history
  String path = "/history/" + String(millis());
  Firebase.RTDB.setInt(&fbdo, path + "/moisture", moisture);
  Firebase.RTDB.setInt(&fbdo, path + "/timestamp", millis());

  delay(5000);
}