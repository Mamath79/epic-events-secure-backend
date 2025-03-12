import jwt
import os
import sentry_sdk
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sentry_sdk import capture_exception
from crm.services.base_service import BaseService
from crm.repositories.user_repository import UserRepository
from crm.models.users_model import User
from crm.utils.auth import save_token
from crm.utils.logger import log_error
from argon2 import PasswordHasher

# Initialiser Argon2
ph = PasswordHasher()

# Charger les variables d'environnement
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY est manquant. Ajoutez-le dans le fichier .env")


class UserService(BaseService):
    def __init__(self, session):
        super().__init__(UserRepository(session))

    def authenticate(self, email, password):
        """
        Vérifie les identifiants de l'utilisateur et génère un token JWT sécurisé.
        """
        try:
            session = self.repository.session
            session.expire_all()  # Évite les problèmes de cache SQLAlchemy

            user = session.query(User).filter_by(email=email).first()

            if not user:
                log_error(f"Tentative de connexion avec un email inconnu : {email}")
                return None  # Empêche la divulgation d'existence de l'email

            # Comparaison correcte du mot de passe haché avec l'entrée utilisateur
            try:
                if not ph.verify(user._password, password):
                    log_error(
                        f"Échec d'authentification : Mot de passe incorrect pour l'utilisateur ID {user.id}"
                    )
                    return None
            except Exception as e:
                log_error(
                    f"Erreur de vérification du mot de passe pour l'utilisateur ID {user.id} : {str(e)}"
                )
                return None

            # Générer un token JWT sécurisé
            payload = {
                "user_id": user.id,
                "email": user.email,
                "departments_id": user.departments_id,
                "exp": datetime.utcnow() + timedelta(hours=2),  # Expiration en 2h
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            # Sauvegarde du token
            save_token(token)

            return token

        except Exception as e:
            log_error(f"Erreur lors de l'authentification : {str(e)}")
            capture_exception(e)  # Envoi à Sentry pour monitoring
            return None  # Empêche les fuites d'erreurs vers l'utilisateur

    def get_users_by_department(self, department_id):
        """
        Récupère tous les utilisateurs d'un département donné.
        """
        try:
            return (
                self.repository.session.query(self.repository.model)
                .filter_by(departments_id=department_id)
                .all()
            )
        except Exception as e:
            log_error(
                f"Erreur lors de la récupération des utilisateurs du département {department_id} : {str(e)}"
            )
            capture_exception(e)
            return []

    def get_all_filtered(self, filters):
        """
        Récupère les utilisateurs en appliquant des filtres dynamiques.
        """
        try:
            query = self.repository.session.query(User).options(
                joinedload(User.department)
            )

            if "last_name" in filters:
                query = query.filter(User.last_name.ilike(f"%{filters['last_name']}%"))
            if "first_name" in filters:
                query = query.filter(
                    User.first_name.ilike(f"%{filters['first_name']}%")
                )
            if "email" in filters:
                query = query.filter(User.email.ilike(f"%{filters['email']}%"))
            if "username" in filters:
                query = query.filter(User.username.ilike(f"%{filters['username']}%"))
            if "departments_id" in filters:
                query = query.filter(User.departments_id == filters["departments_id"])

            return query.all()
        except Exception as e:
            log_error(f"Erreur lors du filtrage des utilisateurs : {str(e)}")
            sentry_sdk.capture_exception(e)
            return []
