# Sistem Pengoptimalan Dosis Pakan Ikan Otomatis Berbasis Image Processing dan IoT untuk Mendeteksi Sisa Pakan pada Tambak

## Deskripsi Proyek
Proyek ini adalah prototipe sistem cerdas yang dirancang untuk meningkatkan efisiensi pemberian pakan pada tambak ikan. Dengan memanfaatkan Image Processing (Pemrosesan Citra) dan konektivitas IoT, sistem ini mampu secara otomatis mendeteksi keberadaan sisa pakan di permukaan air. Keputusan untuk memberi atau menghentikan pakan diambil secara real-time untuk mencegah pakan terbuang (mengurangi biaya operasional) dan meminimalkan pencemaran air (meningkatkan kualitas air tambak).

## Fitur Utama
### 1. Deteksi Sisa Pakan Otomatis: Menggunakan algoritma Color Thresholding (OpenCV) untuk mengisolasi dan menghitung persentase sisa pakan di area pemantauan.
### 2. Pengambilan Keputusan Cerdas: Dosis pakan dioptimalkan berdasarkan hasil analisis citra: jika sisa pakan terdeteksi melebihi ambang batas, pemberian pakan otomatis dihentikan sementara.
### 3. Kontrol Otomatis via IoT: Perintah pemberian pakan dikirim secara nirkabel dari modul Image Processing (simulasi Laptop/Python) ke modul Aktuator (ESP32) melalui koneksi HTTP (Web Server lokal).
### 4. Aktuasi Presisi: Menggunakan Servo motor untuk menggerakkan mekanisme feeder dengan dosis yang terukur.


