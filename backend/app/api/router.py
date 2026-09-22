from fastapi import APIRouter

from app.api.endpoints import companies, health, relationships

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(companies.router)
api_router.include_router(relationships.router)
