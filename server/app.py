from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

status_pakan = "STABIL"
percentage_pakan = 0.0

@app.route("/update")
def update():
    global status_pakan, percentage_pakan
    status_pakan = request.args.get("status", status_pakan)
    percentage_pakan = float(request.args.get("percentage", percentage_pakan))
    return {"status": status_pakan, "percentage": percentage_pakan}

@app.route("/data")
def data():
    return jsonify({
        "status": status_pakan,
        "percentage": percentage_pakan
    })

@app.route("/")
def dashboard():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
