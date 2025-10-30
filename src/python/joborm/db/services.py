from models import Company, Opportunity, Process, ProcessItem


def update_company(session, company: Company):
    session.add(company)


def update_opportunity(session, opportunity: Opportunity):
    session.add(opportunity)


def update_process(session, process: Process):
    session.add(process)


def update_process_item(session, process_item: ProcessItem):
    session.add(process_item)
