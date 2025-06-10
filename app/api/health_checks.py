from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.endpoint import Endpoint
from app.models.health_check import HealthCheck
from app.schemas.health_check import HealthCheckOut
from app.core.health_check_scheduler import perform_health_check

router = APIRouter()

@router.get("/{endpoint_id}/check", response_model=HealthCheckOut)
async def manual_check(endpoint_id: int, db: AsyncSession = Depends(get_db)):
    ep = await db.get(Endpoint, endpoint_id)
    if not ep:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    await perform_health_check(ep, db)
    result = await db.execute(
        select(HealthCheck).where(HealthCheck.endpoint_id == endpoint_id).order_by(HealthCheck.check_time.desc()).limit(1)
    )
    latest_check = result.scalars().first()
    if not latest_check:
        raise HTTPException(status_code=404, detail="No health check found")
    return HealthCheckOut.model_validate(latest_check)

@router.get("/{endpoint_id}/history", response_model=List[HealthCheckOut])
async def get_health_history(endpoint_id: int, limit: int = 20, db: AsyncSession = Depends(get_db)):
    ep = await db.get(Endpoint, endpoint_id)
    if not ep:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    query = await db.execute(
        select(HealthCheck).where(HealthCheck.endpoint_id == endpoint_id).order_by(HealthCheck.check_time.desc()).limit(limit)
    )
    return query.scalars().all()
