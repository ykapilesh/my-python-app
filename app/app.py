from flask import Flask, request, Response
from prometheus_client import Counter, Histogram, generate_latest
import threading
import requests
import random
import time

app = Flask(__name__)

# Metrics
REQUESTS_TOTAL = Counter(
    'http_requests_total', 
    'Total HTTP requests',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['endpoint']
)

@app.route('/')
def hello():
    start_time = time.time()

    sleep_time = random.uniform(0.1, 1.0)
    time.sleep(sleep_time)

    if random.random() < 0.2:
        status_code = 500
        response = "Internal Server Error", 500
    else:
        status_code = 200
        response = "Hello from my-python-app!"

    REQUESTS_TOTAL.labels(method=request.method, endpoint='/', http_status=status_code).inc()
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start_time)

    return response

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

def periodic_curl():
    """Function that runs periodically to 'curl' the own app."""
    while True:
        try:
            resp = requests.get("http://localhost:5000/")
            print(f"Periodic call: status {resp.status_code}")
        except Exception as e:
            print(f"Periodic call failed: {e}")
        time.sleep(10)  # run every 10 sec

# Start background thread
threading.Thread(target=periodic_curl, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
