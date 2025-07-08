from flask import Flask, request, Response
from prometheus_client import Counter, Histogram, generate_latest
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

    # Simulate processing time
    sleep_time = random.uniform(0.1, 1.0)
    time.sleep(sleep_time)

    # Simulate random error
    if random.random() < 0.2:
        status_code = 500
        response = "Internal Server Error", 500
    else:
        status_code = 200
        response = "Hello from my-python-app!"

    # Observe metrics
    REQUESTS_TOTAL.labels(method=request.method, endpoint='/', http_status=status_code).inc()
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start_time)

    return response

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
