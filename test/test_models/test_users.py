import pytest
from sqlalchemy.exc import IntegrityError
from crm.models.users_model import User

def test_create_user(new_user):
    assert new_user.id is not None
    assert new_user.email == "john.doe@email.com"

def test_update_user(test_session, new_user):
    new_user.username = "john_updated"
    test_session.commit()
    assert new_user.username == "john_updated"

def test_delete_user(test_session, new_user):
    test_session.delete(new_user)
    test_session.commit()
    assert test_session.query(User).filter_by(id=new_user.id).first() is None

def test_unique_user_email(test_session):
    user1 = User(email="unique@email.com", username="user1", password="pass", departments_id=1)
    test_session.add(user1)
    test_session.commit()

    user2 = User(email="unique@email.com", username="user2", password="pass", departments_id=1)
    test_session.add(user2)

    with pytest.raises(IntegrityError):
        test_session.commit()
