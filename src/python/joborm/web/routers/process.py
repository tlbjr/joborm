#!/usr/bin/env python3
"""REST API for Job Opportunity Relationship Management"""
from typing import Annotated
from uuid import UUID

from fastapi import Depends, APIRouter, Response
import structlog

from db.pg import get_session, Session
from db.services import ProcessSvc
from db.models import (
    Process,
    ProcessItem,
    ProcessCreate,
)

# TODO Junk seeding data for test; remove when datastore is in place
# from sample_data import companies, opportunities

logger = structlog.stdlib.get_logger()

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/process/{process_id}", response_model=Process)
async def get_process(process_id: UUID, session: SessionDep) -> Process | Response:
    """Retreive the process specified by id"""

    process = session.get(Process, process_id)
    if process is None:
        return Response('{"detail": "Not found"}', 404)
    return process


@router.post("/process", response_model=Process)
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


@router.put("/process/{process_id}", response_model=Process)
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


@router.delete("/process/{process_id}", response_model=None)
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
