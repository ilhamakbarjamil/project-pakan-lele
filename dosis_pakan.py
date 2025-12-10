import cv2
import numpy as np
import requests

# ==========================================================
# 1. KONFIGURASI JARINGAN (WAJIB DIGANTI!)
# ==========================================================
# GANTI IP INI dengan IP yang didapat dari Serial Monitor ESP32 Anda
ESP32_IP = "192.168.110.232" 
SERVO_URL = f"http://{ESP32_IP}/servo?pos="

# ===============================
# FUNGSI: Mode Kalibrasi HSV
# ===============================
def mode_kalibrasi():
    """
    Mode untuk mencari rentang warna HSV pakan ikan menggunakan slider.
    """
    def nothing(x):
        pass

    cap = cv2.VideoCapture(0)
    # Cek apakah kamera terbuka
    if not cap.isOpened():
        print("Error: Kamera tidak dapat diakses.")
        return

    cv2.namedWindow("Trackbars")

    # Batas Awal untuk Trackbar (sesuaikan agar mudah menemukan pakan)
    cv2.createTrackbar("L-H", "Trackbars", 0, 179, nothing)
    cv2.createTrackbar("L-S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("L-V", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("U-H", "Trackbars", 179, 179, nothing)
    cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing)

    print("\n=== MODE KALIBRASI ===")
    print("Gerakkan slider sampai pakan terlihat PUTIH di jendela 'Mask'.")
    print("Tekan Q untuk keluar dan mencetak hasilnya.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Ambil nilai dari trackbar
        l_h = cv2.getTrackbarPos("L-H", "Trackbars")
        l_s = cv2.getTrackbarPos("L-S", "Trackbars")
        l_v = cv2.getTrackbarPos("L-V", "Trackbars")
        u_h = cv2.getTrackbarPos("U-H", "Trackbars")
        u_s = cv2.getTrackbarPos("U-S", "Trackbars")
        u_v = cv2.getTrackbarPos("U-V", "Trackbars")

        lower = np.array([l_h, l_s, l_v])
        upper = np.array([u_h, u_s, u_v])

        # Masking: Isolasi warna pakan
        mask = cv2.inRange(hsv, lower, upper)

        cv2.imshow("Mask", mask)
        cv2.imshow("Original Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("\n=== HASIL KALIBRASI ===")
    print(f"Lower HSV = [{l_h}, {l_s}, {l_v}]")
    print(f"Upper HSV = [{u_h}, {u_s}, {u_v}]")
    print("=======================\n")

    cap.release()
    cv2.destroyAllWindows()


# ===============================
# FUNGSI: Mode Deteksi Sisa Pakan
# ===============================
def mode_deteksi():
    """
    Mode untuk menjalankan deteksi sisa pakan, mengambil keputusan,
    dan mengirim perintah ke ESP32 via HTTP.
    """
    # GANTI NILAI INI DENGAN HASIL KALIBRASI NYATA ANDA
    # Contoh untuk pakan cokelat yang umum:
    h_min, s_min, v_min = 5, 50, 50 
    h_max, s_max, v_max = 30, 255, 255

    # Ambang batas persentase piksel pakan. Sesuaikan sesuai pengujian!
    THRESHOLD_SISA_PAKAN = 0.05  # 0.05% dari total piksel.

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Kamera tidak dapat diakses.")
        return

    print(f"\n=== MODE DETEKSI PAKAN AKTIF: Menghubungi ESP32 di {ESP32_IP} ===")
    print(f"Ambang Batas Sisa Pakan: {THRESHOLD_SISA_PAKAN}%")
    print("Tekan Q untuk keluar.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 1. Pemrosesan Citra
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        mask = cv2.inRange(hsv, lower, upper)

        # Membersihkan noise (Erode & Dilate)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # 2. Analisis Piksel
        total_pixels = frame.shape[0] * frame.shape[1]
        feed_pixels = cv2.countNonZero(mask)
        percentage = (feed_pixels / total_pixels) * 100

        # 3. Pengambilan Keputusan Otomatis
        if percentage > THRESHOLD_SISA_PAKAN:
            decision = "SISA PAKAN BANYAK: JANGAN BERI PAKAN"
            servo_cmd = "0"  # Perintah Tutup
        else:
            decision = "SISA PAKAN SEDIKIT: BERI PAKAN"
            servo_cmd = "90" # Perintah Buka (Contoh Dosis Pakan)

        # 4. Pengiriman Perintah ke ESP32 (Simulasi IoT)
        try:
            full_url = SERVO_URL + servo_cmd
            response = requests.get(full_url, timeout=0.5) 
            status_text = f"CMD Sent: {servo_cmd} | Status: {response.status_code}"
        except requests.exceptions.RequestException:
            status_text = "ERROR: Gagal koneksi ke ESP32!"

        # 5. Tampilkan Hasil
        cv2.putText(frame, f"Pakan: {percentage:.4f}%", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, decision, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, status_text, (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)


        cv2.imshow("Deteksi Pakan", frame)
        cv2.imshow("Mask Pakan", mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# ===============================
# PROGRAM UTAMA: Pemilihan Mode
# ===============================
if __name__ == "__main__":
    print("\n=== SISTEM DETEKSI PAKAN IKAN CERDAS ===")
    print("1. Kalibrasi warna pakan (HSV)")
    print("2. Jalankan deteksi sisa pakan dan kontrol Servo (IoT)")
    print("========================================")

    pilih = input("Pilih mode (1/2): ")

    if pilih == "1":
        mode_kalibrasi()
    elif pilih == "2":
        mode_deteksi()
    else:
        print("Pilihan tidak valid!")