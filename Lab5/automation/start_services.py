#!/usr/bin/env python3
"""
LAB 5 — Week03 Microservices Launcher
Starts all 4 services: Upload(8000), Processing(8001), AI(8002), Gateway(9000)
"""
import subprocess
import sys
import time
import os
import signal

SERVICES = [
    {"name": "Upload Service",      "module": "upload_service:app",     "port": 8000},
    {"name": "Processing Service",  "module": "processing_service:app", "port": 8001},
    {"name": "AI Service",          "module": "ai_service:app",         "port": 8002},
    {"name": "Gateway Service",     "module": "gateway_service:app",    "port": 9000},
]

processes = []

def start_service(service):
    cmd = [
        sys.executable, "-m", "uvicorn",
        service["module"],
        "--host", "0.0.0.0",
        "--port", str(service["port"]),
        "--log-level", "info"
    ]
    print(f"[START] {service['name']} on port {service['port']}")
    proc = subprocess.Popen(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
    return proc

def shutdown(sig, frame):
    print("\n[STOP] Shutting down all services...")
    for p in processes:
        p.terminate()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    print("=" * 55)
    print("  LAB 5 — Microservices Stack (Week03 Integration)")
    print("=" * 55)

    for svc in SERVICES:
        proc = start_service(svc)
        processes.append(proc)
        time.sleep(0.5)

    print("\n[OK] All services started:")
    print(f"  Upload Service      → http://0.0.0.0:8000")
    print(f"  Processing Service  → http://0.0.0.0:8001")
    print(f"  AI Service          → http://0.0.0.0:8002")
    print(f"  Gateway Service     → http://0.0.0.0:9000")
    print("\n  Press Ctrl+C to stop all services.\n")

    # Wait for all
    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        shutdown(None, None)
