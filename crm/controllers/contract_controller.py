import click
from sentry_sdk import capture_exception
from crm.views.contract_view import ContractView
from crm.services.contract_service import ContractService
from crm.database.base import SessionLocal
from crm.utils.auth import requires_auth
from crm.utils.logger import log_error, log_info


def contract_menu():
    """
    Menu interactif pour la gestion des contrats.
    """
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
        elif choice == 0:
            log_info("Retour au menu principal")
            break
        else:
            log_error(f"Option invalide sélectionnée : {choice}")
            click.echo("\n[bold red]Option invalide, veuillez réessayer.[/bold red]")


@requires_auth(read_only=True)
def list_all_contracts(user):
    """
    Affiche la liste de tous les contrats.
    """
    session = SessionLocal()
    service = ContractService(session)
    try:
        contracts = service.get_all()
        if contracts:
            ContractView.display_contracts(contracts)
        else:
            click.echo("\n[bold yellow]Aucun contrat trouvé.[/bold yellow]")
    except Exception as e:
        log_error(f"\n[bold red]Erreur lors de la récupération des contrats : {e} [/bold red]")
        capture_exception(e)
        click.echo("\n[bold red]Une erreur est survenue lors de l'affichage des contrats.[/bold red]")
    finally:
        session.close()


@requires_auth(read_only=True)
def get_contract_by_id(user):
    """
    Affiche les détails d'un contrat par ID.
    """
    contract_id = click.prompt("\n[bold cyan]Entrez l'ID du contrat[/bold cyan]", type=int)

    session = SessionLocal()
    service = ContractService(session)
    try:
        contract = service.get_by_id(contract_id)
        if contract:
            ContractView.display_contract(contract)
        else:
            click.echo("\n[bold yellow]Contrat introuvable.[/bold yellow]")
    except Exception as e:
        log_error(f"\n[bold red]Erreur lors de la récupération du contrat {contract_id} : {e}[/bold red]")
        capture_exception(e)
        click.echo("\n[bold red]Une erreur est survenue.[/bold red]")
    finally:
        session.close()


@requires_auth(required_roles=[1, 3])
def create_contract(user):
    """
    Ajoute un nouveau contrat.
    """
    data = ContractView.prompt_contract_data()
    if not data:
        return  # Annulation si aucune donnée saisie

    session = SessionLocal()
    service = ContractService(session)
    try:
        new_contract = service.create(data)
        log_info(f"[bold green]Contrat {new_contract.id} créé avec succès ![/bold green]")
        click.echo(f"[bold green]Contrat {new_contract.id} ajouté avec succès ![/bold green]")
    except ValueError as e:
        click.echo(f"\n[bold yellow]Erreur de validation : {str(e)}[/bold yellow]")  # Affichage clair des erreurs utilisateur
    except Exception as e:
        log_error(f"\n[bold red]Erreur lors de la création du contrat : {e}[/bold red]")
        capture_exception(e)
        click.echo("\n[bold red]Erreur lors de la création du contrat.[/bold red]")
    finally:
        session.close()


@requires_auth(required_roles=[1, 3])
def update_contract(user):
    """
    Met à jour un contrat existant avec un menu interactif.
    """
    contract_id = click.prompt("\n[bold cyan]Entrez l'ID du contrat à modifier[/bold cyan]", type=int)

    session = SessionLocal()
    service = ContractService(session)
    try:
        contract = service.get_by_id(contract_id)
        if not contract:
            click.echo("\n[bold yellow]Contrat introuvable.[/bold yellow]")
            return

        update_data = ContractView.prompt_contract_update(contract)
        if not update_data:
            return

        updated_contract = service.update(contract_id, update_data)
        log_info(f"[bold green]Contrat {updated_contract.id} mis à jour avec succès ![/bold green]")
        click.echo(f"[bold green]Contrat {updated_contract.id} mis à jour avec succès ![/bold green]")

    except ValueError as e:
        click.echo(f"\n[bold yellow]Erreur de validation : {str(e)}[/bold yellow]")  # Affichage clair des erreurs utilisateur
    except Exception as e:
        log_error(f"\n[bold red]Erreur lors de la mise à jour du contrat {contract_id} : {e}[/bold red]")
        capture_exception(e)
        click.echo("\n[bold red]Une erreur est survenue.[/bold red]")
    finally:
        session.close()


@requires_auth(required_roles=[1, 3])
def delete_contract(user):
    """
    Supprime un contrat avec confirmation.
    """
    contract_id = click.prompt("\n[bold cyan]Entrez l'ID du contrat à supprimer[/bold cyan]", type=int)

    session = SessionLocal()
    service = ContractService(session)
    try:
        contract = service.get_by_id(contract_id)
        if not contract:
            click.echo("\n[bold yellow]Contrat introuvable.[/bold yellow]")
            return

        confirm = click.confirm(
            f"\n[bold yellow]Voulez-vous vraiment supprimer le contrat {contract.id} ?[/bold yellow]",
            default=False,
        )
        if confirm:
            service.delete(contract_id)
            log_info(f"[bold green]Contrat {contract.id} supprimé avec succès.[/bold green]")
            click.echo("\n[bold green]Contrat supprimé avec succès.[/bold green]")
        else:
            click.echo("\n[bold yellow]Suppression annulée.[/bold yellow]")
    except Exception as e:
        log_error(f"\n[bold red]Erreur lors de la suppression du contrat {contract_id} : {e}[/bold red]")
        capture_exception(e)
        click.echo("\n[bold red]Une erreur est survenue.[/bold red]")
    finally:
        session.close()
