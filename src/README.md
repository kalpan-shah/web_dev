# Todo APP - Template 
Last Updated: May 14, 2026

### Setup
1. Install uv
2. Install requirements
    ```bash
    cd src
    uv sync
    ```
3. Rename the .env.template to .env and update variables accordingly

### Run
`uv run uvicorn app.main:app --reload --reload-dir ./app`

### Run Tests
`pytest`

### Data Migrations
- Note: PostgreSQL Only and Not yet tested

`pg_dump -Fc -v -d "SOURCE_DB_CONN_STRING" | pg_restore -v --no-owner --no-privileges -d "TARGET_DB_CONN_STRING"
`

### Load Testing 
1. Independent headless
`uv run locust -f ./tests/load/locustfile.py --headless -u 50 -r 5 -t 2m -H http://127.0.0.1:8000`

**Command Flags:**
- `-f`: Path to locust file (`./tests/load/locustfile.py`)
- `--headless`: Run in CLI mode without web UI
- `-u`: Number of concurrent users (`50`)
- `-r`: Spawn rate / users per second (`5`)
- `-t`: Test duration (`2m`)
- `-H`: Target host URL (`http://127.0.0.1:8000`)

2. Ft. Locust master
Given the locust master is running with docker

### Monitoring & Observability
For complete architecture and configuration details, see [`infra/monitoring/README.md`](./infra/monitoring/README.md).

| Service | Endpoint / Port | Description |
| :--- | :--- | :--- |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | Dashboards for Metrics & Logs (Loki) (User/Pass: `admin`/`admin`) |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | Metrics scraper & database |
| **Jaeger UI** | [http://localhost:16686](http://localhost:16686) | Distributed tracing UI |
| **Loki** | [http://localhost:3100](http://localhost:3100) | Log aggregation backend |
| **Locust Master** | [http://localhost:8089](http://localhost:8089) | Load testing dashboard |

#### Quick Start Monitoring:
```bash
docker compose up -d --build
```
Query logs in Grafana Explore using LogQL:
```logql
{service_name="todo-app"}
``` 