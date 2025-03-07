import click
from sentry_sdk import capture_exception
from crm.services.department_service import DepartmentService
from crm.database.base import SessionLocal
from crm.views.department_view import DepartmentView
from crm.utils.auth import requires_auth
from crm.utils.logger import log_info, log_error

def department_menu():
    """Menu interactif pour la gestion des départements."""
    while True:
        DepartmentView.show_menu()
        choice = click.prompt("Sélectionnez une option", type=int)

        if choice == 1:
            log_info("Consultation de tous les départements")
            list_all_departments()
        elif choice == 2:
            log_info("Consultation d'un département par ID")
            get_department_by_id()
        elif choice == 3:
            log_info("Création d'un département")
            create_department()
        elif choice == 4:
            log_info("Mise à jour d'un département")
            update_department()
        elif choice == 5:
            log_info("Suppression d'un département")
            delete_department()
        elif choice == 0:
            log_info("Retour au menu principal")
            break
        else:
            log_error(f"Option invalide sélectionnée : {choice}")
            click.echo("Option invalide, veuillez réessayer.")

@requires_auth(read_only=True)
def list_all_departments(user):
    """Affiche la liste des départements."""
    with SessionLocal() as session:
        service = DepartmentService(session)
        try:
            departments = service.get_all()
            DepartmentView.display_departments(departments) if departments else click.echo("Aucun département trouvé.")
        except Exception as e:
            log_error(f"Erreur lors de la récupération des départements : {e}")
            capture_exception(e)
            click.echo("Une erreur est survenue lors de l'affichage des départements.")

@requires_auth(read_only=True)
def get_department_by_id(user):
    """Affiche les détails d'un département par ID."""
    department_id = click.prompt("Entrez l'ID du département", type=int)
    with SessionLocal() as session:
        service = DepartmentService(session)
        try:
            department = service.get_by_id(department_id)
            DepartmentView.display_department(department) if department else click.echo("Département introuvable.")
        except Exception as e:
            log_error(f"Erreur lors de la récupération du département {department_id} : {e}")
            capture_exception(e)
            click.echo("Une erreur est survenue.")

@requires_auth(required_roles=[1])
def create_department(user):
    """Ajoute un nouveau département."""
    data = DepartmentView.prompt_department_data()
    with SessionLocal() as session:
        service = DepartmentService(session)
        try:
            new_department = service.create(data)
            log_info(f"Département {new_department.name} créé avec succès !")
            click.echo(f"Département {new_department.name} ajouté avec succès !")
        except Exception as e:
            log_error(f"Erreur lors de la création du département : {e}")
            capture_exception(e)
            click.echo("Erreur lors de la création du département.")

@requires_auth(required_roles=[1])
def update_department(user):
    """Met à jour un département existant."""
    department_id = click.prompt("Entrez l'ID du département à modifier", type=int)
    with SessionLocal() as session:
        service = DepartmentService(session)
        try:
            department = service.get_by_id(department_id)
            if not department:
                click.echo("Département introuvable.")
                return
            update_data = DepartmentView.prompt_department_update(department)
            updated_department = service.update(department_id, update_data)
            log_info(f"Département {updated_department.name} mis à jour.")
            click.echo(f"Département {updated_department.name} mis à jour !")
        except Exception as e:
            log_error(f"Erreur lors de la mise à jour du département {department_id} : {e}")
            capture_exception(e)
            click.echo("Une erreur est survenue.")

@requires_auth(required_roles=[1])
def delete_department(user):
    """Supprime un département."""
    department_id = click.prompt("Entrez l'ID du département à supprimer", type=int)
    with SessionLocal() as session:
        service = DepartmentService(session)
        try:
            department = service.get_by_id(department_id)
            if not department:
                click.echo("Département introuvable.")
                return
            confirm = click.confirm(f"Voulez-vous vraiment supprimer {department.name} ?", default=False)
            if confirm:
                service.delete(department_id)
                log_info(f"Département {department.name} supprimé.")
                click.echo("Département supprimé avec succès.")
            else:
                click.echo("Suppression annulée.")
        except Exception as e:
            log_error(f"Erreur lors de la suppression du département {department_id} : {e}")
            capture_exception(e)
            click.echo("Une erreur est survenue.")
