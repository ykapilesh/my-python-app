from flask import Flask
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

REQUESTS = Counter('my_python_app_requests_total', 'Total HTTP requests')

@app.route('/')
def hello():
    REQUESTS.inc()
    return "Hello from my-python-app!"

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
