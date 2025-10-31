#!/usr/bin/env python3
"""REST API for Job Opportunity Relationship Management"""
import sys
from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, Response
import structlog

from db.pg import get_session, Session
from db.services import CompanySvc, OpportunitySvc
from db.models import Company
from schemas import Opportunity

# TODO Junk seeding data for test; remove when datastore is in place
# from sample_data import companies, opportunities

logger = structlog.stdlib.get_logger()

app = FastAPI()

SessionDep = Annotated[Session, Depends(get_session)]


# TODO Implement BaseSettings for env vars and/or secrets injection
@app.get("/")
async def about():
    return {
        "env": "dev",
        "docs_url": "/docs",
        "name": "Job Opportunity Relationship Management",
        "version": "0.1.0",
    }


# TODO Move resource groups to routers: app.include_router(company.router)
@app.get("/company/{company_id}", response_model=Company)
async def get_company(company_id: UUID, session: SessionDep) -> Response:
    """Retreive the company specified by id"""

    company = session.get(Company, company_id)
    if company is None:
        return Response('{"detail": "Not found"}', 404)
    return company


@app.post("/company", response_model=Company)
async def create_company(company: Company, session: SessionDep) -> Company | Response:
    """Create a company resource"""

    # TODO Additional validation and dupe detection
    success = CompanySvc.insert_company(session, company)
    if success is False:
        return Response('{"detail": "Error creating company"}', 422)
    return company


@app.put("/company/{company_id}", response_model=Company)
async def update_company(
    company_id: UUID, company: Company, session: SessionDep
) -> Company | Response:
    """Update a company resource"""

    if str(company_id) != company.id:
        return Response('{"detail": "Non matching ids given"}', 422)

    existing_company = session.get(Company, company_id)
    if existing_company is None:
        return Response('{"detail": "Not found"}', 404)

    company.id = UUID(company.id)  # fix warn: expected UUID instead of str
    company_data = company.model_dump(exclude_unset=True)
    existing_company.sqlmodel_update(company_data)
    success = CompanySvc.update_company(session, existing_company)
    if success is False:
        return Response('{"detail": "Error updating company"}', 422)
    return existing_company


@app.delete("/company/{company_id}", response_model=None)
async def delete_company(company_id: UUID, session: SessionDep) -> None | Response:
    """Delete a company resource"""

    existing_company = session.get(Company, company_id)
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

    return None


# TODO Move resource groups to routers: app.include_router(opportunity.router)
@app.get("/opportunity/{opportunity_id}", response_model=Opportunity)
async def get_opportunity(opportunity_id: UUID, session: SessionDep) -> Response:
    """Retreive the opportunity specified by id"""

    opportunity = session.get(Opportunity, opportunity_id)
    if opportunity is None:
        return Response('{"detail": "Not found"}', 404)

    # TODO Move this into record fetch as we'll have referential integrity
    # Augment opportunity with company data
    company = session.get(Company, opportunity.company_id)
    if company is None:
        logger.debug(f"Failed to fetch opportunity's company {opportunity.company_id=}.")
        return Response('{"detail": "Unable to fetch dependent record"}', 500)
    opportunity.company = company
    return opportunity


@app.post("/opportunity", response_model=Opportunity)
async def create_opportunity(
    opportunity: Opportunity, session: SessionDep
) -> Opportunity | Response:
    """Create an opportunity resource"""
    # TODO Additional validation and dupe detection
    success = OpportunitySvc.insert_opportunity(session, opportunity)
    if success is False:
        return Response('{"detail": "Error creating opportunity"}', 500)
    return opportunity


@app.put("/opportunity/{opportunity_id}", response_model=Opportunity)
async def update_opportunity(
    opportunity_id: UUID, opportunity: Opportunity, session: SessionDep
) -> Opportunity | Response:
    """Update an opportunity resource"""
    if opportunity_id != getattr(opportunity, "id", None):
        return Response('{"detail": "Non matching ids given"}', 422)

    opportunity_check = session.get(Opportunity, opportunity_id)
    if opportunity_check is None:
        return Response('{"detail": "Not found"}', 404)

    success = OpportunitySvc.update_opportunity(session, opportunity)
    if success is False:
        return Response('{"detail": "Error updating opportunity"}', 500)
    return opportunity


@app.delete("/opportunity/{opportunity_id}", response_model=None)
async def delete_opportunity(opportunity_id: UUID, session: SessionDep) -> None | Response:
    """Delete an opportunity resource"""
    opportunity = session.gert(Opportunity, opportunity_id)
    if opportunity is None:
        return Response('{"detail": "Not found"}', 404)
    # TODO opportunities don't have dependencies; implement a delete check later
    success = OpportunitySvc.delete_opportunity(session, opportunity)
    if success is False:
        return Response('{"detail": "Error deleting opportunity"}', 422)
    return None


if __name__ == "__main__":
    print(f"Run with uvicorn (--reload) {sys.argv[0][0:-3]}:app instead.")
