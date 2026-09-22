from datetime import date

from fastapi import APIRouter

from app.api.dependencies import Service

router = APIRouter()


@router.get("/api/relationships/{relationship_id}")
def relationship(relationship_id: str, svc: Service, known_at: date | None = None):
    return svc.relationship(relationship_id, known_at)


@router.get("/api/relationships/{relationship_id}/evidence")
def evidence(relationship_id: str, svc: Service, known_at: date | None = None):
    return svc.evidence(relationship_id, known_at)
