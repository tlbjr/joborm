#!/usr/bin/env python
from datetime import datetime, timedelta, UTC
import os

from sqlmodel import select, Session
import structlog

from db.pg import engine
from db.models import CompanyRecord  # TODO CompanySync


logger = structlog.stdlib.get_logger()

TIME_BUDGET = os.getenv("FEED_TIME_BUDGET", 20)
ITEM_BUDGET = os.getenv("FEED_ITEM_BUDGET", 200)


def find_company_website():
    pass


def find_position_job_description():
    pass


# select(Company).join(CompanySync).where(Company.c.url == None).order_by(CompanySync.c.updated_dt.desc())
def do_feed_run():
    start_ts = datetime.now(tz=UTC)
    current_ts = datetime.now(tz=UTC)

    with Session(engine) as session:
        stmt = select(CompanyRecord).where(CompanyRecord.url.in_(['', None])).limit(ITEM_BUDGET)
        companies_to_update = session.exec(stmt).all()

        for idx, company in enumerate(companies_to_update):
            # Realistically, what can I REST API, google, scrape, or LLM?
            print(idx, company)
            # response = requests.get(company.url)

            current_ts = datetime.now(tz=UTC)
            if current_ts - start_ts > timedelta(seconds=TIME_BUDGET):
                print(f"{TIME_BUDGET=} exceeded")
                break


if __name__ == "__main__":
    do_feed_run()
