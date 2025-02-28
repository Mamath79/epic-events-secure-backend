import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from crm.services.base_service import BaseService
from crm.repositories.user_repository import UserRepository
from crm.models.users_model import User
from crm.utils.auth import save_token


# Charger les variables d'environnement
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("SECRET_KEY est manquant. Ajoutez-le dans le fichier .env")

class UserService(BaseService):
    def __init__(self, session):
        super().__init__(UserRepository(session))

    def authenticate(self, email, password):
        """ Vérifie les identifiants et génère un token JWT """
        user = self.repository.session.query(User).filter_by(email=email).first()
        if not user or not user.check_password(password):
            return None  # Authentification échouée

        # Générer un token JWT
        payload = {
            "user_id": user.id,
            "email": user.email,
            "departments_id": user.departments_id,
            "exp": datetime.utcnow() + timedelta(hours=2)  # Expiration en 2h
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        # Sauvegarder le token
        save_token(token)

        return token

    def get_users_by_department(self, department_id):
        """ Récupère tous les utilisateurs d'un département donné. """
        return self.repository.session.query(self.repository.model).filter_by(departments_id=department_id).all()

