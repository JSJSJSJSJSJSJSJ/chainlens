from fastapi import APIRouter

from app.api.dependencies import Service

router = APIRouter()


@router.get("/api/health")
def health(svc: Service):
    return svc.health()
