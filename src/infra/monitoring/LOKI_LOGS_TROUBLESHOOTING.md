# The "WHERE & WHAT" Observability Pillar: Loki Logs Troubleshooting Manual

This guide provides a diagnostic workflow for troubleshooting FastAPI log delivery failures to **Grafana Loki** via the **OpenTelemetry Collector**, structured around Observability Pillars.

---

## 1. Observability Context: Navigating the Three Pillars

Observability rests on three foundational pillars that answer distinct questions during system analysis and incident response:

| Pillar | Primary Focus | Core Question Answered | Technology in Stack |
| :--- | :--- | :--- | :--- |
| **Metrics** | Aggregated time-series counts, rates & gauges | **WHEN** is something degrading? **HOW MUCH** traffic or error rate? | Prometheus |
| **Traces** | End-to-end request flow & span latencies | **WHICH** service, endpoint, or query causes the bottleneck? | Jaeger |
| **Logs** | Discrete event records, structured attributes & stack traces | **WHERE** (exact line/file/context) and **WHAT** went wrong? | **Grafana Loki + OTel** |

When logs fail to reach Grafana Loki, the **"WHERE & WHAT"** pillar collapses, leaving engineers without context, stack traces, or function-level variables during an outage.

---

## 2. Telemetry Architecture for Logs

```
[ FastAPI Application (todo-app) ]
       │
       │ (OTLP gRPC :4317 - Python LoggingHandler)
       ▼
[ OTel Collector (web-otel-collector) ] ──(debug exporter)──► Container stdout
       │
       │ (OTLP HTTP :3100/otlp - otlphttp/loki exporter)
       ▼
[ Grafana Loki (loki:3100) ]
       │
       │ (LogQL HTTP API :3100)
       ▼
[ Grafana UI (Explore / Dashboards) ]
```

---

## 3. The 5-Level Log Diagnostic Workflow

### Level 1: Python FastAPI Application & OpenTelemetry SDK
*Focus: Is the application capturing logs and attempting OTLP export?*

#### Common Failure Modes
1. **Host/DNS Resolution Failure for OTLP Collector Endpoint**:
   - Error signature: `address lookup failed for web-otel-collector:4317: DNS server returned general failure`.
   - **Running locally outside Docker**: Local host OS cannot resolve container service name `web-otel-collector`. Fix: Set `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317`.
   - **Running inside Docker**: Container `web-otel-collector` is down or not on `todo_network`. Fix: Run `docker compose up -d web-otel-collector`.
2. **Silent Failure in Log Handler Initialization**:
   - [`app/core/logger.py`](../../app/core/logger.py) wraps OTel setup in a `try...except` block. Missing dependencies (`opentelemetry-exporter-otlp-proto-grpc`) fail silently without crashing app startup.
3. **Missing Root Logger Attachment**:
   - Verify `otel_handler = LoggingHandler(...)` is attached via `root_logger.addHandler(otel_handler)`.

#### Verification Commands
```bash
# Check app logs for OpenTelemetry warnings/errors
docker logs todo_app | grep -i "opentelemetry"

# Check environment variables inside app container
docker exec todo_app env | grep OTEL

# Test connectivity from FastAPI container to OTel Collector
docker exec todo_app nc -zv web-otel-collector 4317
```

---

### Level 2: OTel Collector YAML Configuration ([`otel-config.yaml`](./otel-config.yaml))
*Focus: Is the OTel Collector configured with valid receivers, exporters, and pipelines?*

#### Common Failure Modes
1. **Unknown Exporter Type (`loki`)**:
   - Error: `unknown exporter type "loki"`.
   - Cause: The legacy `loki` exporter is deprecated/absent in standard builds.
   - Fix: Use `otlphttp/loki` exporter pointing to Loki's native OTLP endpoint `http://loki:3100/otlp`.
2. **OTel Pipeline Exporters List**:
   - [`otel-config.yaml`](./otel-config.yaml) `service.pipelines.logs` must include `otlphttp/loki`:
     ```yaml
     exporters:
       otlphttp/loki:
         endpoint: "http://loki:3100/otlp"
         tls:
           insecure: true

     service:
       pipelines:
         logs:
           receivers: [otlp]
           processors: [batch]
           exporters: [otlphttp/loki, debug]
     ```

