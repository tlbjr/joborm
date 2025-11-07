try:
    from datetime import datetime, UTC
except Exception as _:
    from datetime import datetime, timezone
    UTC = timezone.utc
from typing import List, Optional

from pydantic import ConfigDict
from sqlmodel import DateTime, Field, Relationship, SQLModel
import uuid_utils.compat as uuid

from shared import CompanyType, ContactType, LocationType, ProcessItemType


class JoboBase(SQLModel):
    pass


class JoboRecordBase(JoboBase):
    created_at: Optional[datetime] = Field(
        sa_type=DateTime(timezone=True),
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
    )
    created_by: Optional[str] = ""
    updated_at: Optional[datetime] = Field(
        sa_type=DateTime(timezone=True),
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)},
        nullable=False,
    )
    updated_by: Optional[str] = ""


class CompanyBase(JoboBase):
    """All the loose fields for a company"""

    name: str
    url: str | None = ""
    linkedin: str | None = ""
    glassdoor: str | None = ""
    crunchbase: str | None = ""
    github: str | None = ""
    size: int | None = None
    company_type: CompanyType = CompanyType.UNKNOWN

    model_config = ConfigDict(use_enum_values=True)


class CompanyCreate(CompanyBase):
    """Just loose fields when creating a company"""

    pass


class CompanyUpdate(CompanyBase):
    """Updating or soft-deleting a company requires it's id"""

    id: uuid.UUID | None = Field(default_factory=uuid.uuid7, primary_key=True)


class CompanyPublic(CompanyUpdate):
    """Company's are returned with their opportunities or an empty list"""

    opportunities: List["Opportunity"] = []


class CompanyRecord(CompanyUpdate, JoboRecordBase, table=True):
    """Company records have working relationships and basic audit fields"""

    __tablename__ = "company"

    opportunities: Optional[List["Opportunity"]] = Relationship(back_populates="company")


class ProcessItemCreate(JoboBase):
    item_type: ProcessItemType = ProcessItemType.UNKNOWN
    location_type: LocationType = LocationType.UNKNOWN
    contact_type: ContactType = ContactType.UNKNOWN
    group: bool = False
    order: int = 0

    model_config = ConfigDict(use_enum_values=True)


class ProcessItem(JoboRecordBase, table=True):
    __tablename__ = "processitem"
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


class Process(JoboRecordBase, table=True):
    __tablename__ = "process"
    id: uuid.UUID | None = Field(default_factory=uuid.uuid7, primary_key=True)
    opportunity_id: uuid.UUID = Field(foreign_key="opportunity.id")

    # items: List[ProcessItem] = Relationship(back_populates="process")
    opportunity: "Opportunity" = Relationship(back_populates="processes")


class OpportunityCreate(JoboBase):
    company_id: uuid.UUID
    name: str
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


class Opportunity(JoboRecordBase, table=True):
    __tablename__ = "opportunity"
    id: uuid.UUID | None = Field(default_factory=uuid.uuid7, primary_key=True)
    company_id: uuid.UUID = Field(foreign_key="company.id")
    name: str
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

    company: CompanyRecord = Relationship(back_populates="opportunities")

    model_config = ConfigDict(use_enum_values=True)
