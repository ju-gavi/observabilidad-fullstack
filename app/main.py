from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics
import logging
import sys
import os

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# ✅ Crear el directorio de logs si no existe
log_dir = "/var/log/flask"
os.makedirs(log_dir, exist_ok=True)

# ✅ Configurar logger personalizado
logger = logging.getLogger("custom-logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    # Log a archivo (Loki lo recogerá)
    file_handler = logging.FileHandler(f"{log_dir}/app.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Log a consola (kubectl logs)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

logger.info("🟢 Logger inicializado correctamente")

# ✅ Configurar OpenTelemetry Tracing
resource = Resource(attributes={"service.name": "flask"})
tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)

otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces")
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)

# ✅ Crear la app Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app, tracer_provider=tracer_provider)

# ✅ Exponer métricas Prometheus
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Aplicación Flask instrumentada", version="1.0.0")

tracer = trace.get_tracer(__name__)

@app.route("/hello")
def hello():
    logger.info("👋 Endpoint /hello llamado")
    with tracer.start_as_current_span("hello-handler"):
        return "Hello from Flask!"

@app.route("/error")
def error():
    logger.error("💥 Endpoint /error activado")
    with tracer.start_as_current_span("error-handler"):
        raise Exception("Simulated error for observability demo")

if __name__ == "__main__":
    logger.info("✅ Flask iniciado desde __main__")
    app.run(host="0.0.0.0", port=5000)