#### Verification Commands
```bash
# Test Loki readiness endpoint
curl -s http://localhost:3100/ready

# Test Loki OTLP endpoint HTTP response
curl -i http://localhost:3100/otlp/v1/logs
```

---

### Level 3: OTel Collector Runtime & Export Delivery
*Focus: Is the collector running stably and successfully forwarding logs to Loki?*

#### Common Failure Modes
1. **Collector Crash Loops / Image Mismatch**:
   - Standard `otel/opentelemetry-collector` image lacks extended exporters. Ensure [`docker-compose.yml`](../../docker-compose.yml) uses `otel/opentelemetry-collector-contrib:latest`.
2. **Transient Connection Retries**:
   - Retries and backoffs when Loki is temporarily unreachable or restarting.
3. **Debug Exporter Verification**:
   - Standard stdout debug output in collector container logs confirms raw log records were received by the collector.

#### Verification Commands
```bash
# View live OTel Collector container logs (confirm debug log exports)
docker logs web-otel-collector --tail 100 -f

# Check container status and exit codes
docker ps -a --filter "name=web-otel-collector"
```

---

### Level 4: Grafana Datasource Health ("Grafana is Sad")
*Focus: Can Grafana connect to Loki to query log streams?*

#### Common Failure Modes
1. **Datasource URL Mismatch**:
   - [`grafana-datasources.yml`](./grafana-datasources.yml) must use internal Docker URL `http://loki:3100`, NOT `http://localhost:3100`.
   ```yaml
   datasources:
     - name: Loki
       type: loki
       access: proxy
       url: http://loki:3100
   ```
2. **Network Isolation**:
   - Grafana and Loki must both belong to `todo_network`.

#### Verification Commands
```bash
# Verify Grafana container can reach Loki
docker exec grafana curl -s http://loki:3100/ready

# Check Grafana datasource initialization logs
docker logs grafana | grep -i "datasource"
```

---

### Level 5: Grafana Explore Querying (LogQL & Label Matching)
*Focus: Are you querying Loki with the correct syntax, labels, and time window?*

#### Common Failure Modes
1. **Label Matcher Mismatch under OTLP Ingestion**:
   - Under `otlphttp`, Loki maps OTLP resource attributes to Loki labels automatically (`service.name` -> `service_name`).
   - **Correct Query**:
     ```logql
     {service_name="todo-app"}
     ```
2. **Time Window Outside Range**:
   - Ensure the time picker in Grafana Explore is set to "Last 15 minutes" or "Last 1 hour".
3. **No Generated Traffic**:
   - Generate test HTTP requests to trigger application log entries:
     ```bash
     curl http://localhost:8000/docs
     ```

#### Verification Commands
```bash
# Fetch indexed Loki labels via API
curl -s http://localhost:3100/loki/api/v1/labels | jq

# Direct LogQL search via Loki HTTP API
curl -G -s "http://localhost:3100/loki/api/v1/query_range" \
  --data-urlencode 'query={service_name="todo-app"}' | jq
```

---

## 4. Current Codebase Configuration Summary

| Component | Codebase State | Verified Status |
| :--- | :--- | :--- |
| **Observability Pillar** | Logs (WHERE & WHAT context) via OTel + Loki | ✅ Active |
| **OTel Collector Image** | `otel/opentelemetry-collector-contrib:latest` | ✅ Validated |
| **App OTLP Endpoint** | `OTEL_EXPORTER_OTLP_ENDPOINT=http://web-otel-collector:4317` | ✅ Configured |
| **Collector Exporter** | `otlphttp/loki` (`http://loki:3100/otlp`) | ✅ Updated & Verified |
| **Grafana Provisioning** | Datasource `Loki` -> `http://loki:3100` | ✅ Verified |
| **End-to-End Delivery** | FastAPI -> OTel Collector -> Loki -> Grafana Explore | ✅ Verified |
