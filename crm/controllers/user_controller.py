import click
from crm.database.base import SessionLocal
from crm.services.user_service import UserService
from crm.views.user_view import UserView
from crm.utils.auth import requires_auth


@click.command()
def user_menu():
    print("Menu de gestion des évenements")

@click.group()
def user():
    """Gestion des utilisateurs"""
    pass

@click.command()
@requires_auth(required_roles=[3])  # Gestion uniquement
def list_users():
    """Affiche la liste des utilisateurs"""
    db_session = SessionLocal()
    user_service = UserService(db_session)
    users = user_service.get_all()
    db_session.close()

    UserView.display_users(users)

@click.command()
@requires_auth(required_roles=[3])  # Gestion uniquement
def create_user():
    """Ajoute un nouvel utilisateur"""
    user_data = UserView.prompt_create_user()

    db_session = SessionLocal()
    user_service = UserService(db_session)

    new_user = user_service.create(user_data)
    db_session.close()

    UserView.show_user_creation(new_user)

@click.command()
@requires_auth(required_roles=[3])  # Gestion uniquement
def update_user():
    """Met à jour un utilisateur"""
    update_data = UserView.prompt_update_user()

    db_session = SessionLocal()
    user_service = UserService(db_session)

    updated_user = user_service.update(update_data["user_id"], update_data)
    db_session.close()

    UserView.show_user_update(updated_user)

@click.command()
@requires_auth(required_roles=[3])  # Gestion uniquement
def delete_user():
    """Supprime un utilisateur"""
    user_id = UserView.prompt_delete_user()

    db_session = SessionLocal()
    user_service = UserService(db_session)

    user_service.delete(user_id)
    db_session.close()

    UserView.show_user_deletion(user_id)

# Ajouter les commandes au groupe user
user.add_command(list_users)
user.add_command(create_user)
user.add_command(update_user)
user.add_command(delete_user)
