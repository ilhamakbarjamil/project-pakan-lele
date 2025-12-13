import cv2
import numpy as np

class FishFeederCamera:
    def __init__(self, camera_id=0):
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise RuntimeError(f"Kamera tidak terdeteksi di index {camera_id}!")
        self.latest_frame = None
        self.latest_percentage = 0.0
        self.latest_status = "STABIL"
        
    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Resize dan crop ROI
        frame = cv2.resize(frame, (640, 480))
        roi = frame[200:450, 100:540]
        
        # Image processing
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 160, 255, cv2.THRESH_BINARY)
        
        # Hitung persentase pakan
        white_area = cv2.countNonZero(thresh)
        total_area = thresh.shape[0] * thresh.shape[1]
        self.latest_percentage = (white_area / total_area) * 100
        
        # Tentukan status
        if self.latest_percentage > 20:
            self.latest_status = "STOP PAKAN"
            color = (0, 0, 255)
        elif self.latest_percentage < 5:
            self.latest_status = "TAMBAH PAKAN"
            color = (255, 0, 0)
        else:
            self.latest_status = "STABIL"
            color = (0, 255, 0)
        
        # Tambahkan teks dan kotak ROI
        cv2.putText(frame, f"Sisa Pakan: {self.latest_percentage:.2f}%", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, f"STATUS: {self.latest_status}", (10, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        cv2.rectangle(frame, (100, 200), (540, 450), (0, 255, 255), 2)
        
        # Simpan frame terbaru
        self.latest_frame = frame.copy()
        return frame
    
    def get_status(self):
        return {
            "percentage": self.latest_percentage,
            "status": self.latest_status
        }
    
    def release(self):
        self.cap.release()