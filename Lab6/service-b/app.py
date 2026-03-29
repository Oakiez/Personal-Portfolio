from flask import Flask, jsonify
import os, time

app = Flask(__name__)
SERVICE_NAME = os.getenv("SERVICE_NAME", "service-b")
PORT = int(os.getenv("PORT", 9001))
START_TIME = time.time()

@app.route("/")
def index():
    return jsonify({
        "service": SERVICE_NAME,
        "status": "running",
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "note": "This service is PRIVATE — accessible only via API Gateway on port 8000"
    })

@app.route("/status")
def status():
    return jsonify({
        "service": SERVICE_NAME,
        "network": "LAN-A (192.168.10.0/24)",
        "reachable_via": "API Gateway → port 8000 only",
        "backend_port_9001": "blocked by NAT — not reachable from Internet"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
