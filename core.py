import time

from flask import Flask, request
from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.propagators import inject
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from requests import get

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
# create a JaegerSpanExporter
jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name='core-service',
    agent_host_name='localhost',
    agent_port=6831,
)
# Create a BatchExportSpanProcessor and add the exporter to it
span_processor = BatchExportSpanProcessor(jaeger_exporter)
# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)


def authenticate_token(token):
    with tracer.start_as_current_span('authenticate-token'):
        print('authenticating token')
        time.sleep(0.5)  # Simulate database call.
        if token == '123':
            return True
        return False


def deploy_to_orch():
    with tracer.start_as_current_span('deploy-to-orch') as span:
        headers = {}
        inject(dict.__setitem__, headers)
        print(span)
        print(headers)
        requested = get(
            "http://localhost:8081/deploy",
            headers=headers,
        )
        span.set_attribute("http.route", "/orch/deploy")


def update_database():
    with tracer.start_as_current_span('update-node-in-db'):
        time.sleep(1)


@app.route("/create-node")
def create_node():
    print("Starting operation.")
    with tracer.start_as_current_span('node-creation'):
        token = request.args.get('token')
        if not authenticate_token(token):
            return "Wrong Token!", 401

        try:
            deploy_to_orch()
        except Exception as e:
            print(e)
            return "Error in deploying to orchestrator", 401

        update_database()
        return "deployed", 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
