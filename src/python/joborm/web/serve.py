#!/usr/bin/env python3
"""REST API for Job Opportunity Relationship Management"""
import sys
from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, Response
import structlog

from db.pg import get_session, Session
from db.services import OpportunitySvc, ProcessSvc
from db.models import (
    Opportunity,
    OpportunityCreate,
    Process,
    ProcessItem,
    ProcessCreate,
)

from web.routers.company import router as CompanyRouter
from web.routers.opportunity import router as OpportunityRouter
from web.routers.process import router as ProcessRouter
from web.routers.sso import router as SSORouter


logger = structlog.stdlib.get_logger()

app = FastAPI()
for router in [CompanyRouter, OpportunityRouter, ProcessRouter, SSORouter]:
    app.include_router(router)

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


# TODO Move resource groups to routers: app.include_router(opportunity.router)
@app.get("/opportunity/{opportunity_id}", response_model=Opportunity)
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


@app.post("/opportunity", response_model=Opportunity)
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


@app.put("/opportunity/{opportunity_id}", response_model=Opportunity)
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


@app.delete("/opportunity/{opportunity_id}", response_model=None)
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


# TODO Move resource groups to routers: app.include_router(process.router)
@app.get("/process/{process_id}", response_model=Process)
async def get_process(process_id: UUID, session: SessionDep) -> Process | Response:
    """Retreive the process specified by id"""

    process = session.get(Process, process_id)
    if process is None:
        return Response('{"detail": "Not found"}', 404)
    return process


@app.post("/process", response_model=Process)
async def create_process(process: ProcessCreate, session: SessionDep) -> Process | Response:
    """Create a process resource"""

    # TODO Additional validation and dupe detection
    process_data = process.model_dump(exclude_unset=True)
    print(f"before {process_data=}")
    items = process_data.pop("items")
    print(f"after {process_data=}")
    print(f"after {items=}")
    process_new = Process.model_validate(process_data)
    success = ProcessSvc.insert_process(session, process_new)
    print(f"after {process_new=}")
    if success is False:
        return Response('{"detail": "Error creating process"}', 422)
    for idx, item in enumerate(items):
        item["order"] = idx
        item["process_id"] = process_new.id
        item_new = ProcessItem.model_validate(item)
        print(f"before {item_new=}")
        ProcessSvc.insert_process_item(session, item_new)
        print(f"after {item_new=}")
        if success is False:
            return Response('{"detail": "Error creating process items"}', 422)

    # TODO Move to middleware or something similar
    session.commit()
    session.refresh(process_new)
    return process_new


@app.put("/process/{process_id}", response_model=Process)
async def update_process(
    process_id: UUID, process: Process, session: SessionDep
) -> Process | Response:
    """Update a company resource"""

    if str(process_id) != process.id:
        return Response('{"detail": "Non matching ids given"}', 422)

    if not process.id:
        return Response('{"detail": "Invalid process_id"}', 422)

    existing_process = session.get(Process, process_id)
    if existing_process is None:
        return Response('{"detail": "Not found"}', 404)

    process.id = UUID(process.id)  # fix warn: expected UUID instead of str
    process_data = process.model_dump(exclude_unset=True)
    existing_process.sqlmodel_update(process_data)
    success = ProcessSvc.update_process(session, existing_process)
    if success is False:
        return Response('{"detail": "Error updating company"}', 422)

    session.commit()
    session.refresh(existing_process)
    return existing_process


@app.delete("/process/{process_id}", response_model=None)
async def delete_process(process_id: UUID, session: SessionDep) -> None | Response:
    """Delete a process resource"""

    existing_process = session.get(Process, process_id)
    if existing_process is None:
        return Response('{"detail": "Not found"}', 404)

    # TODO cascade (or force) parameter
    # Don't allow deletion if a foreign key relationship exists
    # if any(items):  # prevent_deletion:
    #    return Response('{"detail": "Cannot delete due to relationships"}', 422)
    items = ProcessSvc.get_process_items(session, process_id)
    if items:
        logger.warn("Deleting items from process before process deletion")
        ProcessSvc.delete_process_items(session, process_id)
    success = ProcessSvc.delete_process(session, existing_process)
    if success is False:
        return Response('{"detail": "Error deleting process"}', 422)

    session.commit()
    return None


if __name__ == "__main__":
    print(f"Run with uvicorn (--reload) {sys.argv[0][0:-3]}:app instead.")
