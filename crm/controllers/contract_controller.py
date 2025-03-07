import click
from sentry_sdk import capture_exception
from crm.views.contract_view import ContractView
from crm.services.contract_service import ContractService
from crm.database.base import SessionLocal
from crm.utils.auth import requires_auth
from crm.utils.logger import log_error, log_info


def contract_menu():
    """
    Menu de gestion des contrats.
    """
    while True:
        ContractView.show_menu()
        choice = click.prompt("Sélectionnez une option", type=int)

        if choice == 1:
            list_all_contracts()
        elif choice == 2:
            get_contract_by_id()
        elif choice == 3:
            create_contract()
        elif choice == 4:
            update_contract()
        elif choice == 5:
            delete_contract()
        elif choice == 0:
            break
        else:
            click.echo("[red]Option invalide, veuillez réessayer.[/red]")

@requires_auth(read_only=True)  # Tout le monde peut voir
def list_all_contracts(user):
    """Liste tous les contrats."""
    try:
        with SessionLocal() as session:
            service = ContractService(session)
            contracts = service.get_all()

            if contracts:
                ContractView.display_contracts(contracts)
            else:
                click.echo("Aucun contrat trouvé.")

    except Exception as e:
        log_error(f"Erreur lors de la récupération des contrats : {str(e)}")
        capture_exception(e)
        click.echo("⚠️ Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(read_only=True)  # Tout le monde peut voir
def get_contract_by_id(user):
    """Récupère un contrat par son ID."""
    try:
        contract_id = click.prompt("Entrez l'ID du contrat", type=int)

        with SessionLocal() as session:
            service = ContractService(session)
            contract = service.get_by_id(contract_id)

            if contract:
                ContractView.display_contract(contract)
            else:
                click.echo("[red]Contrat introuvable.[/red]")

    except Exception as e:
        log_error(f"Erreur lors de la récupération du contrat {contract_id} : {str(e)}")
        capture_exception(e)
        click.echo("⚠️ Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(required_roles=[1, 3])
def create_contract(user):
    """ Création d'un nouveau contrat. """
    try:
        data = ContractView.prompt_contract_data()

        with SessionLocal() as session:
            service = ContractService(session)
            new_contract = service.create(data)

            log_info(f"Contrat {new_contract.id} créé avec succès.")
            click.echo(f"Contrat {new_contract.id} ajouté avec succès !")

    except ValueError as e:
        click.echo(f"Erreur de validation : {str(e)}")  # Affiche clairement le problème
    except Exception as e:
        log_error(f"Erreur lors de la création du contrat : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")


@requires_auth(required_roles=[1, 3])
def update_contract(user):
    """ Mise à jour d'un contrat existant. """
    try:
        contract_id = click.prompt("Entrez l'ID du contrat à modifier", type=int)

        with SessionLocal() as session:
            service = ContractService(session)
            contract = service.get_by_id(contract_id)

            if not contract:
                click.echo("Contrat introuvable.")
                return

            new_data = ContractView.prompt_contract_update(contract)
            updated_contract = service.update(contract_id, new_data)

            log_info(f"Contrat {updated_contract.id} mis à jour avec succès.")
            click.echo(f"Contrat {updated_contract.id} mis à jour avec succès !")

    except ValueError as e:
        click.echo(f"Erreur de validation : {str(e)}")  # Affiche clairement le problème
    except Exception as e:
        log_error(f"Erreur lors de la mise à jour du contrat {contract_id} : {str(e)}")
        capture_exception(e)
        click.echo("Une erreur s'est produite. Veuillez réessayer.")

@requires_auth(required_roles=[1, 3])  # Gestionnaires et Commerciaux peuvent supprimer
def delete_contract(user):
    """Suppression d'un contrat."""
    try:
        contract_id = click.prompt("Entrez l'ID du contrat à supprimer", type=int)

        with SessionLocal() as session:
            service = ContractService(session)
            contract = service.get_by_id(contract_id)

            if not contract:
                ContractView.display_message("Contrat introuvable.", "error")
                return

            confirm = click.confirm(f"⚠️ Voulez-vous vraiment supprimer le contrat {contract.id} ?", default=False)
            if confirm:
                service.delete(contract_id)
                log_info(f"Contrat {contract.id} supprimé avec succès.")
                ContractView.display_message("Contrat supprimé avec succès.", "success")
            else:
                ContractView.display_message("Suppression annulée.", "info")

    except Exception as e:
        log_error(f"Erreur lors de la suppression du contrat {contract_id} : {str(e)}")
        capture_exception(e)
        click.echo("⚠️ Une erreur s'est produite. Veuillez réessayer.")
