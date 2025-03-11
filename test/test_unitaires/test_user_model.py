import pytest
from crm.models.users_model import User
from argon2 import PasswordHasher


@pytest.fixture
def user():
    """
    Fixture pour créer un utilisateur de test.
    """
    u = User(username="test_user", email="test@example.com")
    u.password = "MonSuperMotDePasse123!"
    return u


def test_password_hashing(user):
    """
    Test que le mot de passe est bien hashé.
    """
    assert user._password is not None
    assert user._password.startswith("$argon2id$")


def test_correct_password_verification(user):
    """
    Test que la vérification du bon mot de passe fonctionne.
    """
    assert user.check_password("MonSuperMotDePasse123!") is True


def test_incorrect_password_verification(user):
    """Test que la vérification d'un mauvais mot de passe échoue."""
    assert user.check_password("MauvaisMotDePasse") is False
