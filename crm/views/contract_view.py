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
        table.add_column("Client ID", style="green")
        table.add_column("Montant", style="yellow")
        table.add_column("Statut", style="magenta")

        for contract in contracts:
            table.add_row(
                str(contract.id),
                str(contract.client_id),
                f"{contract.amount}€",
                "Signé" if contract.is_signed else "Non signé"
            )

        console.print(table)

    @staticmethod
    def display_contract(contract):
        """Affiche les détails d'un contrat."""
        console.print(f"[cyan bold]ID:[/cyan bold] {contract.id}")
        console.print(f"[cyan bold]Client ID:[/cyan bold] {contract.client_id}")
        console.print(f"[cyan bold]Montant:[/cyan bold] {contract.amount}€")
        console.print(f"[cyan bold]Statut:[/cyan bold] {'Signé' if contract.is_signed else 'Non signé'}")

    @staticmethod
    def prompt_contract_data():
        """Demande les informations pour créer un contrat."""
        client_id = Prompt.ask("ID du Client", type=int)
        amount = Prompt.ask("Montant", type=float)
        is_signed = Prompt.ask("Signé (oui/non)", choices=["oui", "non"], default="non") == "oui"

        return {
            "client_id": client_id,
            "amount": amount,
            "is_signed": is_signed
        }

    @staticmethod
    def prompt_contract_update(contract):
        """Demande les nouvelles informations pour modifier un contrat."""
        amount = Prompt.ask("Montant", default=str(contract.amount), type=float)
        is_signed = Prompt.ask("Signé (oui/non)", choices=["oui", "non"], default="oui" if contract.is_signed else "non") == "oui"

        return {
            "amount": amount,
            "is_signed": is_signed
        }
