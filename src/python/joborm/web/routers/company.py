#!/usr/bin/env python3
"""REST API for Job Opportunity Relationship Management"""
import sys
from typing import Annotated
from uuid import UUID

from fastapi import Depends, APIRouter, Response
import structlog

from db.pg import get_session, Session
from db.services import CompanySvc, OpportunitySvc, ProcessSvc
from db.models import (
    CompanyCreate,
    CompanyPublic,
    CompanyRecord,
    CompanyUpdate,
    Opportunity,
    OpportunityCreate,
    Process,
    ProcessItem,
    ProcessCreate,
)

# TODO Junk seeding data for test; remove when datastore is in place
# from sample_data import companies, opportunities

logger = structlog.stdlib.get_logger()

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/company/{company_id}", response_model=CompanyPublic)
async def get_company(company_id: UUID, session: SessionDep) -> Response:
    """Retreive the company specified by id"""

    company = CompanySvc.get_by_id(session, company_id)
    if company is None:
        return Response('{"detail": "Not found"}', 404)
    return company


@router.post("/company", response_model=CompanyPublic)
async def create_company(company: CompanyCreate, session: SessionDep) -> CompanyPublic | Response:
    """Create a company resource"""

    # TODO Additional validation and dupe detection
    company_data = company.model_dump(exclude_unset=True)
    company_new = CompanySvc.insert_company(session, company_data)
    if company_new is None:
        return Response('{"detail": "Error creating company"}', 422)
    session.commit()
    session.refresh(company_new)
    return company_new


@router.put("/company/{company_id}", response_model=CompanyPublic)
async def update_company(
    company_id: UUID, company: CompanyUpdate, session: SessionDep
) -> CompanyPublic | Response:
    """Update a company resource"""

    if company_id != company.id:
        return Response('{"detail": "Non matching ids given"}', 422)

    if not company.id:  # TODO Is this pydantic validation working already?
        return Response('{"detail": "Invalid company_id"}', 422)

    existing_company = CompanySvc.update_company(session, company)
    if existing_company is None:
        return Response('{"detail": "Error updating company"}', 422)
    session.commit()
    session.refresh(existing_company)
    return existing_company


@router.delete("/company/{company_id}", response_model=None)
async def delete_company(company_id: UUID, session: SessionDep) -> None | Response:
    """Delete a company resource"""

    existing_company = session.get(CompanyRecord, company_id)
    if existing_company is None:
        return Response('{"detail": "Not found"}', 404)

    # TODO cascade (or force) parameter
    # Don't allow deletion if a foreign key relationship exists
    # prevent_deletion = any([opp and opp.company_id == company_id for opp in opportunities])
    if any(existing_company.opportunities):  # prevent_deletion:
        return Response('{"detail": "Cannot delete due to relationships"}', 422)
    success = CompanySvc.delete_company(session, existing_company)
    if success is False:
        return Response('{"detail": "Error deleting company"}', 422)

    session.commit()
    return None

