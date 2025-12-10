#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>

// ========================================================== 
// 1. KONFIGURASI WI-FI (WAJIB DIGANTI!) 
// ========================================================== 
// GANTI dengan kredensial jaringan Anda 
const char* ssid = "Reedo L22"; 
const char* password = ""; 

// ========================================================== 
// 2. KONFIGURASI SERVO 
// ========================================================== 
// Pin Sinyal Servo dihubungkan ke GPIO 26 
const int servoPin = 26; 
Servo feederServo; 

// Objek Web Server, Port 80 
WebServer server(80); 

// ========================================================== 
// FUNGSI UNTUK MENGATUR SERVO 
// ========================================================== 
void handleServo() { 
  String response = ""; 
  
  // Cek apakah parameter 'pos' (posisi sudut) ada di URL 
  if (server.hasArg("pos")) { 
    String posStr = server.arg("pos"); 
    int pos = posStr.toInt(); 
    
    // Validasi: Posisi harus antara 0 hingga 180 derajat 
    if (pos >= 0 && pos <= 180) { 
      feederServo.write(pos); // GERAKKAN SERVO ke posisi yang diminta 
      response = "OK: Servo bergerak ke posisi " + posStr + " derajat."; 
      Serial.print("Perintah diterima, Servo pindah ke: "); 
      Serial.println(pos); 
    } else { 
      response = "ERROR: Posisi harus antara 0 hingga 180."; 
      Serial.println("ERROR: Posisi di luar batas."); 
    } 
  } else { 
    // Jika parameter 'pos' tidak ada 
    response = "ERROR: Parameter 'pos' tidak ditemukan. Format: /servo?pos=90"; 
    Serial.println("ERROR: Parameter 'pos' hilang."); 
  } 
  
  // Kirim respons balik ke Client (Laptop Python) 
  server.send(200, "text/plain", response); 
} 

// Fungsi dasar untuk halaman root 
void handleRoot() { 
  String html = "<html><head><title>ESP32 Servo Control</title></head><body>";
  html += "<h1>ESP32 Servo Web Server</h1>";
  html += "<p>Servo terhubung pada GPIO 26</p>";
  html += "<p>Gunakan format: <b>/servo?pos=90</b> untuk mengontrol servo</p>";
  html += "<form action='/servo' method='GET'>";
  html += "Posisi Servo (0-180): <input type='number' name='pos' min='0' max='180' value='90'>";
  html += "<input type='submit' value='Kirim'>";
  html += "</form></body></html>";
  
  server.send(200, "text/html", html); 
} 

// ========================================================== 
// SETUP DAN LOOP UTAMA 
// ========================================================== 
void setup() { 
  Serial.begin(115200); 
  delay(1000);
  
  // Inisialisasi Servo pada GPIO 26 
  feederServo.attach(servoPin); 
  feederServo.write(0); // Atur posisi awal: 0 derajat (Katup Tertutup / STOP Pakan) 
  Serial.println("Servo diinisialisasi pada posisi 0 derajat (GPIO 26)."); 
  
  // --- KONEKSI WI-FI --- 
  Serial.print("Connecting to "); 
  Serial.println(ssid); 
  WiFi.begin(ssid, password); 
  
  // Tunggu hingga koneksi Wi-Fi berhasil 
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) { 
    delay(500); 
    Serial.print("."); 
    attempts++;
  } 
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected"); 
    Serial.print("IP Address: "); 
    Serial.println(WiFi.localIP()); // TAMPILKAN IP ADDRESS LOKAL 
  } else {
    Serial.println("\nGagal terhubung ke WiFi!");
    Serial.println("Periksa SSID dan Password Anda.");
  }
  
  // --- INISIALISASI WEB SERVER --- 
  server.on("/", handleRoot); 
  server.on("/servo", handleServo); // Menangani semua permintaan yang masuk ke /servo 
  server.begin(); 
  Serial.println("HTTP Server started on Port 80."); 
} 

void loop() { 
  // Wajib: Memproses permintaan yang masuk ke server 
  server.handleClient(); 
}