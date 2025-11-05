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


@router.get("/opportunity/{opportunity_id}", response_model=Opportunity)
async def get_opportunity(opportunity_id: UUID, session: SessionDep) -> Response:
    """Retreive the opportunity specified by id"""

    opportunity = session.get(Opportunity, opportunity_id)
    if opportunity is None:
        return Response('{"detail": "Not found"}', 404)

    # TODO Move this into record fetch as we'll have referential integrity
    # Augment opportunity with company data
    # company = session.get(Company, opportunity.company_id)
    # if company is None:
    #    logger.debug(f"Failed to fetch opportunity's company {opportunity.company_id=}.")
    #    return Response('{"detail": "Unable to fetch dependent record"}', 500)
    # opportunity.company = company
    return opportunity


@router.post("/opportunity", response_model=Opportunity)
async def create_opportunity(
    opportunity: OpportunityCreate, session: SessionDep
) -> Opportunity | Response:
    """Create an opportunity resource"""

    # if not opportunity.company_id:
    #    return Response('{"detail": "Invalid company_id"}', 422)

    opportunity_data = opportunity.model_dump(exclude_unset=True)
    opportunity_new = Opportunity.model_validate(opportunity_data)

    # TODO Additional validation and dupe detection
    success = OpportunitySvc.insert_opportunity(session, opportunity_new)
    if success is False:
        return Response('{"detail": "Error creating opportunity"}', 500)

    session.commit()
    session.refresh(opportunity_new)
    return opportunity_new


@router.put("/opportunity/{opportunity_id}", response_model=Opportunity)
async def update_opportunity(
    opportunity_id: UUID, opportunity: Opportunity, session: SessionDep
) -> Opportunity | Response:
    """Update an opportunity resource"""

    if str(opportunity_id) != opportunity.id:
        return Response('{"detail": "Non matching ids given"}', 422)

    if not opportunity.id:
        return Response('{"detail": "Invalid opportunity_id"}', 422)

    if not opportunity.company_id:
        return Response('{"detail": "Invalid company_id"}', 422)

    existing_opportunity = session.get(Opportunity, opportunity_id)
    if existing_opportunity is None:
        return Response('{"detail": "Not found"}', 404)

    opportunity.id = UUID(opportunity.id)  # fix warn: expected UUID instead of str
    opportunity.company_id = UUID(opportunity.company_id)  # fix warn: expected UUID instead of str
    opportunity_data = opportunity.model_dump(exclude_unset=True)
    existing_opportunity.sqlmodel_update(opportunity_data)
    success = OpportunitySvc.update_opportunity(session, existing_opportunity)
    if success is False:
        return Response('{"detail": "Error updating opportunity"}', 500)

    session.commit()
    session.refresh(existing_opportunity)
    return existing_opportunity


@router.delete("/opportunity/{opportunity_id}", response_model=None)
async def delete_opportunity(opportunity_id: UUID, session: SessionDep) -> None | Response:
    """Delete an opportunity resource"""
    existing_opportunity = session.get(Opportunity, opportunity_id)
    if existing_opportunity is None:
        return Response('{"detail": "Not found"}', 404)
    if any(existing_opportunity.processes):  # prevent_deletion:
        return Response('{"detail": "Cannot delete due to relationships"}', 422)
    success = OpportunitySvc.delete_opportunity(session, existing_opportunity)
    if success is False:
        return Response('{"detail": "Error deleting opportunity"}', 422)
    session.commit()
    return None

