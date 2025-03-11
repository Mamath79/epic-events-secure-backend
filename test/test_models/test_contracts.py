import pytest
from sqlalchemy.exc import IntegrityError
from crm.models.contracts_model import Contract


def test_create_contract(new_contract):
    assert new_contract.id is not None
    assert new_contract.total_amount == 5000


def test_update_contract(test_session, new_contract):
    new_contract.total_amount = 7000
    test_session.commit()
    assert new_contract.total_amount == 7000


def test_delete_contract(test_session, new_contract):
    test_session.delete(new_contract)
    test_session.commit()
    assert test_session.query(Contract).filter_by(id=new_contract.id).first() is None


def test_contract_amount_not_null(test_session, new_client):
    contract = Contract(
        clients_id=new_client.id, contract_status_id=1, total_amount=None
    )
    test_session.add(contract)

    with pytest.raises(IntegrityError):
        test_session.commit()
