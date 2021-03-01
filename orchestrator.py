from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask import Flask
from flask import request
import requests
import time
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
# create a JaegerSpanExporter
jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name='orch-service',
    agent_host_name='localhost',
    agent_port=6831,
)
# Create a BatchExportSpanProcessor and add the exporter to it
span_processor = BatchExportSpanProcessor(jaeger_exporter)
# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)


def get_information_from_k8s():
    with tracer.start_as_current_span('k8s-information'):
        requests.get('http://www.google.com')


@app.route("/deploy")
def deploy_to_kubernetes():
    print("Starting operation.")
    with tracer.start_as_current_span('deploy-to-kubernetes') as span:
        print(span)
        print(request.headers)
        # Simulate 4 second of deployment.
        get_information_from_k8s()

        time.sleep(1.5)
        return "deployed_to_k8s", 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
