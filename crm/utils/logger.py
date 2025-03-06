import sentry_sdk
import os
import logging
from dotenv import load_dotenv

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
    print("⚠️ SENTRY_DSN non trouvé dans .env")

# Configuration du logging standard Python
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def log_info(message):
    """Log un message d'information."""
    logger.info(message)

def log_error(message, exception=None):
    """Log une erreur et l'envoie à Sentry si une exception est fournie."""
    logger.error(message)
    if exception:
        sentry_sdk.capture_exception(exception)
