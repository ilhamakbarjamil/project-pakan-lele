#include <WiFi.h>
#include <HTTPClient.h>
#include <ESP32Servo.h>

// ====== KONFIGURASI JARINGAN (SUDAH DIPERBAIKI!) ======
const char* ssid = "Reedo L22";          // Sesuaikan dengan nama WiFi Anda
const char* password = "";                // Sesuaikan dengan password WiFi
const char* laptopIP = "192.168.110.99"; // IP LAPTOP ANDA YANG BENAR!

// ====== PIN & KONFIGURASI ======
#define SERVO_PIN 13
#define SERVO_OPEN 100
#define SERVO_CLOSE 0

Servo feederServo;
unsigned long lastRequest = 0;
const long requestInterval = 2000; // Polling setiap 2 detik
bool isConnected = false;

void setup() {
  Serial.begin(115200);
  Serial.println("\n\n=== SMART FEEDING SYSTEM - FIXED IP MODE ===");
  Serial.println("✓ IP Laptop: 192.168.110.99 (SUDAH DIPERBAIKI!)");
  Serial.println("1. Pastikan server Flask di laptop SUDAH DIJALANKAN");
  Serial.println("2. Gunakan POWER SUPPLY EKSTERNAL untuk servo!");
  Serial.println("3. Laptop dan ESP32 dalam jaringan WiFi yang SAMA");
  Serial.println("===========================================\n");

  // Setup servo
  feederServo.attach(SERVO_PIN);
  feederServo.write(SERVO_CLOSE); // Pastikan servo tertutup
  
  // Koneksi WiFi
  connectToWiFi();
}

void loop() {
  // Cek koneksi WiFi setiap 30 detik
  if (millis() - lastRequest > 30000) {
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("[!] WiFi terputus, mencoba reconnect...");
      connectToWiFi();
    }
  }

  // Polling server setiap interval
  if (millis() - lastRequest >= requestInterval && isConnected) {
    lastRequest = millis();
    String status = getStatusFromServer();
    
    if (status != "") {
      Serial.printf("[🔍] Status diterima: [%s]\n", status.c_str());
      
      // Kontrol servo berdasarkan status
      if (status.indexOf("TAMBAH PAKAN") >= 0) {
        Serial.println("[✅] DETEKSI: Perlu tambah pakan!");
        giveFeed();
      } 
      else if (status.indexOf("STOP PAKAN") >= 0) {
        Serial.println("[⚠️] DETEKSI: Stop pemberian pakan!");
        closeFeeder();
      }
      else {
        Serial.println("[ℹ️] Status: STABIL");
        closeFeeder();
      }
    }
  }
  delay(10);
}

// ====== FUNGSI UTAMA ======

void connectToWiFi() {
  Serial.print("Menghubungkan ke WiFi: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  int attempts = 0;
  
  while (WiFi.status() != WL_CONNECTED && attempts < 15) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✓ WiFi terhubung!");
    Serial.print("IP ESP32: ");
    Serial.println(WiFi.localIP());
    Serial.print("Target Server: http://");
    Serial.print(laptopIP);
    Serial.println(":5000/data");
    isConnected = true;
  } else {
    Serial.println("\n✗ Gagal terhubung ke WiFi");
    isConnected = false;
  }
}

String getStatusFromServer() {
  HTTPClient http;
  String url = "http://" + String(laptopIP) + ":5000/data";
  
  Serial.print("\n[📡] Mengakses: ");
  Serial.println(url);
  
  http.begin(url);
  int httpCode = http.GET();
  
  if (httpCode == 200) {
    String payload = http.getString();
    Serial.print("[✅] Respons: ");
    Serial.println(payload);
    
    // Ekstrak status dari JSON
    int statusStart = payload.indexOf("\"status\":\"") + 10;
    int statusEnd = payload.indexOf("\"", statusStart);
    if (statusStart > 10 && statusEnd > statusStart) {
      return payload.substring(statusStart, statusEnd);
    }
    return "STABIL";
  } 
  else {
    Serial.printf("[❌] Error HTTP %d\n", httpCode);
    return "";
  }
  
  http.end();
}

void giveFeed() {
  Serial.print("[⚙️] Memberikan pakan selama 3 detik...");
  
  // Buka servo dengan gerakan halus
  feederServo.write(SERVO_OPEN);
  delay(500); // Stabilkan posisi
  
  // Tahan terbuka selama 3 detik
  unsigned long startTime = millis();
  while (millis() - startTime < 3000) {
    delay(10);
  }
  
  // Tutup servo
  closeFeeder();
  Serial.println(" ✓ Selesai");
}

void closeFeeder() {
  feederServo.write(SERVO_CLOSE);
}