import uuid

from sqlmodel import delete, select

from db.models import Company, Opportunity, Process, ProcessItem, ProcessItemCreate


class CompanySvc:
    @classmethod
    def insert_company(cls, session, company: Company) -> Company:
        """Create a company record"""
        session.add(company)
        session.flush()
        session.refresh(company)
        return company

    # Use session.get instead
    # @classmethod
    # def get_by_id(cls, session, company_id: uuid.UUID) -> Company:
    #    return session.scalars(select(Company).where(Company.id == company_id)).first()

    @classmethod
    def update_company(cls, session, company: Company) -> Company:
        """Update a company record"""
        session.add(company)
        session.flush()
        session.refresh(company)
        return company

    @classmethod
    def delete_company(cls, session, company: Company) -> None:
        """Delete a company record"""
        session.delete(company)
        session.flush()


class OpportunitySvc:
    @classmethod
    def insert_opportunity(cls, session, opportunity: Opportunity) -> Opportunity:
        """Create an opportunity record"""
        session.add(opportunity)
        session.flush()
        session.refresh(opportunity)
        return opportunity

    # Use session.get instead
    # @classmethod
    # def get_by_id(cls, session, opportunity_id: uuid.UUID) -> Opportunity:
    #    return session.scalars(select(Opportunity).where(Opportunity.id == opportunity_id)).first()

    @classmethod
    def update_opportunity(cls, session, opportunity: Opportunity):
        """Update an opportunity record"""
        session.add(opportunity)
        session.flush()
        session.refresh(opportunity)

    @classmethod
    def delete_opportunity(cls, session, opportunity: Opportunity) -> None:
        """Delete an opportunity record"""
        session.delete(opportunity)
        session.flush()


class ProcessSvc:
    @classmethod
    def insert_process(cls, session, process: Process) -> Process:
        """Create a process record"""
        session.add(process)
        session.flush()
        session.refresh(process)
        return process

    @classmethod
    def update_process(cls, session, process: Process):
        """Update a process record"""
        session.add(process)
        session.flush()
        session.refresh(process)
        return process

    @classmethod
    def delete_process(cls, session, process: Process) -> None:
        """Delete a company record"""
        session.delete(process)
        session.flush()

    @classmethod
    def insert_process_item(cls, session, process_item: ProcessItemCreate):
        """Create a process item record"""
        session.add(process_item)
        session.flush()
        session.refresh(process_item)
        return process_item

    @classmethod
    def get_process_items(cls, session, process_id: uuid.UUID):
        return session.scalars(
            select(ProcessItem).where(ProcessItem.process_id == process_id)
        ).all()

    @classmethod
    def delete_process_items(cls, session, process_id: uuid.UUID):
        return session.execute(delete(ProcessItem).where(ProcessItem.process_id == process_id))
