import click
from crm.views.user_view import UserView
from crm.services.user_service import UserService
from crm.database.base import SessionLocal
from crm.utils.auth import requires_auth

def user_menu():
    """
    Menu interactif pour la gestion des utilisateurs.
    """
    while True:
        UserView.show_menu()
        choice = click.prompt("Sélectionnez une option", type=int)

        if choice == 1:
            list_all_users()
        elif choice == 2:
            get_user_by_id()
        elif choice == 3:
            create_user()
        elif choice == 4:
            update_user()
        elif choice == 5:
            delete_user()
        elif choice == 0:
            break
        else:
            click.echo("❌ Option invalide, veuillez réessayer.")

@requires_auth(required_roles=[1, 2, 3])
def list_all_users(user):
    """Affiche la liste des utilisateurs."""
    session = SessionLocal()
    service = UserService(session)
    users = service.get_all()
    session.close()

    if users:
        UserView.display_users(users)
    else:
        click.echo("Aucun utilisateur trouvé.")

@requires_auth(required_roles=[1, 2, 3])
def get_user_by_id(user):
    """Affiche les détails d'un utilisateur par ID."""
    user_id = click.prompt("Entrez l'ID de l'utilisateur", type=int)
    
    session = SessionLocal()
    service = UserService(session)
    user = service.get_by_id(user_id)
    session.close()

    if user:
        UserView.display_user(user)
    else:
        click.echo("Utilisateur introuvable.")

@requires_auth(required_roles=[1])
def create_user(user):
    """Ajoute un nouvel utilisateur."""
    data = UserView.prompt_user_data()

    session = SessionLocal()
    service = UserService(session)
    try:
        new_user = service.create(data)
        session.close()
        click.echo(f"Utilisateur {new_user.first_name} {new_user.last_name} ajouté avec succès !")
    except Exception as e:
        click.echo(f"Erreur lors de la création de l'utilisateur : {e}")

@requires_auth(required_roles=[1])
def update_user(user):
    """Met à jour un utilisateur existant avec un menu interactif."""
    user_id = click.prompt("Entrez l'ID de l'utilisateur à modifier", type=int)
    
    session = SessionLocal()
    service = UserService(session)
    user = service.get_by_id(user_id)

    if not user:
        session.close()
        click.echo("Utilisateur introuvable.")
        return

    update_data = UserView.prompt_user_update(user)

    try:
        updated_user = service.update(user_id, update_data)
        session.close()
        click.echo(f"Utilisateur {updated_user.first_name} {updated_user.last_name} mis à jour !")
    except Exception as e:
        click.echo(f"Erreur lors de la mise à jour : {e}")

@requires_auth(required_roles=[1])
def delete_user(user):
    """Supprime un utilisateur avec confirmation."""
    user_id = click.prompt("Entrez l'ID de l'utilisateur à supprimer", type=int)

    session = SessionLocal()
    service = UserService(session)
    user = service.get_by_id(user_id)

    if not user:
        session.close()
        click.echo("Utilisateur introuvable.")
        return

    confirm = click.confirm(f"Voulez-vous vraiment supprimer {user.first_name} {user.last_name} ?", default=False)
    if confirm:
        service.delete(user_id)
        session.close()
        click.echo("Utilisateur supprimé avec succès.")
    else:
        session.close()
        click.echo("Suppression annulée.")
