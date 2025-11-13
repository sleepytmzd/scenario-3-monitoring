# Observability Monitoring Setup

This project provides a lightweight observability stack for monitoring a local FastAPI web service running in Docker. The setup collects CPU usage, memory consumption, and response-time metrics, visualizes them in Grafana, and triggers Prometheus alerts when CPU usage exceeds 70% or the app becomes unhealthy.

## Project Structure

```
observability-monitoring
├── app
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── config
│   ├── grafana
│   │   ├── dashboards
│   │   │   └── observability-dashboard.json
│   │   └── provisioning
│   │       ├── dashboards
│   │       │   └── dashboards.yaml
│   │       └── datasources
│   │           └── prometheus.yaml
│   └── prometheus
│       ├── alert_rules.yml
│       └── prometheus.yml
├── docker-compose.yml
├── scripts
│   └── alert_dispatcher.sh
└── README.md
```

## Components

- **FastAPI Demo App** (`app/`): Exposes `/`, `/health`, and `/metrics` endpoints with Prometheus-compatible metrics.
- **Prometheus** (`config/prometheus/`): Scrapes the demo app, Node Exporter, and itself. Includes alert rules for CPU saturation and app availability.
- **Node Exporter**: Collects basic host metrics for Prometheus.
- **Grafana** (`config/grafana/`): Preconfigured data source and dashboard for visualizing app metrics.
- **Alert Dispatcher Script** (`scripts/alert_dispatcher.sh`): Fetches active alerts from Prometheus and logs them locally.

## Getting Started

```bash
# from the project root
docker-compose up -d
```

- FastAPI app: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default credentials: admin / admin)

Grafana automatically loads the bundled dashboard. Trigger alerts by stressing the app (e.g., repeated requests) or toggling health via `POST http://localhost:8000/health/toggle`.

## Alert Logging (Bonus)

```bash
bash scripts/alert_dispatcher.sh
```

Logs are written to `logs/prometheus-alerts.log`.

## Screenshot

After metrics appear, capture a Grafana dashboard screenshot showing the charts and any active alert to satisfy the deliverable.