Pre-requesites

```
pip install virtualenv
virtualenv opentelemetry-venv
source opentelemetry-venv/bin/activate
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-jaeger flask opentelemetry-instrumentation-flask opentelemetry-instrumentation-requests

docker run --rm -p 6831:6831/udp -p 6832:6832/udp -p 16686:16686 jaegertracing/all-in-one:1.13 --log-level=debugs
```

Run this to do a sample request out.
`curl --location --request GET 'localhost:8080/create-node?token=123'`
