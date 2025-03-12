import click
from sentry_sdk import capture_exception
from crm.views.user_view import UserView
from crm.services.user_service import UserService
from crm.database.base import SessionLocal
from crm.utils.auth import requires_auth
from crm.utils.logger import log_info, log_error


def user_menu():
    """
    Menu interactif pour la gestion des utilisateurs.
    """
    while True:
        UserView.show_menu()
        choice = click.prompt("Sélectionnez une option", type=int)

        if choice == 1:
            log_info("Consultation de tous les utilisateurs")
            list_all_users()
        elif choice == 2:
            log_info("Consultation d'un utilisateur par ID")
            get_user_by_id()
        elif choice == 3:
            log_info("Création d'un nouvel utilisateur")
            create_user()
        elif choice == 4:
            log_info("Mise à jour d'un utilisateur")
            update_user()
        elif choice == 5:
            log_info("Suppression d'un utilisateur")
            delete_user()
        elif choice == 6:
            log_info("Filtrage des utilisateurs")
            filter_users()
        elif choice == 0:
            log_info("Retour au menu principal")
            break
        else:
            log_error(f"Option invalide sélectionnée : {choice}")
            click.secho("Option invalide, veuillez réessayer.", fg="red", bold=True)


@requires_auth(required_roles=[1, 2, 3])
def list_all_users(user):
    """
    Affiche la liste des utilisateurs.
    """
    try:
        with SessionLocal() as session:
            service = UserService(session)
            users = service.get_all()
            if users:
                UserView.display_users(users)
            else:
                click.secho("Aucun utilisateur trouvé.", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la récupération des utilisateurs : {e}")
        capture_exception(e)
        click.secho("Une erreur est survenue lors de l'affichage des utilisateurs.", fg="red", bold=True)


@requires_auth(required_roles=[1, 2, 3])
def get_user_by_id(user):
    """
    Affiche les détails d'un utilisateur par ID.
    """
    user_id = click.prompt("Entrez l'ID de l'utilisateur", type=int)

    try:
        with SessionLocal() as session:
            service = UserService(session)
            user = service.get_by_id(user_id)
            if user:
                UserView.display_user(user)
            else:
                click.secho("Utilisateur introuvable.", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la récupération de l'utilisateur {user_id} : {e}")
        capture_exception(e)
        click.secho("Une erreur est survenue.", fg="red", bold=True)


@requires_auth(required_roles=[1])
def create_user(user):
    """
    Ajoute un nouvel utilisateur.
    """
    data = UserView.prompt_user_data()

    try:
        with SessionLocal() as session:
            service = UserService(session)
            new_user = service.create(data)
            log_info(f"Utilisateur {new_user.first_name} {new_user.last_name} créé avec succès.")
            click.secho(f"Utilisateur {new_user.first_name} {new_user.last_name} ajouté avec succès !", fg="green", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la création de l'utilisateur : {e}")
        capture_exception(e)
        click.secho("Erreur lors de la création de l'utilisateur.", fg="red", bold=True)


@requires_auth(required_roles=[1])
def update_user(user):
    """
    Met à jour un utilisateur existant avec un menu interactif.
    """
    user_id = click.prompt("Entrez l'ID de l'utilisateur à modifier", type=int)

    try:
        with SessionLocal() as session:
            service = UserService(session)
            user = service.get_by_id(user_id)
            if not user:
                click.secho("Utilisateur introuvable.", fg="yellow", bold=True)
                return

            update_data = UserView.prompt_user_update(user)
            updated_user = service.update(user_id, update_data)

            log_info(f"Utilisateur {updated_user.first_name} {updated_user.last_name} mis à jour.")
            click.secho(f"Utilisateur {updated_user.first_name} {updated_user.last_name} mis à jour !", fg="green", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la mise à jour de l'utilisateur {user_id} : {e}")
        capture_exception(e)
        click.secho("Une erreur est survenue.", fg="red", bold=True)


@requires_auth(required_roles=[1])
def delete_user(user):
    """
    Supprime un utilisateur avec confirmation.
    """
    user_id = click.prompt("Entrez l'ID de l'utilisateur à supprimer", type=int)

    try:
        with SessionLocal() as session:
            service = UserService(session)
            user = service.get_by_id(user_id)
            if not user:
                click.secho("Utilisateur introuvable.", fg="yellow", bold=True)
                return

            confirm = click.confirm(f"Voulez-vous vraiment supprimer {user.first_name} {user.last_name} ?", default=False)
            if confirm:
                service.delete(user_id)
                log_info(f"Utilisateur {user.first_name} {user.last_name} supprimé.")
                click.secho("Utilisateur supprimé avec succès.", fg="green", bold=True)
            else:
                click.secho("Suppression annulée.", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la suppression de l'utilisateur {user_id} : {e}")
        capture_exception(e)
        click.secho("Une erreur est survenue.", fg="red", bold=True)


@requires_auth(read_only=True)
def filter_users(user):
    """
    Filtre les utilisateurs en fonction des critères choisis.
    """
    try:
        filters = UserView.prompt_user_filters()
        with SessionLocal() as session:
            service = UserService(session)
            users = service.get_all_filtered(filters)
            if users:
                UserView.display_users(users)
            else:
                click.secho("Aucun utilisateur trouvé avec ces critères.", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors du filtrage des utilisateurs : {str(e)}")
        capture_exception(e)
        click.secho("Une erreur s'est produite. Veuillez réessayer.", fg="red", bold=True)
