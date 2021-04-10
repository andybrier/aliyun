import prometheus_client
from prometheus_client import Counter
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

app = Flask(__name__)

requests_total = Counter("request_count", "Total request cout of the host")

@app.route("/error")
def requests_count():

    registry = CollectorRegistry()
    g = Gauge('host_error', 'Host Error Happened', ['host'], registry=registry)
    g.labels('www.huawei.com').set(1)
    push_to_gateway('127.0.0.1:9091', job='batchA', registry=registry)  
  
    return "ok"

@app.route('/')
def index():
    requests_total.inc()
    return "Hello World"

if __name__ == "__main__":
    app.run(host="0.0.0.0")