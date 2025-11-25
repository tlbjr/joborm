#!/usr/bin/env python3
"""REST API for Job Opportunity Relationship Management"""
from typing import Annotated
from uuid import UUID

import aiohttp
from fastapi import Depends, APIRouter, Response
import requests
import structlog

from db.pg import get_session, Session
from db.services import OpportunitySvc
from db.models import (
    Opportunity,
    OpportunityCreate,
    OpportunityPage,
    OpportunitySimple,
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


@router.post("/opportunity/ingest", response_model=Opportunity)
async def ingest_opportunity(
    opportunity_page: OpportunityPage, session: SessionDep
) -> Opportunity | Response:
    """Create an opportunity resource from web page details"""

    opportunity_rec = None
    # TODO Check for the url first. Existing opp? If not, queue for ingest.
    # response = requests.get(opportunity_page.url)
    logger.debug(f"Fetching {opportunity_page.url=}")

    # TODO Move fetch to queue/async calls
    async def get_page():
        """Helper function to use the async loop of fastapi"""
        async with aiohttp.ClientSession() as session:
            response = await session.get(opportunity_page.url)
            return await response.text()

    try:
        response_html = await get_page()
    except Exception as _:
        response_html = None
        trace_back.print_exc()

    # TODO Move parsing to util lib
    def _names_from_html(soup):
        """Parse an HTML page for company and opportunity names"""
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(response_html, "html.parser")
        clean = str(soup.title).replace("<title>", "").replace("</title>", "")
        logger.debug(f"{soup.title=} and {clean=}")
        data = clean.replace(" | LinkedIn", "").split(" hiring ")
        company_name = data[0]
        opportunity_name = data[1].split(" in ")[0]
        logger.debug(f"{company_name=} {opportunity_name=}")
        return company_name, opportunity_name

    if response_html is not None:
        company_name, opportunity_name = _names_from_html(response_html)
        if company_name is not None and opportunity_name is not None:
            opportunity = OpportunitySimple(
                company_name=company_name,
                opportunity_name=opportunity_name,
                url=opportunity_page.url,
            )
            opportunity_rec = OpportunitySvc.ingest_opportunity_from_url(session, opportunity)
            logger.debug("Calling commit")
            session.commit()
            session.refresh(opportunity_rec)

    return opportunity_rec
