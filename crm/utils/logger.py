import sentry_sdk
import os
import logging
from dotenv import load_dotenv
from crm.utils.auth import get_current_user

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé DSN depuis le fichier .env
SENTRY_DSN = os.getenv("SENTRY_DSN")

# Initialisation de Sentry
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        send_default_pii=True,  # Capture les infos utilisateur
        traces_sample_rate=1.0,  # Capture toutes les transactions (logs détaillés)
    )
else:
    print("SENTRY_DSN non trouvé dans .env")

# Configuration du logging standard Python
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def log_info(message):
    """Log un message d'information uniquement si l'utilisateur n'est pas de Type 2."""
    user = get_current_user()  # Récupère l'utilisateur connecté

    if user and user.departments_id != 2:  # Bloque les logs pour les utilisateurs Support
        logger.info(message)


def log_error(message):
    """Log un message d'erreur uniquement si l'utilisateur n'est pas de Type 2."""
    user = get_current_user()

    if user and user.departments_id != 2:
        logger.error(message)
    sentry_sdk.capture_exception(Exception(message))  # Toujours envoyer les erreurs à Sentry


def log_warning(message):
    """Log un message d'avertissement uniquement si l'utilisateur n'est pas de Type 2."""
    user = get_current_user()

    if user and user.departments_id != 2:
        logger.warning(message)
