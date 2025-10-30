#!/usr/bin/env python3
"""Schemas for Job Opportunity Relationship Management"""
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict

from shared import CompanyType, ProcessItemType


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
