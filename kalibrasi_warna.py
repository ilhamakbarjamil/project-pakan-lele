import cv2
import numpy as np

# Fungsi callback untuk trackbar (tidak melakukan apa-apa)
def nothing(x):
    pass

# Ambil video dari kamera (0 adalah kamera default laptop)
cap = cv2.VideoCapture(0)

# Buat jendela untuk trackbar (slider)
cv2.namedWindow("Trackbars")

# Buat trackbar untuk mengatur batas warna HSV
cv2.createTrackbar("L-H", "Trackbars", 0, 179, nothing) # Lower Hue
cv2.createTrackbar("L-S", "Trackbars", 0, 255, nothing) # Lower Saturation
cv2.createTrackbar("L-V", "Trackbars", 0, 255, nothing) # Lower Value
cv2.createTrackbar("U-H", "Trackbars", 179, 179, nothing) # Upper Hue
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing) # Upper Saturation
cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing) # Upper Value

while True:
    # Baca frame dari kamera
    ret, frame = cap.read()
    if not ret:
        break
    
    # Konversi dari BGR ke HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Ambil nilai batas warna dari trackbar
    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")

    # Buat batas HSV
    lower_bound = np.array([l_h, l_s, l_v])
    upper_bound = np.array([u_h, u_s, u_v])

    # Buat mask (masker) untuk mengisolasi warna pakan
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Tampilkan hasil mask (hanya warna yang masuk rentang yang akan putih)
    cv2.imshow("Mask", mask)
    
    # Tampilkan video asli
    cv2.imshow("Original Frame", frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Setelah keluar, cetak rentang HSV terakhir yang Anda gunakan
print(f"Batas Bawah HSV: [{l_h}, {l_s}, {l_v}]")
print(f"Batas Atas HSV: [{u_h}, {u_s}, {u_v}]")

cap.release()
cv2.destroyAllWindows()