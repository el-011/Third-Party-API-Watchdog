from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json

from app.core.database import get_db
from app.models.endpoint import Endpoint
from app.schemas.endpoint import EndpointCreate, EndpointOut

router = APIRouter()

@router.post("/", response_model=EndpointOut, status_code=status.HTTP_201_CREATED)
async def register_endpoint(endpoint: EndpointCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Endpoint).where(Endpoint.url == endpoint.url))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Endpoint URL already registered")
    ep = Endpoint(
        url=endpoint.url,
        expected_status_code=endpoint.expected_status_code,
        expected_response_schema=json.dumps(endpoint.expected_response_schema) if endpoint.expected_response_schema else None
    )
    db.add(ep)
    await db.commit()
    await db.refresh(ep)
    return ep
