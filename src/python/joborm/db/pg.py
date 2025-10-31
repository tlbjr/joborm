#!/usr/bin/env python3
"""Datastore shim for Job Opportunity Relationship Management

This is a shim for a proper "get record by uuid" query system"""
import traceback
from typing import Any, List

from sqlmodel import create_engine, Session
import structlog

from config import settings

logger = structlog.stdlib.get_logger()

engine = create_engine(
    settings.POSTGRES_URI, pool_pre_ping=settings.POOL_PRE_PING, echo=settings.POSTGRES_ECHO
)


def get_session():
    with Session(engine) as session:
        yield session


def _get_by_id(collection: List[Any], id_: str):
    """Helper function to abstract querying by primary key"""
    # TODO Right now id is an index for prototyping, so swallow exceptions
    try:
        obj = collection[int(id_)]
    except Exception as _:
        obj = None
        traceback.print_exc()
    return obj


def _set_id(obj: Any, id_: str):
    """Helper function to abstract saving primary key"""
    setattr(obj, "id", id_)
    return obj


def _insert_record(collection: List[Any], obj: Any):
    """Helper function to abstract inserting a record"""
    id_ = getattr(obj, "id")
    count = len(collection)
    if not id_:
        # TODO Just for prototyping. Use a proper DB sequence / serial / uuid.
        setattr(obj, "id", str(count))
        collection.append(obj)
    else:
        return False
    return obj


def _update_record(collection: List[Any], obj: Any):
    """Helper function to abstract updating a record"""
    id_ = getattr(obj, "id", None)
    count = len(collection)
    logger.debug(f"Updating {id_=} with total collection {count=}")
    if id_ is not None and count > int(id_):
        collection[int(id_)] = obj
    else:
        return False
    return obj


def _delete_record(collection: list[Any], obj: Any):
    """Helper function to abstract deleting a record"""
    return collection.remove(obj)
