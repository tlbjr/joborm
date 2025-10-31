from typing import List, Literal

from sqlmodel import Field, Relationship, SQLModel
import uuid_utils.compat as uuid

from shared import CompanyType, ProcessItemType


class JobORMBase(SQLModel):
    pass


class Company(JobORMBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid7, primary_key=True)
    name: str
    url: str | None = ""
    linkedin: str | None = ""
    glassdoor: str | None = ""
    github: str | None = ""
    size: int | None = None
    type_: CompanyType = CompanyType.UNKNOWN

    opportunities: list["Opportunity"] = Relationship(back_populates="company")


class Opportunity(JobORMBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid7, primary_key=True)
    company_id: uuid.UUID = Field(foreign_key="company.id")
    company: "Company" = Relationship(back_populates="opportunities")
    title: str = "TBD"
    job_description_url: str = ""


class ProcessItem(JobORMBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid7, primary_key=True)
    type_: ProcessItemType = ProcessItemType.UNKNOWN
    location: str = Literal["in-person", "remote", "either", "unknown"]
    with_: str = Literal["external", "internal", "unknown"]
    group: bool = False
    process_id: uuid.UUID = Field(foreign_key="process.id")
    process: "Process" = Relationship(back_populates="items")


class Process(JobORMBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid7, primary_key=True)
    items: List[ProcessItem] = Relationship(back_populates="process")
