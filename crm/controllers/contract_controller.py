import click
from crm.views.contract_view import ContractView
from crm.services.contract_service import ContractService
from crm.database.base import SessionLocal

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
            click.echo("Option invalide, veuillez réessayer.")

def list_all_contracts():
    """Liste tous les contrats."""
    session = SessionLocal()
    service = ContractService(session)
    contracts = service.get_all()
    session.close()

    if contracts:
        ContractView.display_contracts(contracts)
    else:
        click.echo("Aucun contrat trouvé.")

def get_contract_by_id():
    """Récupère un contrat par son ID."""
    contract_id = click.prompt("Entrez l'ID du contrat", type=int)
    
    session = SessionLocal()
    service = ContractService(session)
    contract = service.get_by_id(contract_id)
    session.close()

    if contract:
        ContractView.display_contract(contract)
    else:
        click.echo("Contrat introuvable.")

def create_contract():
    """Création d'un nouveau contrat."""
    data = ContractView.prompt_contract_data()

    session = SessionLocal()
    service = ContractService(session)
    try:
        new_contract = service.create(data)
        session.close()
        click.echo(f"Contrat {new_contract.id} ajouté avec succès !")
    except Exception as e:
        click.echo(f"Erreur lors de la création du contrat : {e}")

def update_contract():
    """Mise à jour d'un contrat existant."""
    contract_id = click.prompt("Entrez l'ID du contrat à modifier", type=int)
    
    session = SessionLocal()
    service = ContractService(session)
    contract = service.get_by_id(contract_id)

    if not contract:
        session.close()
        click.echo("Contrat introuvable.")
        return

    new_data = ContractView.prompt_contract_update(contract)
    try:
        updated_contract = service.update(contract_id, new_data)
        session.close()
        click.echo(f"Contrat {updated_contract.id} mis à jour !")
    except Exception as e:
        click.echo(f"Erreur lors de la mise à jour : {e}")

def delete_contract():
    """Suppression d'un contrat."""
    contract_id = click.prompt("Entrez l'ID du contrat à supprimer", type=int)

    session = SessionLocal()
    service = ContractService(session)
    contract = service.get_by_id(contract_id)

    if not contract:
        session.close()
        click.echo("Contrat introuvable.")
        return

    confirm = click.confirm(f"Voulez-vous vraiment supprimer le contrat {contract.id} ?", default=False)
    if confirm:
        service.delete(contract_id)
        session.close()
        click.echo("Contrat supprimé avec succès.")
    else:
        session.close()
        click.echo("Suppression annulée.")
