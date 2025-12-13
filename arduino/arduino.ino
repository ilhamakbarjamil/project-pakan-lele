#include <WiFi.h>
#include <HTTPClient.h>
#include <Servo.h>

const char* ssid = "oppo";
const char* password = "123456789";
const char* serverURL = "http://IP_LAPTOP:5000/status";

Servo feederServo;

void setup() {
  Serial.begin(115200);

  feederServo.attach(13);
  feederServo.write(0); // posisi tertutup

  WiFi.begin(ssid, password);
  Serial.print("Connecting WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    int httpCode = http.GET();

    if (httpCode == 200) {
      String payload = http.getString();
      Serial.println(payload);

      if (payload.indexOf("TAMBAH") >= 0) {
        feederServo.write(90);   // buka pakan
      } else {
        feederServo.write(0);    // tutup
      }
    }
    http.end();
  }
  delay(1000);
}
