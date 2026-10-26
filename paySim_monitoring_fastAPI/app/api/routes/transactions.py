import os
import secrets

from fastapi import APIRouter, Depends, HTTPException, status, Header

from app.schemas.transaction import TransactionEvent
from app.services.analytics import record_event

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/transactions", status_code=status.HTTP_201_CREATED)
def receive_transaction_event(
    event: TransactionEvent,
    x_monitoring_key: str = Header(),
):
    api_key = os.getenv("MONITORING_API_KEY")
    if not api_key or x_monitoring_key != api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

    if not record_event(event):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Transaction event already exists",
        )
    accepted = record_event(event)

    return {
        "received": True,
        "duplicate": not accepted,
        "transaction_id": event.transaction_id,
    }