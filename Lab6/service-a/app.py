from flask import Flask, jsonify
import os, time

app = Flask(__name__)
SERVICE_NAME = os.getenv("SERVICE_NAME", "service-a")
PORT = int(os.getenv("PORT", 9000))
START_TIME = time.time()

@app.route("/")
def index():
    return jsonify({
        "service": SERVICE_NAME,
        "status": "running",
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "note": "This service is PRIVATE — accessible only via API Gateway on port 8000"
    })

@app.route("/data")
def data():
    return jsonify({
        "service": SERVICE_NAME,
        "data": ["record-1", "record-2", "record-3"],
        "lab": "LAB6 - Microservice Exposure Control"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
