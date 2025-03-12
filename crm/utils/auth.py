import jwt
import os
from pathlib import Path
import click
from functools import wraps
from dotenv import load_dotenv
from crm.models.users_model import User
from crm.repositories.user_repository import UserRepository
from crm.database.base import SessionLocal


# Charger les variables d'environnement
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY est manquant. Ajoutez-le dans le fichier .env")

# Fichier où stocker le token localement
BASE_DIR = Path(__file__).resolve().parent.parent  # Va remonter au dossier 'crm'
TOKEN_FILE = BASE_DIR / "utils" / "auth_token.txt"


def save_token(token):
    """Sauvegarde le token JWT dans un fichier local"""
    with open(TOKEN_FILE, "w") as file:
        file.write(token)


def load_token():
    """Charge le token JWT depuis le fichier local"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            return file.read().strip()
    return None


def requires_auth(required_roles=None, read_only=False):
    """
    Décorateur pour gérer l'authentification et les permissions des utilisateurs.

    - `required_roles`: Liste des `departments_id` autorisés (ex: [1, 2, 3]).
    - `read_only`: Si `True`, permet l'accès à tous les utilisateurs en lecture seule.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = load_token()

            if not token:
                click.echo(
                    "[bold red]Erreur : Vous devez vous authentifier avec `python main.py login`.[/bold red]"
                )
                return

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                user_id = payload.get("user_id")
                user_department = payload.get("departments_id")

                # Vérifier si l'utilisateur existe en base
                session = SessionLocal()
                user_repo = UserRepository(session)
                user = user_repo.get_by_id(user_id)
                session.close()

                if not user:
                    click.echo("[bold red]Erreur : Utilisateur introuvable.[/bold red]")
                    return

                # Lecture seule autorisée pour tous
                if read_only:
                    return f(*args, **kwargs, user=user)

                # Vérification stricte des permissions
                if required_roles and user_department not in required_roles:
                    click.echo(
                        "[bold red]Accès refusé : Vous n'avez pas les permissions nécessaires.[/bold red]"
                    )
                    return

                return f(*args, **kwargs, user=user)

            except jwt.ExpiredSignatureError:
                click.echo(
                    "[bold red]Erreur : Le token a expiré. Veuillez vous reconnecter.[/bold red]"
                )
            except jwt.InvalidTokenError:
                click.echo(
                    "[bold red]Erreur : Token invalide. Veuillez vous reconnecter.[/bold red]"
                )

        return decorated_function

    return decorator


def get_current_user():
    """Retourne l'utilisateur connecté actuellement."""
    try:
        with SessionLocal() as session:
            user_id = getattr(session, "current_user_id", None)
            if user_id:
                return session.query(User).filter(User.id == user_id).first()
    except Exception as e:
        print(f"Erreur lors de la récupération de l'utilisateur actuel : {e}")
        return None
