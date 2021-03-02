Prerequisites

```
pip install virtualenv
virtualenv opentelemetry-venv
source opentelemetry-venv/bin/activate
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-jaeger flask opentelemetry-instrumentation-flask opentelemetry-instrumentation-requests

docker run --rm -p 6831:6831/udp -p 6832:6832/udp -p 16686:16686 jaegertracing/all-in-one
```

Run these 2 in 2 separate terminals to start the 2 microservices.
1. python core.py
2. python orchestrator.py

Run this to do a sample request out.
`curl --location --request GET 'localhost:8080/create-node?token=123'`

`curl --location --request GET 'localhost:8080/create-node'` --> Invalid token.

View jaegar @ `http://localhost:16686/`

This program does the following
1. Client (Curl) calls core service using create-node?token=123.
2. Core-service authenticates this token using auth function.
3. Auth function calls db(simulated via sleep) to ensure 123 is a valid token and returns T or F.
4. If T, Core will call orch-service to 'deploy' a node via /deploy endpoint.
5. Orch service will call k8s to deploy (Simluated via sleep)
6. Once deployed, orch service will send 200 to core.
7. Core will send 200 to user.

The entire flow is depicted under the screenshot at the root of this repo.
