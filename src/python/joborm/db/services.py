from db.models import Company, Opportunity, Process, ProcessItem


class CompanySvc:
    @classmethod
    def insert_company(cls, session, company: Company) -> Company:
        """Create a company record"""
        session.add(company)
        session.commit()
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
        session.commit()
        session.refresh(company)
        return company

    @classmethod
    def delete_company(cls, session, company: Company) -> None:
        """Delete a company record"""
        session.delete(company)
        session.commit()


class OpportunitySvc:
    @classmethod
    def insert_opportunity(cls, session, opportunity: Opportunity) -> Opportunity:
        """Create an opportunity record"""
        session.add(opportunity)
        session.commit()
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
        session.commit()
        session.refresh(opportunity)

    @classmethod
    def delete_opportunity(cls, session, opportunity: Opportunity) -> None:
        """Delete an opportunity record"""
        session.delete(opportunity)
        session.commit()

    @classmethod
    def update_process(cls, session, process: Process):
        session.add(process)

    @classmethod
    def update_process_item(cls, session, process_item: ProcessItem):
        session.add(process_item)
