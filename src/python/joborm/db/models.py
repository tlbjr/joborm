from typing import List, Literal

from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel
import uuid_utils.compat as uuid

from shared import CompanyType, ProcessItemType


class JobORMBase(SQLModel):
    pass


class CompanyCreate(JobORMBase):
    name: str
    url: str | None = ""
    linkedin: str | None = ""
    glassdoor: str | None = ""
    github: str | None = ""
    size: int | None = None
    type_: CompanyType = CompanyType.UNKNOWN

    model_config = ConfigDict(use_enum_values=True)

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

    model_config = ConfigDict(use_enum_values=True)


class ProcessItem(JobORMBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid7, primary_key=True)
    process_id: uuid.UUID = Field(foreign_key="process.id")
    type_: ProcessItemType = ProcessItemType.UNKNOWN
    location: str = Literal["in-person", "remote", "either", "unknown"]
    with_: str = Literal["external", "internal", "unknown"]
    group: bool = False
    order: int = 0

    process: "Process" = Relationship(back_populates="items")


class Process(JobORMBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid7, primary_key=True)
    opportunity_id: uuid.UUID = Field(foreign_key="opportunity.id")

    items: List[ProcessItem] = Relationship(back_populates="process")

    opportunity: "Opportunity" = Relationship(back_populates="process")


class OpportunityCreate(JobORMBase):
    company_id: uuid.UUID
    position: str
    url: str | None = ""
    location: Literal["in-person", "remote", "unknown"] = "unknown"
    team: str | None = ""
    team_size: int | None = None
    team_size_growth: int | None = None
    remote: bool | None = None
    hybrid: bool | None = None
    comp_base_range: str | None = ""
    total_comp: str | None = ""
    equity: str | None = ""
    ai_usage: Literal["no", "encouraged", "forced", "unknown"] = "unknown"
    longer_hours: bool | None = None

    model_config = ConfigDict(use_enum_values=True)


class Opportunity(JobORMBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid7, primary_key=True)
    company_id: uuid.UUID = Field(foreign_key="company.id")
    position: str
    url: str | None = ""
    # location: Literal["in-person", "remote", "unknown"] = "unknown"
    team: str | None = ""
    team_size: int | None = None
    team_size_growth: int | None = None
    remote: bool | None = None
    hybrid: bool | None = None
    comp_base_range: str | None = ""
    total_comp: str | None = ""
    equity: str | None = ""
    # ai_usage: Literal["no", "encouraged", "forced", "unknown"] = "unknown"
    longer_hours: bool | None = None

    process: Process = Relationship(back_populates="opportunity")

    company: Company = Relationship(back_populates="opportunities")

    model_config = ConfigDict(use_enum_values=True)
