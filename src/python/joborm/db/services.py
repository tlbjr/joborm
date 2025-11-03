import uuid

from sqlmodel import delete, select

from db.models import (
    CompanyCreate,
    CompanyPublic,
    CompanyRecord,
    CompanyUpdate,
    Opportunity,
    Process,
    ProcessItem,
    ProcessItemCreate,
)


class CompanySvc:
    @classmethod
    def insert_company(cls, session, company: CompanyCreate) -> CompanyRecord:
        """Create a company record"""
        company_rec = CompanyRecord.model_validate(company)
        session.add(company_rec)
        session.flush()
        session.refresh(company_rec)
        return company_rec

    @classmethod
    def get_by_id(cls, session, company_id: uuid.UUID) -> CompanyRecord | None:
        """Return a company record by id"""
        return session.scalars(select(CompanyRecord).where(CompanyRecord.id == company_id)).first()

    @classmethod
    def update_company(cls, session, company: CompanyUpdate) -> CompanyPublic:
        """Update a company record"""
        existing_company = cls.get_by_id(session, company.id)
        if existing_company is None:
            return None
        update_data = company.model_dump(exclude_unset=True)
        existing_company.sqlmodel_update(update_data)
        session.add(existing_company)
        session.flush()
        session.refresh(existing_company)
        return existing_company

    @classmethod
    def delete_company(cls, session, company: CompanyUpdate) -> None:
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
