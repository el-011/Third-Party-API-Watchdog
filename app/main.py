import asyncio
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import engine, Base, get_db
from app.core.health_check_scheduler import scheduled_health_checks
from app.api import endpoints, health_checks
from app.schemas.dashboard import DashboardEndpointStatus
from typing import List
from app.models.endpoint import Endpoint
from app.models.health_check import HealthCheck

app = FastAPI(title="Third-Party API Watchdog")

app.include_router(endpoints.router, prefix="/endpoints", tags=["endpoints"])
app.include_router(health_checks.router, prefix="/endpoints", tags=["health_checks"])

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    asyncio.create_task(scheduled_health_checks())

@app.get("/dashboard", response_model=List[DashboardEndpointStatus])
async def dashboard(db: AsyncSession = Depends(get_db)):
    endpoints = (await db.execute(select(Endpoint))).scalars().all()
    results = []
    for ep in endpoints:
        checks = (await db.execute(
            select(HealthCheck).where(HealthCheck.endpoint_id == ep.id).order_by(HealthCheck.check_time.desc()).limit(100)
        )).scalars().all()
        last_status = checks[0].status if checks else None
        last_checked = checks[0].check_time if checks else None
        uptime_percentage = (sum(1 for c in checks if c.status == "UP") / len(checks) * 100) if checks else None
        results.append(DashboardEndpointStatus(
            id=ep.id,
            url=ep.url,
            last_status=last_status,
            last_checked=last_checked,
            uptime_percentage=uptime_percentage
        ))
    return results
