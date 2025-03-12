import click
from sentry_sdk import capture_exception
from crm.views.contract_view import ContractView
from crm.services.contract_service import ContractService
from crm.database.base import SessionLocal
from crm.utils.auth import requires_auth
from crm.utils.logger import log_error, log_info


def contract_menu():
    """Menu interactif pour la gestion des contrats."""
    while True:
        ContractView.show_menu()
        choice = click.prompt("Sélectionnez une option", type=int)

        if choice == 1:
            log_info("Consultation de tous les contrats")
            list_all_contracts()
        elif choice == 2:
            log_info("Consultation d'un contrat par ID")
            get_contract_by_id()
        elif choice == 3:
            log_info("Création d'un contrat")
            create_contract()
        elif choice == 4:
            log_info("Mise à jour d'un contrat")
            update_contract()
        elif choice == 5:
            log_info("Suppression d'un contrat")
            delete_contract()
        elif choice == 6:
            log_info("Consultation par filtres")
            filter_contracts()
        elif choice == 0:
            log_info("Retour au menu principal")
            break
        else:
            log_error(f"Option invalide sélectionnée : {choice}")
            click.secho("Option invalide, veuillez réessayer.", fg="red", bold=True)


@requires_auth(read_only=True)
def list_all_contracts(user):
    """Affiche la liste de tous les contrats."""
    session = SessionLocal()
    service = ContractService(session)
    try:
        contracts = service.get_all()
        if contracts:
            ContractView.display_contracts(contracts)
        else:
            click.secho("Aucun contrat trouvé.", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la récupération des contrats : {e}")
        capture_exception(e)
        click.secho("Une erreur est survenue lors de l'affichage des contrats.", fg="red", bold=True)
    finally:
        session.close()


@requires_auth(read_only=True)
def get_contract_by_id(user):
    """Affiche les détails d'un contrat par ID."""
    contract_id = click.prompt("Entrez l'ID du contrat", type=int)

    session = SessionLocal()
    service = ContractService(session)
    try:
        contract = service.get_by_id(contract_id)
        if contract:
            ContractView.display_contract(contract)
        else:
            click.secho("Contrat introuvable.", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la récupération du contrat {contract_id} : {e}")
        capture_exception(e)
        click.secho("Une erreur est survenue.", fg="red", bold=True)
    finally:
        session.close()


@requires_auth(required_roles=[1, 3])
def create_contract(user):
    """Ajoute un nouveau contrat."""
    data = ContractView.prompt_contract_data()
    if not data:
        return  # Annulation si aucune donnée saisie

    session = SessionLocal()
    service = ContractService(session)
    try:
        new_contract = service.create(data)
        log_info(f"Contrat {new_contract.id} créé avec succès !")
        click.secho(f"Contrat {new_contract.id} ajouté avec succès !", fg="green", bold=True)
    except ValueError as e:
        click.secho(f"Erreur de validation : {str(e)}", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la création du contrat : {e}")
        capture_exception(e)
        click.secho("Erreur lors de la création du contrat.", fg="red", bold=True)
    finally:
        session.close()


@requires_auth(required_roles=[1, 3])
def update_contract(user):
    """Met à jour un contrat existant avec un menu interactif."""
    contract_id = click.prompt("Entrez l'ID du contrat à modifier", type=int)

    session = SessionLocal()
    service = ContractService(session)
    try:
        contract = service.get_by_id(contract_id)
        if not contract:
            click.secho("Contrat introuvable.", fg="yellow", bold=True)
            return

        update_data = ContractView.prompt_contract_update(contract)
        if not update_data:
            return

        updated_contract = service.update(contract_id, update_data)
        log_info(f"Contrat {updated_contract.id} mis à jour avec succès !")
        click.secho(f"Contrat {updated_contract.id} mis à jour avec succès !", fg="green", bold=True)
    except ValueError as e:
        click.secho(f"Erreur de validation : {str(e)}", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la mise à jour du contrat {contract_id} : {e}")
        capture_exception(e)
        click.secho("Une erreur est survenue.", fg="red", bold=True)
    finally:
        session.close()


@requires_auth(required_roles=[1, 3])
def delete_contract(user):
    """Supprime un contrat avec confirmation."""
    contract_id = click.prompt("Entrez l'ID du contrat à supprimer", type=int)

    session = SessionLocal()
    service = ContractService(session)
    try:
        contract = service.get_by_id(contract_id)
        if not contract:
            click.secho("Contrat introuvable.", fg="yellow", bold=True)
            return

        confirm = click.confirm(f"Voulez-vous vraiment supprimer le contrat {contract.id} ?", default=False)
        if confirm:
            service.delete(contract_id)
            log_info(f"Contrat {contract.id} supprimé avec succès.")
            click.secho("Contrat supprimé avec succès.", fg="green", bold=True)
        else:
            click.secho("Suppression annulée.", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors de la suppression du contrat {contract_id} : {e}")
        capture_exception(e)
        click.secho("Une erreur est survenue.", fg="red", bold=True)
    finally:
        session.close()


@requires_auth(read_only=True)
def filter_contracts(user):
    """Filtre les contrats en fonction des critères choisis par l'utilisateur."""
    try:
        filters = ContractView.prompt_contract_filters()  # Demande les critères de filtrage
        with SessionLocal() as session:
            service = ContractService(session)
            contracts = service.get_all_filtered(filters)  # Applique les filtres
            if contracts:
                ContractView.display_contracts(contracts)
            else:
                click.secho("Aucun contrat correspondant trouvé.", fg="yellow", bold=True)
    except Exception as e:
        log_error(f"Erreur lors du filtrage des contrats : {str(e)}")
        capture_exception(e)
        click.secho("Une erreur s'est produite. Veuillez réessayer.", fg="red", bold=True)
