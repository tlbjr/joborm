#!/usr/bin/env python3
"""Schemas for Job Opportunity Relationship Management"""
from enum import StrEnum
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict


class CompanyType(StrEnum):
    """The stage of the company"""

    SEED = "Seed"
    SERIES_A = "Series A"
    SERIES_B = "Series B"
    SERIES_C = "Series C"
    SERIES_D = "Series D"
    SERIES_E = "Series E"
    SERIES_X = "Series X"
    LLC = "LLC"
    B_CORP = "B Corp"
    S_CORP = "S Corp"
    NON_PROFIT = "Non-profit"
    PUBLIC = "Public"
    UNKNOWN = "Unknown"


class Company(BaseModel):
    """The company's details"""

    name: str
    url: Optional[str] = ""
    linkedin: Optional[str] = ""
    glassdoor: Optional[str] = ""
    github: Optional[str] = ""
    size: Optional[int] = None
    type_: CompanyType = CompanyType.UNKNOWN

    # When object is database backed
    id: Optional[str] = None

    model_config = ConfigDict(use_enum_values=True)


class ProcessItemType(StrEnum):
    """The type of interview"""

    SCREEN_RECRUITER = "Screen - Recruiter"
    SCREEN_HIRING_MANAGER = "Screen - Hiring Manager"
    SCREEN_TECHNICAL = "Screen - Technical"
    SCREEN_OTHER = "Screen - Other"
    TECHNICAL_CODING = "Technical - Coding"
    TECHNICAL_DESIGN = "Technical - Design"
    TECHNICAL_TAKE_HOME = "Technical - Take Home"
    TECHNICAL_OTHER = "Technical - Other"
    PANEL = "Panel"
    PRODUCT = "Product"
    EXECUTIVE = "Executive"
    UNKNOWN = "Unknown"


class ProcessItem(BaseModel):
    """An item in the interview"""

    type_: ProcessItemType = ProcessItemType.UNKNOWN
    location: Literal["in-person", "remote", "either", "unknown"]
    with_: Literal["external", "internal", "unknown"]

    def __str__(self) -> str:
        return f"{self.type_} ({self.location}, {self.with_})"


class Process(BaseModel):
    """An interview process"""

    items: List[ProcessItem]


class Opportunity(BaseModel):
    """An opportunity"""

    company_id: str
    company: Optional[Company] = None
    position: str
    process: Process
    location: Literal["in-person", "remote", "unknown"] = "unknown"
    team: Optional[str] = ""
    team_size: Optional[int] = None
    team_size_growth: Optional[int] = None
    remote: Optional[bool] = None
    hybrid: Optional[bool] = None
    comp_base_range: Optional[str] = ""
    total_comp: Optional[str] = ""
    equity: Optional[str] = ""

    # When object is database backed
    id: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.position} @{self.company.name if self.company else self.company_id}"
