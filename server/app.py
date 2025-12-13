from flask import Flask, request

app = Flask(__name__)

status_pakan = "STABIL"

@app.route("/update")
def update():
    global status_pakan
    status_pakan = request.args.get("value", "STABIL")
    print("STATUS DARI KAMERA:", status_pakan)
    return {"status": status_pakan}

@app.route("/status")
def status():
    return {"status": status_pakan}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
