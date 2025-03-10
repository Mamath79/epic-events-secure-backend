from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()


class ContractView:

    @staticmethod
    def show_menu():
        """Affiche le menu de gestion des contrats."""
        console.print("\n[bold cyan]╭────────────────╮[/bold cyan]")
        console.print("[bold cyan]│  Menu Contrats │[/bold cyan]")
        console.print("[bold cyan]╰────────────────╯[/bold cyan]")
        console.print("\n[1] Lister tous les contrats")
        console.print("[2] Voir un contrat par ID")
        console.print("[3] Créer un contrat")
        console.print("[4] Modifier un contrat")
        console.print("[5] Supprimer un contrat")
        console.print("[0] Retour au menu principal\n")

    @staticmethod
    def display_contracts(contracts):
        """Affiche tous les contrats sous forme de tableau."""
        table = Table(title="\n[bold cyan]Liste des contrats[/bold cyan]\n")

        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Client ID", style="green", justify="center", no_wrap=True)
        table.add_column("Montant Total (€)", style="yellow", justify="right", no_wrap=True)
        table.add_column("Montant Payé (€)", style="white", justify="right", no_wrap=True)
        table.add_column("Statut", style="magenta", justify="center", no_wrap=True)

        for contract in contracts:
            table.add_row(
                str(contract.id),
                str(contract.clients_id),
                f"{contract.total_amount}€",
                f"{contract.payed_amount}€",
                ContractView.get_status_label(contract.contract_status_id),
            )

        # Calcul de la largeur de la table
        table_width = console.measure(table).maximum

        # Affichage dynamique des séparateurs
        console.print("\n" + "═" * table_width, style="bold white")
        console.print(table)
        console.print("\n" + "═" * table_width, style="bold white")

    @staticmethod
    def display_contract(contract):
        """Affiche les détails d'un contrat sous forme de fiche détaillée."""
        contract_details = f"""
        [cyan bold]Fiche Contrat[/cyan bold]

        ─────────────────

        [cyan bold]ID:[/cyan bold] {contract.id}
        [green bold]Client ID:[/green bold] {contract.clients_id}
        [yellow bold]Montant Total:[/yellow bold] {contract.total_amount}€
        [white bold]Montant Payé:[/white bold] {contract.payed_amount}€
        [magenta bold]Statut:[/magenta bold] {ContractView.get_status_label(contract.contract_status_id)}
        """

        console.print(
            Panel.fit(
                contract_details,
                title="\n[bold cyan]Détails Contrat[/bold cyan]",
                style="white",
            )
        )

    @staticmethod
    def prompt_contract_data():
        """Demande les informations pour créer un contrat."""
        console.print("\n[bold cyan]Création d'un nouveau contrat[/bold cyan]")

        clients_id = int(Prompt.ask("\n[bold cyan]ID du Client[/bold cyan]", default="1"))
        total_amount = float(Prompt.ask("[bold cyan]Montant total (€)[/bold cyan]", default="0"))
        payed_amount = float(Prompt.ask("[bold cyan]Montant déjà payé (€)[/bold cyan]", default="0"))

        console.print("\n[bold cyan]Sélectionnez le statut du contrat :[/bold cyan]")
        console.print("[1] En attente de signature")
        console.print("[2] Signé")
        console.print("[3] Annulé")
        contract_status_id = int(
            Prompt.ask(
                "Choisissez un ID de statut", choices=["1", "2", "3"], default="1"
            )
        )

        return {
            "clients_id": clients_id,
            "total_amount": total_amount,
            "payed_amount": payed_amount,
            "contract_status_id": contract_status_id,
        }

    @staticmethod
    def prompt_contract_update(contract):
        """Demande les nouvelles informations pour modifier un contrat."""
        console.print(f"\n[bold cyan]Modification du contrat ID {contract.id}[/bold cyan]")

        total_amount = float(
            Prompt.ask(
                f"Montant Total Actuel : [yellow]{contract.total_amount}€[/yellow] ➝ Nouveau montant total (€)",
                default=str(contract.total_amount),
            )
        )
        payed_amount = float(
            Prompt.ask(
                f"Montant Payé Actuel : [white]{contract.payed_amount}€[/white] ➝ Nouveau montant payé (€)",
                default=str(contract.payed_amount),
            )
        )

        console.print("\n[bold cyan]Modifier le statut du contrat :[/bold cyan]")
        console.print("[1] En attente de signature")
        console.print("[2] Signé")
        console.print("[3] Annulé")
        contract_status_id = int(
            Prompt.ask(
                "Choisissez un ID de statut",
                choices=["1", "2", "3"],
                default=str(contract.contract_status_id),
            )
        )

        return {
            "total_amount": total_amount,
            "payed_amount": payed_amount,
            "contract_status_id": contract_status_id,
        }

    @staticmethod
    def get_status_label(status_id):
        """Renvoie le libellé du statut en fonction de l'ID."""
        status_labels = {1: "En attente de signature", 2: "Signé", 3: "Annulé"}
        return status_labels.get(status_id, "Inconnu")

    @staticmethod
    def display_message(message, msg_type="info"):
        """Affiche un message en fonction du type (success, error, info)."""
        colors = {"success": "green", "error": "red", "info": "cyan"}
        console.print(
            f"[{colors.get(msg_type, 'white')}] {message} [/{colors.get(msg_type, 'white')}]"
        )
