#!/usr/bin/env python3
"""Schemas for Job Opportunity Relationship Management"""
from enum import StrEnum


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
