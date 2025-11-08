import uuid

from sqlmodel import delete, select, Session

from db.models import (
    CompanyCreate,
    CompanyPublic,
    CompanyRecord,
    CompanyUpdate,
    Opportunity,
    Process,
    ProcessItem,
    ProcessItemCreate,
    UserCreate,
    UserPublic,
    UserRecord,
    UserGoogleSSO,
)
from shared import UserFrom


class CompanySvc:
    @classmethod
    def insert_company(cls, session: Session, company: CompanyCreate) -> CompanyRecord:
        """Create a company record"""
        company_rec = CompanyRecord.model_validate(company)
        session.add(company_rec)
        session.flush()
        session.refresh(company_rec)
        return company_rec

    @classmethod
    def get_by_id(cls, session: Session, company_id: uuid.UUID) -> CompanyRecord | None:
        """Return a company record by id"""
        return session.scalars(select(CompanyRecord).where(CompanyRecord.id == company_id)).first()

    @classmethod
    def update_company(cls, session: Session, company: CompanyUpdate) -> CompanyPublic:
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
    def delete_company(cls, session: Session, company: CompanyUpdate) -> None:
        """Delete a company record"""
        session.delete(company)
        session.flush()


class OpportunitySvc:
    @classmethod
    def insert_opportunity(cls, session: Session, opportunity: Opportunity) -> Opportunity:
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
    def update_opportunity(cls, session: Session, opportunity: Opportunity):
        """Update an opportunity record"""
        session.add(opportunity)
        session.flush()
        session.refresh(opportunity)

    @classmethod
    def delete_opportunity(cls, session: Session, opportunity: Opportunity) -> None:
        """Delete an opportunity record"""
        session.delete(opportunity)
        session.flush()


class ProcessSvc:
    @classmethod
    def insert_process(cls, session: Session, process: Process) -> Process:
        """Create a process record"""
        session.add(process)
        session.flush()
        session.refresh(process)
        return process

    @classmethod
    def update_process(cls, session: Session, process: Process):
        """Update a process record"""
        session.add(process)
        session.flush()
        session.refresh(process)
        return process

    @classmethod
    def delete_process(cls, session: Session, process: Process) -> None:
        """Delete a company record"""
        session.delete(process)
        session.flush()

    @classmethod
    def insert_process_item(cls, session: Session, process_item: ProcessItemCreate):
        """Create a process item record"""
        session.add(process_item)
        session.flush()
        session.refresh(process_item)
        return process_item

    @classmethod
    def get_process_items(cls, session: Session, process_id: uuid.UUID):
        return session.scalars(
            select(ProcessItem).where(ProcessItem.process_id == process_id)
        ).all()

    @classmethod
    def delete_process_items(cls, session: Session, process_id: uuid.UUID):
        return session.execute(delete(ProcessItem).where(ProcessItem.process_id == process_id))


class UserSvc:
    @classmethod
    def insert_user(cls, session: Session, user: UserCreate) -> UserPublic:
        """Create a user record"""
        user_rec = UserRecord.model_validate(user)
        session.add(user_rec)
        session.flush()
        session.refresh(user_rec)
        return user_rec

    @classmethod
    def get_by_email(cls, session: Session, email: str) -> UserRecord | None:
        """Return a company record by id"""
        return session.scalars(select(UserRecord).where(UserRecord.email == email)).first()

    @classmethod
    def insert_from_google_sso(cls, session: Session, user: UserGoogleSSO) -> UserRecord:
        """Given a user obj from google, insert it as a UserRecord"""
        user_new = {
            "foreign_id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "display_name": user.display_name,
            "picture": user.picture,
            "user_from": UserFrom.GOOGLE,
        }
        return cls.insert_user(session, user_new)
