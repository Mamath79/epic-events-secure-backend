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
        elif choice == 0:
            log_info("Retour au menu principal")
            break
        else:
            log_error(f"Option invalide sélectionnée : {choice}")
            click.echo("Option invalide, veuillez réessayer.")


@requires_auth(required_roles=[1, 2, 3])
def list_all_users(user):
    """
    Affiche la liste des utilisateurs.
    """
    session = SessionLocal()
    service = UserService(session)
    try:
        users = service.get_all()
        if users:
            UserView.display_users(users)
        else:
            click.echo("\n[bold yellow]Aucun utilisateur trouvé.[/bold yellow]")
    except Exception as e:
        log_error(f"\n[bold red]Erreur lors de la récupération des utilisateurs : {e} [/bold red]")
        capture_exception(e)
        click.echo("\n[bold red]Une erreur est survenue lors de l'affichage des utilisateurs.[/bold red]")
    finally:
        session.close()


@requires_auth(required_roles=[1, 2, 3])
def get_user_by_id(user):
    """
    Affiche les détails d'un utilisateur par ID.
    """

    user_id = click.prompt("\n[cyan bold]Entrez l'ID de l'utilisateur[/cyan bold]", type=int)

    session = SessionLocal()
    service = UserService(session)
    try:
        user = service.get_by_id(user_id)
        if user:
            UserView.display_user(user)
        else:
            click.echo("Utilisateur introuvable.")
    except Exception as e:
        log_error(f"\n[bold red]Erreur lors de la récupération de l'utilisateur {user_id} : {e}[/bold red]")
        capture_exception(e)
        click.echo("\n[bold red]Une erreur est survenue.[/bold red]")
    finally:
        session.close()


@requires_auth(required_roles=[1])
def create_user(user):
    """
    Ajoute un nouvel utilisateur.
    """
    data = UserView.prompt_user_data()

    session = SessionLocal()
    service = UserService(session)
    try:
        new_user = service.create(data)
        log_info(
            f"[bold green]Utilisateur {new_user.first_name} {new_user.last_name} créé avec succès ![/bold green]"
        )
        click.echo(
            f"[bold green]Utilisateur {new_user.first_name} {new_user.last_name} ajouté avec succès ![/bold green]"
        )
    except Exception as e:
        log_error(f"\n[bold red]Erreur lors de la création de l'utilisateur : {e}[/bold red]")
        capture_exception(e)
        click.echo("\n[bold red]Erreur lors de la création de l'utilisateur.[/bold red]")
    finally:
        session.close()


@requires_auth(required_roles=[1])
def update_user(user):
    """
    Met à jour un utilisateur existant avec un menu interactif.
    """
    user_id = click.prompt("Entrez l'ID de l'utilisateur à modifier", type=int)

    session = SessionLocal()
    service = UserService(session)
    try:
        user = service.get_by_id(user_id)
        if not user:
            click.echo("\n[bold yellow]Utilisateur introuvable.[/bold yellow]")
            return

        update_data = UserView.prompt_user_update(user)
        updated_user = service.update(user_id, update_data)

        log_info(
            f"[bold green]Utilisateur {updated_user.first_name} {updated_user.last_name} mis à jour !.[/bold green]"
        )
        click.echo(
            f"[bold green]Utilisateur {updated_user.first_name} {updated_user.last_name} mis à jour ![/bold green]"
        )

    except Exception as e:
        log_error(f"\n[bold red]Erreur lors de la mise à jour de l'utilisateur {user_id} : {e}[/bold red]")
        capture_exception(e)
        click.echo("\n[bold red]Une erreur est survenue.[/bold red]")
    finally:
        session.close()


@requires_auth(required_roles=[1])
def delete_user(user):
    """
    Supprime un utilisateur avec confirmation.
    """
    user_id = click.prompt("Entrez l'ID de l'utilisateur à supprimer", type=int)

    session = SessionLocal()
    service = UserService(session)
    try:
        user = service.get_by_id(user_id)
        if not user:
            click.echo("[bold yellow]Utilisateur introuvable.[/bold yellow]")
            return

        confirm = click.confirm(
            f"[bold yellow]Voulez-vous vraiment supprimer {user.first_name} {user.last_name} ?[/bold yellow]",
            default=False,
        )
        if confirm:
            service.delete(user_id)
            log_info(f"[bold green]Utilisateur {user.first_name} {user.last_name} supprimé.[/bold green]")
            click.echo("[bold green]Utilisateur supprimé avec succès.[/bold green]")
        else:
            click.echo("[bold yellow]Suppression annulée.[/bold yellow]")
    except Exception as e:
        log_error(f"[bold red]Erreur lors de la suppression de l'utilisateur {user_id} : {e}[/bold red]")
        capture_exception(e)
        click.echo("[bold red]Une erreur est survenue.[/bold red]")
    finally:
        session.close()
