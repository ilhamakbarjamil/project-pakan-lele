import cv2
import numpy as np

# ===============================
# FUNGSI: Mode Kalibrasi HSV
# ===============================
def mode_kalibrasi():
    def nothing(x):
        pass

    cap = cv2.VideoCapture(0)

    cv2.namedWindow("Trackbars")

    cv2.createTrackbar("L-H", "Trackbars", 0, 179, nothing)
    cv2.createTrackbar("L-S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("L-V", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("U-H", "Trackbars", 179, 179, nothing)
    cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing)

    print("\n=== MODE KALIBRASI ===")
    print("Gerakkan slider untuk mencari warna pakan.")
    print("Tekan Q untuk keluar.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        l_h = cv2.getTrackbarPos("L-H", "Trackbars")
        l_s = cv2.getTrackbarPos("L-S", "Trackbars")
        l_v = cv2.getTrackbarPos("L-V", "Trackbars")
        u_h = cv2.getTrackbarPos("U-H", "Trackbars")
        u_s = cv2.getTrackbarPos("U-S", "Trackbars")
        u_v = cv2.getTrackbarPos("U-V", "Trackbars")

        lower = np.array([l_h, l_s, l_v])
        upper = np.array([u_h, u_s, u_v])

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
    # GANTI NILAI INI sesuai hasil kalibrasi!
    h_min, s_min, v_min = 5, 50, 50
    h_max, s_max, v_max = 30, 255, 255

    THRESHOLD_SISA_PAKAN = 0.05  # 0.05% piksel

    cap = cv2.VideoCapture(0)

    print("\n=== MODE DETEKSI PAKAN ===")
    print("Tekan Q untuk keluar.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        mask = cv2.inRange(hsv, lower, upper)

        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        total_pixels = frame.shape[0] * frame.shape[1]
        feed_pixels = cv2.countNonZero(mask)
        percentage = (feed_pixels / total_pixels) * 100

        # Pengambilan keputusan
        if percentage > THRESHOLD_SISA_PAKAN:
            decision = "SISA PAKAN BANYAK"
            servo_cmd = "0"
        else:
            decision = "SISA PAKAN SEDIKIT"
            servo_cmd = "90"

        # Tampilkan di frame
        cv2.putText(frame, f"Pakan: {percentage:.4f}%", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, decision, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Perintah Servo: {servo_cmd}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow("Deteksi Pakan", frame)
        cv2.imshow("Mask Pakan", mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# ===============================
# PROGRAM UTAMA
# ===============================
print("\n=== SISTEM DETEKSI PAKAN LELE ===")
print("1. Kalibrasi warna pakan (HSV)")
print("2. Jalankan deteksi sisa pakan\n")

pilih = input("Pilih mode (1/2): ")

if pilih == "1":
    mode_kalibrasi()
elif pilih == "2":
    mode_deteksi()
else:
    print("Pilihan tidak valid!")
