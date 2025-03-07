from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

class ContractView:

    @staticmethod
    def show_menu():
        """Affiche le menu de gestion des contrats."""
        console.print("\n[bold cyan]╭───────────────╮[/bold cyan]")
        console.print("[bold cyan]│ Menu Contrats │[/bold cyan]")
        console.print("[bold cyan]╰───────────────╯[/bold cyan]")
        console.print("[1] Lister tous les Contrats")
        console.print("[2] Voir un Contrat par ID")
        console.print("[3] Créer un Contrat")
        console.print("[4] Modifier un Contrat")
        console.print("[5] Supprimer un Contrat")
        console.print("[0] Retour au menu principal")

    @staticmethod
    def display_contracts(contracts):
        """Affiche tous les contrats sous forme de tableau."""
        table = Table(title="Liste des Contrats", show_lines=True)
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Client ID", style="green", justify="center")
        table.add_column("Montant Total (€)", style="yellow", justify="right")
        table.add_column("Montant Payé (€)", style="white", justify="right")
        table.add_column("Statut", style="magenta", justify="center")

        for contract in contracts:
            table.add_row(
                str(contract.id),
                str(contract.clients_id),
                f"{contract.total_amount}€",
                f"{contract.payed_amount}€",
                ContractView.get_status_label(contract.contract_status_id)
            )

        console.print(table)

    @staticmethod
    def display_contract(contract):
        """Affiche les détails d'un contrat."""
        console.print(f"[cyan bold]ID:[/cyan bold] {contract.id}")
        console.print(f"[cyan bold]Client ID:[/cyan bold] {contract.clients_id}")
        console.print(f"[cyan bold]Montant Total:[/cyan bold] {contract.total_amount}€")
        console.print(f"[cyan bold]Montant Total:[/cyan bold] {contract.payed_amount}€")
        console.print(f"[cyan bold]Statut:[/cyan bold] {ContractView.get_status_label(contract.contract_status_id)}")

    @staticmethod
    def prompt_contract_data():
        """Demande les informations pour créer un contrat."""
        clients_id = int(Prompt.ask("ID du Client", default="1"))
        total_amount = float(Prompt.ask("Montant total (€)", default="0"))
        payed_amount = float(Prompt.ask("Montant deja Payé (€)", default="0"))
        
        console.print("\n[bold cyan]📌 Sélectionnez le statut du contrat :[/bold cyan]")
        console.print("[1] En attente de signature")
        console.print("[2] Signé")
        console.print("[3] Annulé")
        contract_status_id = int(Prompt.ask("Choisissez un ID de statut", choices=["1", "2", "3"], default="1"))

        return {
            "clients_id": clients_id,
            "total_amount": total_amount,
            "payed_amount": payed_amount,
            "contract_status_id": contract_status_id
        }

    @staticmethod
    def prompt_contract_update(contract):
        """Demande les nouvelles informations pour modifier un contrat."""
        total_amount = float(Prompt.ask("Montant Total (€)", default=str(contract.total_amount)))
        payed_amount = float(Prompt.ask("Montant Payé(€)", default=str(contract.payed_amount)))

        console.print("\n[bold cyan]📌 Modifier le statut du contrat :[/bold cyan]")
        console.print("[1] En attente de signature")
        console.print("[2] Signé")
        console.print("[3] Annulé")
        contract_status_id = int(Prompt.ask("Choisissez un ID de statut", choices=["1", "2", "3"], default=str(contract.contract_status_id)))

        return {
            "total_amount": total_amount,
            "payed_amount": payed_amount,
            "contract_status_id": contract_status_id
        }

    @staticmethod
    def get_status_label(status_id):
        """Renvoie le libellé du statut en fonction de l'ID."""
        status_labels = {
            1: "En attente de signature",
            2: "Signé",
            3: "Annulé"
        }
        return status_labels.get(status_id, "Inconnu")

    @staticmethod
    def display_message(message, status="info"):
        """Affiche un message avec une couleur adaptée."""
        from rich.console import Console

        console = Console()
        colors = {"info": "cyan", "success": "green", "error": "red", "warning": "yellow"}

        color = colors.get(status, "white")
        console.print(f"[bold {color}]{message}[/bold {color}]")