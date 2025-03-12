import pytest
from crm.database.base import engine
from crm.utils.logger import log_error


def test_connection_database():
    """
    Verifie la connection à la base de données est bien établie.
    """
    try:
        with engine.connect() as connection:
            assert connection is not None
            print("Success !")

    except Exception as e:
        log_error(f"Erreur de connexion à la base de données : {str(e)}")
        pytest.fail("La connexion a échoué.")
