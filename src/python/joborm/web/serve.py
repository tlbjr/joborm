#!/usr/bin/env python3
"""REST API for Job Opportunity Relationship Management"""
import sys

from fastapi import FastAPI, Response
import structlog

# TODO Persistence throwaway stubs; replace with real datastore
from db.pg import _get_by_id, _delete_record, _insert_record, _update_record
from schemas import Company, Opportunity

# TODO Junk seeding data for test; remove when datastore is in place
from sample_data import companies, opportunities

logger = structlog.stdlib.get_logger()

app = FastAPI()


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
async def get_company(company_id: str) -> Response:
    """Retreive the company specified by id"""

    company = _get_by_id(companies, company_id)
    if company is None:
        return Response('{"detail": "Not found"}', 404)
    return company


@app.post("/company", response_model=Company)
async def create_company(company: Company) -> Company | Response:
    """Create a company resource"""

    # TODO Additional validation and dupe detection
    success = _insert_record(companies, company)
    if success is False:
        return Response('{"detail": "Error creating company"}', 422)
    return company


@app.put("/company/{company_id}", response_model=Company)
async def update_company(company_id: str, company: Company) -> Company | Response:
    """Update a company resource"""

    if company_id != getattr(company, "id", None):
        return Response('{"detail": "Non matching ids given"}', 422)

    company_check = _get_by_id(companies, company_id)
    if company_check is None:
        return Response('{"detail": "Not found"}', 404)

    success = _update_record(companies, company)
    if success is False:
        return Response('{"detail": "Error updating company"}', 422)
    return company


@app.delete("/company/{company_id}", response_model=None)
async def delete_company(company_id: str) -> None | Response:
    """Delete a company resource"""

    company = _get_by_id(companies, company_id)
    if company is None:
        return Response('{"detail": "Not found"}', 404)

    # TODO cascade (or force) parameter
    # Don't allow deletion if a foreign key relationship exists
    prevent_deletion = any([opp and opp.company_id == company_id for opp in opportunities])
    if prevent_deletion:
        return Response('{"detail": "Cannot delete due to relationships"}', 422)
    success = _delete_record(companies, company)
    if success is False:
        return Response('{"detail": "Error deleting company"}', 422)

    return None


# TODO Move resource groups to routers: app.include_router(opportunity.router)
@app.get("/opportunity/{opportunity_id}", response_model=Opportunity)
async def get_opportunity(opportunity_id: str) -> Response:
    """Retreive the opportunity specified by id"""

    opportunity = _get_by_id(opportunities, opportunity_id)
    if opportunity is None:
        return Response('{"detail": "Not found"}', 404)

    # TODO Move this into record fetch as we'll have referential integrity
    # Augment opportunity with company data
    company = _get_by_id(companies, opportunity.company_id)
    if company is None:
        logger.debug(f"Failed to fetch opportunity's company {opportunity.company_id=}.")
        return Response('{"detail": "Unable to fetch dependent record"}', 500)
    opportunity.company = company
    return opportunity


@app.post("/opportunity", response_model=Opportunity)
async def create_opportunity(opportunity: Opportunity) -> Opportunity | Response:
    """Create an opportunity resource"""
    # TODO Additional validation and dupe detection
    success = _insert_record(opportunities, opportunity)
    if success is False:
        return Response('{"detail": "Error creating opportunity"}', 500)
    return opportunity


@app.put("/opportunity/{opportunity_id}", response_model=Opportunity)
async def update_opportunity(
    opportunity_id: str, opportunity: Opportunity
) -> Opportunity | Response:
    """Update an opportunity resource"""
    if opportunity_id != getattr(opportunity, "id", None):
        return Response('{"detail": "Non matching ids given"}', 422)

    opportunity_check = _get_by_id(opportunities, opportunity_id)
    if opportunity_check is None:
        return Response('{"detail": "Not found"}', 404)

    success = _update_record(opportunities, opportunity)
    if success is False:
        return Response('{"detail": "Error updating opportunity"}', 500)
    return opportunity


@app.delete("/opportunity/{opportunity_id}", response_model=None)
async def delete_opportunity(opportunity_id: str) -> None | Response:
    """Delete an opportunity resource"""
    opportunity = _get_by_id(opportunities, opportunity_id)
    if opportunity is None:
        return Response('{"detail": "Not found"}', 404)
    # TODO opportunities don't have dependencies; implement a delete check later
    success = _delete_record(opportunities, opportunity)
    if success is False:
        return Response('{"detail": "Error deleting opportunity"}', 422)
    return None


if __name__ == "__main__":
    print(f"Run with uvicorn (--reload) {sys.argv[0][0:-3]}:app instead.")
