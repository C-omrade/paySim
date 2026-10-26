from fastapi import APIRouter, status

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    return {
        "status": "Healthy",
        "service": "paySim_monitoring_fastAPI"
    }