import pytest
from crm.models.companies_model import Company

def test_create_company(test_session):
    company = Company(title="company test", siret=1234567891234)
    test_session.add(company)
    test_session.commit()

    assert company.id is not None
    assert company.title == "company test"

def test_update_company(test_session):
    company = test_session.query(Company).first()
    if company:
        company.title = "Updated company"
        test_session.commit()
        assert company.title == "Updated company"

def test_delete_company(test_session):
    company = test_session.query(Company).first()
    if company:
        test_session.delete(company)
        test_session.commit()
        assert test_session.query(Company).filter_by(id=company.id).first() is None
