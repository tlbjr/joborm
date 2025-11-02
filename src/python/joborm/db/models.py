from typing import List

from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel
import uuid_utils.compat as uuid

from shared import CompanyType, ContactType, LocationType, ProcessItemType


class JoboBase(SQLModel):
    pass


class CompanyCreate(JoboBase):
    name: str
    url: str | None = ""
    linkedin: str | None = ""
    glassdoor: str | None = ""
    github: str | None = ""
    size: int | None = None
    company_type: CompanyType = CompanyType.UNKNOWN

    model_config = ConfigDict(use_enum_values=True)


class Company(JoboBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid7, primary_key=True)
    name: str
    url: str | None = ""
    linkedin: str | None = ""
    glassdoor: str | None = ""
    github: str | None = ""
    size: int | None = None
    company_type: CompanyType = CompanyType.UNKNOWN

    opportunities: List["Opportunity"] = Relationship(back_populates="company")

    model_config = ConfigDict(use_enum_values=True)


class ProcessItemCreate(JoboBase):
    item_type: ProcessItemType = ProcessItemType.UNKNOWN
    location_type: LocationType = LocationType.UNKNOWN
    contact_type: ContactType = ContactType.UNKNOWN
    group: bool = False
    order: int = 0

    model_config = ConfigDict(use_enum_values=True)


class ProcessItem(JoboBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid7, primary_key=True)
    process_id: uuid.UUID = Field(foreign_key="process.id")
    item_type: ProcessItemType = ProcessItemType.UNKNOWN
    location_type: LocationType = LocationType.UNKNOWN
    contact_type: ContactType = ContactType.UNKNOWN
    group: bool = False
    order: int = 0

    # process: "Process" = Relationship(back_populates="items")

    model_config = ConfigDict(use_enum_values=True)


class ProcessCreate(JoboBase):
    opportunity_id: uuid.UUID
    items: List[ProcessItemCreate]


class Process(JoboBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid7, primary_key=True)
    opportunity_id: uuid.UUID = Field(foreign_key="opportunity.id")

    # items: List[ProcessItem] = Relationship(back_populates="process")
    opportunity: "Opportunity" = Relationship(back_populates="processes")


class OpportunityCreate(JoboBase):
    company_id: uuid.UUID
    position: str
    url: str | None = ""
    location_type: LocationType = LocationType.UNKNOWN
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

    model_config = ConfigDict(use_enum_values=True)


class Opportunity(JoboBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid7, primary_key=True)
    company_id: uuid.UUID = Field(foreign_key="company.id")
    position: str
    url: str | None = ""
    location_type: LocationType = LocationType.UNKNOWN
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

    processes: list[Process] = Relationship(back_populates="opportunity")

    company: Company = Relationship(back_populates="opportunities")

    model_config = ConfigDict(use_enum_values=True)
