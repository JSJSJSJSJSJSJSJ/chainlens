from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import Filters, Service

router = APIRouter()


@router.get("/api/companies")
def companies(
    svc: Service,
    q: Annotated[str | None, Query(max_length=200)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return svc.companies(q, page, page_size)


@router.get("/api/companies/{company_id}")
def company(company_id: str, svc: Service):
    return svc.company(company_id)


@router.get("/api/companies/{company_id}/relationships")
def relationships(company_id: str, filters: Filters, svc: Service):
    return svc.relationships(company_id, filters)


@router.get("/api/companies/{company_id}/graph")
def graph(company_id: str, filters: Filters, svc: Service):
    return svc.graph(company_id, filters)
