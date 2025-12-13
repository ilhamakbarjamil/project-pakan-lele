import cv2
import numpy as np
import requests
import time

# ===============================
# KONFIGURASI
# ===============================
SERVER_URL = "http://localhost:5000/update"
SEND_INTERVAL = 1.0  # kirim status tiap 1 detik

latest_frame = None
cap = cv2.VideoCapture(0)
last_send = 0
status = "STABIL"

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera tidak terbaca")
        break

    # Resize biar ringan
    frame = cv2.resize(frame, (640, 480))

    # Crop area air (sesuaikan jika perlu)
    roi = frame[200:450, 100:540]

    # Image processing
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 160, 255, cv2.THRESH_BINARY)

    # Hitung area putih (pakan)
    white_area = cv2.countNonZero(thresh)
    total_area = thresh.shape[0] * thresh.shape[1]
    percentage = (white_area / total_area) * 100

    # global latest_frame
    latest_frame = frame.copy()


    # Logika keputusan
    if percentage > 20:
        status = "STOP PAKAN"
        color = (0, 0, 255)      # Merah
    elif percentage < 5:
        status = "TAMBAH PAKAN"
        color = (255, 0, 0)      # Biru
    else:
        status = "STABIL"
        color = (0, 255, 0)      # Hijau

    # ===============================
    # TAMPILKAN DI LAYAR
    # ===============================
    cv2.putText(frame, f"Sisa Pakan: {percentage:.2f}%", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.putText(frame, f"STATUS: {status}", (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Kotak ROI
    cv2.rectangle(frame, (100, 200), (540, 450), (0, 255, 255), 2)

    cv2.imshow("Monitoring Tambak", frame)
    cv2.imshow("ROI", roi)
    cv2.imshow("Threshold", thresh)

    # ===============================
    # KIRIM STATUS KE SERVER (IoT)
    # ===============================
    current_time = time.time()
    if current_time - last_send > SEND_INTERVAL:
        try:
            requests.get(
                "http://localhost:5000/update",
                params={
                    "status": status,
                    "percentage": percentage
                },
                timeout=0.3
            )
        except:
            pass  # server belum jalan → tidak crash

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
