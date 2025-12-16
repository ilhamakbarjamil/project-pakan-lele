import cv2
import time

def test_camera(index, name):
    print(f"\nTesting {name} (index {index})...")
    cap = cv2.VideoCapture(index)
    
    if not cap.isOpened():
        print(f"❌ {name} tidak terbuka")
        return False
    
    # Baca beberapa frame untuk memastikan stabil
    for i in range(5):
        ret, frame = cap.read()
        if not ret:
            print(f"❌ Frame {i+1} gagal dibaca")
            break
        print(f"✅ Frame {i+1} berhasil - Resolusi: {frame.shape[1]}x{frame.shape[0]}")
    
    # Tampilkan preview 2 detik
    if ret:
        cv2.imshow(f'Preview {name}', frame)
        cv2.waitKey(2000)
        cv2.imwrite(f'preview_{name.lower().replace(" ", "_")}.jpg', frame)
        print(f"📸 Screenshot disimpan sebagai preview_{name.lower().replace(' ', '_')}.jpg")
    
    cap.release()
    cv2.destroyAllWindows()
    return True

if __name__ == "__main__":
    print("=== TEST SEMUA KAMERA ===")
    
    # Test kamera internal dulu
    test_camera(0, "Kamera Internal 0")
    test_camera(1, "Kamera Internal 1")
    
    # Test kamera eksternal
    test_camera(2, "Kamera Eksternal 2")
    test_camera(3, "Kamera Eksternal 3")
    
    print("\n=== HASIL TEST ===")
    print("1. Buka file screenshot untuk melihat hasil")
    print("2. Pilih index yang menghasilkan gambar terbaik")
    print("3. Gunakan index tersebut di kode utama")