from flask import Flask, Response, render_template, jsonify
import cv2
import threading
import time
from camera import FishFeederCamera

app = Flask(__name__)
camera = FishFeederCamera()
status_data = {"percentage": 0.0, "status": "STABIL"}

def update_status():
    """Thread untuk update status secara berkala"""
    global status_data
    while True:
        try:
            camera.process_frame()
            status_data = camera.get_status()
        except Exception as e:
            print(f"Error processing frame: {str(e)}")
        time.sleep(0.5)

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            frame = camera.process_frame()
            if frame is not None:
                _, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.1)
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Endpoint baru untuk threshold
@app.route('/threshold_feed')
def threshold_feed():
    def generate():
        while True:
            threshold_frame = camera.get_threshold_frame()
            if threshold_frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + threshold_frame + b'\r\n')
            time.sleep(0.1)
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def data():
    return jsonify(status_data)

if __name__ == '__main__':
    # Jalankan thread untuk update status
    status_thread = threading.Thread(target=update_status, daemon=True)
    status_thread.start()
    
    # Jalankan Flask
    app.run(host='0.0.0.0', port=5000, threaded=True)