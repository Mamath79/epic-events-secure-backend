import pytest
from crm.database.base import engine


def test_connection_database():
    """
    Verifie la connection à la base de données est bien établie.
    """
    try:
        with engine.connect() as connection:
            assert connection is not None
            print("Success !")
        
    except Exception as e:
        pytest.fail(f'La connexion a echoué.')
