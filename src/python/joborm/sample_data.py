#!/usr/bin/env python3
"""Sample Data for Job Opportunity Relationship Management

The Data Model:
Company 1-M (unordered) Opportunity 1-1 (Interview)Process 1-M (ordered) (Interview)ProcessItem

Enums:
    CompanyType
    ProcessItemType
Literals:
    "either", "in-person", "remote", "unknown"

TODO:
1. Figure out semantics around shared / crowd sourced data, if any.
2. Extend Process and ProcessItem with more metadata.
2. Allow Process (which is just a list of ProcessItems) to be recursive. e.g.
    Process = {
        items: [
            ProcessItem,
            ProcessItem,
            Process = {
                items: [
                    (Sub)ProcessItem,
                    (Sub)ProcessItem,
                    (Sub)ProcessItem,
                ]
            },
            ProcessItem,
            ...,
        ]
    }

"""
import copy


from schemas import Company, Opportunity, Process, ProcessItem
from shared import CompanyType, ProcessItemType

samp_company_1 = Company.model_validate(
    {
        "id": "1",
        "name": "Sample Company 1",
        "type_": CompanyType.S_CORP,
        "url": "https://example.com",
        "linkedin": "https://linkedin.com/example.com",
    }
)
samp_company_2 = Company.model_validate(
    {
        "id": "2",
        "name": "Sample Company 2",
        "type_": CompanyType.SERIES_A,
        "url": "https://example2.com",
        "github": "https://github.com/example2.com",
    }
)

samp_process_em = Process(
    items=[
        ProcessItem(
            type_=ProcessItemType.SCREEN_RECRUITER,
            location="remote",
            with_="external",
        ),
        ProcessItem(
            type_=ProcessItemType.SCREEN_RECRUITER,
            location="remote",
            with_="internal",
        ),
        ProcessItem(
            type_=ProcessItemType.SCREEN_HIRING_MANAGER,
            location="remote",
            with_="internal",
        ),
        ProcessItem(
            type_=ProcessItemType.TECHNICAL_TAKE_HOME,
            location="remote",
            with_="internal",
        ),
        ProcessItem(
            type_=ProcessItemType.PANEL,
            location="in-person",
            with_="internal",
        ),
        ProcessItem(
            type_=ProcessItemType.EXECUTIVE,
            location="remote",
            with_="internal",
        ),
    ]
)

samp_process_quick = Process(
    items=[
        ProcessItem(
            type_=ProcessItemType.SCREEN_HIRING_MANAGER,
            location="remote",
            with_="internal",
        ),
        ProcessItem(
            type_=ProcessItemType.SCREEN_TECHNICAL,
            location="remote",
            with_="internal",
        ),
        ProcessItem(
            type_=ProcessItemType.PANEL,
            location="in-person",
            with_="internal",
        ),
    ]
)

samp_process_full = copy.deepcopy(samp_process_em)
samp_process_full.items[3].type_ = ProcessItemType.TECHNICAL_CODING

samp_opportunity_1 = Opportunity(
    company_id=samp_company_1.id or "1", position="Sample SWE", process=samp_process_full
)
samp_opportunity_2 = Opportunity(
    company_id=samp_company_2.id or "2", position="Sample Sr SWE", process=samp_process_quick
)
samp_opportunity_3 = Opportunity(
    company_id=samp_company_1.id or "1", position="Engineering Mgr", process=samp_process_em
)

companies = [None, samp_company_1, samp_company_2]
opportunities = [None, samp_opportunity_1, samp_opportunity_2, samp_opportunity_3]
