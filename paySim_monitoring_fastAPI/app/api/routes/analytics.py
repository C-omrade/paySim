from fastapi import APIRouter
from app.services.analytics import get_overview

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview")
def overview():
    return get_overview()