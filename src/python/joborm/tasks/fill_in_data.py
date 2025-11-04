#!/usr/bin/env python
from datetime import datetime, timedelta, UTC
import os
import traceback

from ddgs import DDGS
from sqlmodel import select, Session
import structlog

from db.pg import engine
from db.models import CompanyRecord, Opportunity  # TODO SyncRecord, ChangeRecord


logger = structlog.stdlib.get_logger()

DEBUG = os.getenv("DEBUG", False)
DRY_RUN = os.getenv("DRY_RUN", False)
TIME_BUDGET = os.getenv("TIME_BUDGET", 20)
ITEM_BUDGET = os.getenv("ITEM_BUDGET", 200)


def get_search_result_url(search_terms: str) -> str | None:
    """Do a web text search and return the first result"""
    if DEBUG:
        logger.debug(f"search_terms: {search_terms}")
    try:
        result = DDGS().text(f"{search_terms}", backend="auto", max_results=1)
        if result:
            if DEBUG:
                logger.debug(result)
            return result[0].get("href")
    except Exception as _:
        logger.warn(f"{__file__} Exception looking up {search_terms}")
        traceback.print_exc()
    return None


def _check_site(column_name, url_result) -> bool:
    """Is a requested search site part of the search result url?"""
    return f"{column_name}.com" in url_result if column_name != "url" else True


def _find_and_set_url(
    record: CompanyRecord | Opportunity,
    site_description: str,
    set_attr: str = "url",
) -> bool:
    """Use a variety of methods to obtain correct information about a record

    @params
    set_attr: The attribute to search for and set."""
    site_qualifier = f"site:{set_attr}.com" if set_attr != "url" else ""
    logger.debug(f"Attempting to find {record.name}'s {set_attr}")
    # TODO If coming in through the moderation queue, filter out the current value.
    # url_result = get_search_result_url(f"\"{record.name}\" -{record.url} {site_description} {site_qualifier}")
    url_result = get_search_result_url(f'"{record.name}" {site_description} {site_qualifier}')
    if url_result and _check_site(set_attr, url_result):
        logger.info(f"Updating {record.name}'s {set_attr} to {url_result}")
        setattr(record, set_attr, url_result)
        return True
    return False


# TODO
def find_position_job_description():
    pass


def find_company_size():
    pass


def find_company_funding_type_and_state():
    pass


# select(Company).join(CompanySync).where(Company.c.url == None).order_by(CompanySync.c.updated_dt.desc())
# stmt = select(CompanyRecord).where(CompanyRecord.url.in_(["", None])).limit(ITEM_BUDGET)
def do_feed_run():
    """For records that have incomplete data, attempt to figure out the missing values"""
    start_ts = datetime.now(tz=UTC)
    current_ts = datetime.now(tz=UTC)

    with Session(engine) as session:
        stmt = select(CompanyRecord).limit(ITEM_BUDGET / 2)
        companies_to_update = session.exec(stmt).all()

        for idx, company in enumerate(companies_to_update):
            # Realistically, what can I REST API, google, scrape, or LLM?
            logger.info(f"Company #{idx+1} {company.name}")
            if not company.url:  # or company.url_reported_wrong > 3:
                logger.debug(f"Attempting search for {company.name}'s webiste")
                if _find_and_set_url(company, "website url"):
                    session.add(company)
            if not company.linkedin:
                logger.debug(f"Attempting search for {company.name}'s linkedin")
                if _find_and_set_url(company, "url for linkedin", set_attr="linkedin"):
                    session.add(company)
            if not company.glassdoor:
                logger.debug(f"Attempting search for {company.name}'s glassdoor")
                if _find_and_set_url(company, "url for glassdoor", set_attr="glassdoor"):
                    session.add(company)
            if not company.github:
                logger.debug(f"Attempting search for {company.name}'s github")
                if _find_and_set_url(company, "url for github", set_attr="github"):
                    session.add(company)
            if not company.crunchbase:
                if _find_and_set_url(company, "url for crunchbase", set_attr="crunchbase"):
                    session.add(company)

            current_ts = datetime.now(tz=UTC)
            if current_ts - start_ts > timedelta(seconds=TIME_BUDGET):
                session.commit()  # Commit any outstanding records
                logger.info(f"{TIME_BUDGET=} exceeded")
                break

        session.commit()

        stmt = select(Opportunity, CompanyRecord).join(CompanyRecord).limit(ITEM_BUDGET / 2)
        opportunities_to_update = session.exec(stmt).all()

        for idx, opportunity_and_company in enumerate(opportunities_to_update):
            (opportunity, company) = opportunity_and_company
            # Realistically, what can I REST API, google, scrape, or LLM?
            logger.info(f"Opportunity #{idx+1} {opportunity.name} @{company.name}")
            if not opportunity.url:  # or company.url_reported_wrong > 3:
                logger.debug("Opportunity for company webiste")
                if _find_and_set_url(opportunity, "{opportunity.name} job description url"):
                    session.add(opportunity)

            current_ts = datetime.now(tz=UTC)
            if current_ts - start_ts > timedelta(seconds=TIME_BUDGET):
                logger.info(f"{TIME_BUDGET=} exceeded")
                break

        session.commit()


if __name__ == "__main__":
    do_feed_run()
