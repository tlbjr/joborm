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
from web.routers.static import router as StaticRouter


logger = structlog.stdlib.get_logger()

app = FastAPI()
for router in [CompanyRouter, OpportunityRouter, ProcessRouter, SSORouter, StaticRouter]:
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


if __name__ == "__main__":
    print(f"Run with uvicorn (--reload) {sys.argv[0][0:-3]}:app instead.")
