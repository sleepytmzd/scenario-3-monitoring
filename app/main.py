import asyncio
import random
from time import perf_counter
from typing import Dict

import psutil
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, Gauge, generate_latest

app = FastAPI(title="Demo Observability App")

cpu_usage_gauge = Gauge("app_cpu_usage_percent", "Application CPU usage percentage")
memory_usage_gauge = Gauge("app_memory_usage_percent", "Application memory usage percentage")
response_time_gauge = Gauge("app_response_time_ms", "Mock response time in milliseconds")

health_state: Dict[str, bool] = {"healthy": True}


async def update_resource_metrics() -> None:
    while True:
        cpu_usage_gauge.set(psutil.cpu_percent(interval=None))
        memory_usage_gauge.set(psutil.virtual_memory().percent)
        response_time_gauge.set(random.uniform(80.0, 220.0))
        await asyncio.sleep(5)


@app.on_event("startup")
async def startup_event() -> None:
    asyncio.create_task(update_resource_metrics())


@app.get("/")
async def root() -> Dict[str, str]:
    simulated_latency = random.uniform(0.05, 0.25)
    start = perf_counter()
    await asyncio.sleep(simulated_latency)
    duration_ms = (perf_counter() - start) * 1000
    response_time_gauge.set(duration_ms)
    return {"message": "FastAPI demo service", "response_time_ms": f"{duration_ms:.2f}"}


@app.get("/health")
async def health() -> JSONResponse:
    status = 200 if health_state["healthy"] else 503
    body = {"status": "ok" if health_state["healthy"] else "unhealthy"}
    return JSONResponse(content=body, status_code=status)


@app.post("/health/toggle")
async def toggle_health() -> Dict[str, bool]:
    health_state["healthy"] = not health_state["healthy"]
    return {"healthy": health_state["healthy"]}


@app.get("/metrics")
async def metrics() -> Response:
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)