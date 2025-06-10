import asyncio
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
import json
from app.core.validation import validate_response_contract
from app.models.endpoint import Endpoint
from app.models.health_check import HealthCheck
from app.core.database import AsyncSessionLocal

async def perform_health_check(endpoint: Endpoint, db: AsyncSession):
    async with httpx.AsyncClient(timeout=10.0) as client:
        start_time = datetime.utcnow()
        status = "DOWN"
        error_message = None
        response_time_ms = None
        status_code = None
        try:
            response = await client.get(endpoint.url)
            status_code = response.status_code
            response_time_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            if status_code == endpoint.expected_status_code:
                if endpoint.expected_response_schema:
                    try:
                        json_data = response.json()
                        valid = await validate_response_contract(json_data, json.loads(endpoint.expected_response_schema))
                        if valid:
                            status = "UP"
                        else:
                            status = "CONTRACT_BROKEN"
                    except Exception as e:
                        status = "CONTRACT_BROKEN"
                        error_message = f"Invalid JSON or contract validation error: {str(e)}"
                else:
                    status = "UP"
            else:
                status = "DOWN"
                error_message = f"Expected status {endpoint.expected_status_code}, got {status_code}"
        except Exception as e:
            error_message = str(e)

        health_check = HealthCheck(
            endpoint_id=endpoint.id,
            status_code=status_code,
            response_time_ms=response_time_ms,
            check_time=datetime.utcnow(),
            status=status,
            error_message=error_message
        )
        db.add(health_check)
        await db.commit()

async def scheduled_health_checks():
    while True:
        async with AsyncSessionLocal() as db:
            endpoints = (await db.execute(select(Endpoint))).scalars().all()
            tasks = [perform_health_check(ep, db) for ep in endpoints]
            await asyncio.gather(*tasks)
        await asyncio.sleep(300)
