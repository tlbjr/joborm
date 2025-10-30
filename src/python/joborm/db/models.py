from typing import List, Literal, Optional
import uuid

from sqlmodel import Relationship, SqlModel

from shared import CompanyType, ProcessItemType


class Company(SqlModel):
    id: Optional[uuid] = None
    name: str
    type_: CompanyType = CompanyType.UNKNOWN


class Opportunity(SqlModel):
    id: Optional[uuid] = None
    company: str = Relationship("Company", backref="opportunities", foreign_key="company_id")
    title: str = "TBD"
    job_description_url: str = ""


class ProcessItem(SqlModel):
    type_: ProcessItemType = ProcessItemType.UNKNOWN
    location: str = Literal["in-person", "remote", "either", "unknown"]
    with_: str = Literal["external", "internal", "unknown"]
    group: bool = False


class Process(SqlModel):
    items: List[ProcessItem] = []
