import uuid

from sqlmodel import select

from db.models import Company, Opportunity, Process, ProcessItem


class CompanySvc:
    @classmethod
    def insert_company(cls, session, company: Company) -> Company:
        session.add(company)
        session.commit()
        session.refresh(company)
        return company

    @classmethod
    def get_by_id(cls, session, company_id: uuid.UUID) -> Company:
        return session.scalars(select(Company).where(Company.id == company_id)).first()

    @classmethod
    def update_company(cls, session, company: Company) -> None:
        session.add(company)
        session.commit()

    @classmethod
    def delete_company(cls, session, company: Company) -> None:
        session.delete(company)
        session.commit()


class OpportunitySvc:
    @classmethod
    def insert_opportunity(cls, session, opportunity: Opportunity) -> Opportunity:
        session.add(opportunity)
        session.commit()
        session.refresh(opportunity)
        return opportunity

    @classmethod
    def get_by_id(cls, session, opportunity_id: uuid.UUID) -> Opportunity:
        return session.scalars(select(Opportunity).where(Opportunity.id == opportunity_id)).first()

    @classmethod
    def update_opportunity(cls, session, opportunity: Opportunity):
        session.add(opportunity)

    @classmethod
    def delete_opportunity(cls, session, opportunity: Opportunity) -> None:
        session.delete(opportunity)
        session.commit()

    @classmethod
    def update_process(cls, session, process: Process):
        session.add(process)

    @classmethod
    def update_process_item(cls, session, process_item: ProcessItem):
        session.add(process_item)
