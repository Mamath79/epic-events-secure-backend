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
        console.print("[6] Filtrer les Contrats")
        console.print("[0] Retour au menu principal\n")

    @staticmethod
    def display_contracts(contracts):
        """Affiche tous les contrats sous forme de tableau."""
        table = Table(title="\n[bold cyan]Liste des contrats[/bold cyan]\n")

        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Client ID")
        table.add_column("Client Name")
        table.add_column("Montant Total (€)")
        table.add_column("Montant Payé (€)")
        table.add_column("Statut")
        table.add_column("Commercial")

        for contract in contracts:
            sales_contact_info = (
                f"{contract.sales_contact.id} ({contract.sales_contact.first_name} {contract.sales_contact.last_name})"
                if contract.sales_contact
                else "Non assigné"
            )

            table.add_row(
                str(contract.id),
                str(contract.client.id) if contract.client else "N/A",
                (
                    f"{contract.client.last_name} {contract.client.first_name}"
                    if contract.client
                    else "N/A"
                ),
                str(contract.total_amount),
                str(contract.payed_amount),
                ContractView.get_status_label(contract.contract_status_id),
                sales_contact_info,
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
        sales_contact_info = (
            f"{contract.sales_contact.first_name} {contract.sales_contact.last_name} ({contract.sales_contact.id})"
            if contract.sales_contact
            else "Non assigné"
        )

        contract_details = f"""
        [cyan bold]Fiche Contrat ID: {contract.id}[/cyan bold]

        ─────────────────

        [cyan bold]Client Name:[/cyan bold] {contract.client.first_name} {contract.client.last_name}, {contract.client.company.title}, id: {contract.clients_id}
        [cyan bold]Montant Total:[/cyan bold] {contract.total_amount}€
        [cyan bold]Montant Payé:[/cyan bold] {contract.payed_amount}€
        [cyan bold]Statut:[/cyan bold] {ContractView.get_status_label(contract.contract_status_id)}
        [cyan bold]Sales contact:[/cyan bold] {sales_contact_info}
        [cyan bold]Créé le:[/cyan bold] {contract.created_at}
        [cyan bold]Modifié le:[/cyan bold] {contract.updated_at}
        [cyan bold]Supprimé le:[/cyan bold] {contract.deleted_at}
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

        clients_id = int(
            Prompt.ask("\n[bold cyan]ID du Client[/bold cyan]", default="1")
        )
        total_amount = float(
            Prompt.ask("[bold cyan]Montant total (€)[/bold cyan]", default="0")
        )
        payed_amount = float(
            Prompt.ask("[bold cyan]Montant déjà payé (€)[/bold cyan]", default="0")
        )

        console.print("\n[bold cyan]Sélectionnez le statut du contrat :[/bold cyan]")
        console.print("[1] En attente de signature")
        console.print("[2] Signé")
        console.print("[3] Annulé")
        contract_status_id = int(
            Prompt.ask(
                "Choisissez un ID de statut", choices=["1", "2", "3"], default="1"
            )
        )
        sales_contact_id = int(
            Prompt.ask("\n[bold cyan]ID du Commercial[/bold cyan]", default="1")
        )

        return {
            "clients_id": clients_id,
            "total_amount": total_amount,
            "payed_amount": payed_amount,
            "contract_status_id": contract_status_id,
            "sales_contact_id": sales_contact_id,
        }

    @staticmethod
    def prompt_contract_update(contract):
        """Demande les nouvelles informations pour modifier un contrat."""
        console.print(
            f"\n[bold cyan]Modification du contrat ID {contract.id}[/bold cyan]"
        )

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

        sales_contact_id = Prompt.ask(
            f"ID du Commercial Actuel : [yellow]{contract.sales_contact.id if contract.sales_contact else 'Non assigné'}[/yellow] ➝ Nouvel ID du Commercial",
            default=str(contract.sales_contact.id if contract.sales_contact else ""),
        )

        sales_contact_id = (
            int(sales_contact_id) if sales_contact_id.isdigit() else None
        )

        return {
            "total_amount": total_amount,
            "payed_amount": payed_amount,
            "contract_status_id": contract_status_id,
            "sales_contact_id": sales_contact_id,
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

    @staticmethod
    def prompt_contract_filters():
        """
        Affiche un menu permettant de sélectionner plusieurs critères de filtrage des contrats.
        """
        filters = {}

        console.print(
            "\n[bold cyan]Sélection des filtres pour les contrats[/bold cyan]"
        )

        filter_options = {
            "1": "Statut du contrat",
            "2": "ID du Client",
            "3": "ID du Commercial",
            "4": "Montant total minimum",
            "5": "Montant total maximum",
            "6": "Montant payé minimum",
            "7": "Montant payé maximum",
        }

        # Affichage des options
        for key, option in filter_options.items():
            console.print(f"[{key}] {option}")

        selected_options = Prompt.ask(
            "Entrez les numéros des filtres à appliquer (séparés par une virgule)",
            default="",
        ).split(",")

        for option in selected_options:
            option = option.strip()
            if option in filter_options:
                if option == "1":
                    filters["contract_status_id"] = Prompt.ask(
                        "Entrez l'ID du statut du contrat"
                    )
                elif option == "2":
                    filters["clients_id"] = Prompt.ask("Entrez l'ID du client")
                elif option == "3":
                    filters["sales_contact_id"] = Prompt.ask(
                        "Entrez l'ID du commercial"
                    )
                elif option == "4":
                    filters["total_amount_min"] = Prompt.ask("Montant total minimum")
                elif option == "5":
                    filters["total_amount_max"] = Prompt.ask("Montant total maximum")
                elif option == "6":
                    filters["payed_amount_min"] = Prompt.ask("Montant payé minimum")
                elif option == "7":
                    filters["payed_amount_max"] = Prompt.ask("Montant payé maximum")

        return filters
