from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
import click

console = Console()


class InvoiceView:
    @staticmethod
    def show_menu():
        """Affiche le menu de gestion des factures."""
        console.print("\n[bold cyan]╭───────────────╮[/bold cyan]")
        console.print("[bold cyan]│ Menu Factures │[/bold cyan]")
        console.print("[bold cyan]╰───────────────╯[/bold cyan]")
        console.print("\n[1] Lister toutes les factures")
        console.print("[2] Voir une facture par ID")
        console.print("[3] Créer une facture")
        console.print("[4] Modifier une facture")
        console.print("[5] Supprimer une facture")
        console.print("[0] Retour au menu principal\n")

    @staticmethod
    def display_invoices(invoices):
        """Affiche toutes les factures sous forme de tableau."""
        table = Table(title="\n[bold cyan]Liste des Factures[/bold cyan]\n")

        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Contrat ID", justify="center", style="green")
        table.add_column("Montant Total (€)", justify="right", style="yellow")
        table.add_column("Montant Payé (€)", justify="right", style="white")
        table.add_column("Statut", justify="center", style="magenta")

        for invoice in invoices:
            table.add_row(
                str(invoice.id),
                str(invoice.contracts_id),
                f"{invoice.total_amount}€",
                f"{invoice.payed_amount}€",
                InvoiceView.get_status_label(invoice.status),
            )

        # Calcul de la largeur de la table
        table_width = console.measure(table).maximum

        # Affichage dynamique des séparateurs
        console.print("\n" + "═" * table_width, style="bold white")
        console.print(table)
        console.print("\n" + "═" * table_width, style="bold white")

    @staticmethod
    def display_invoice(invoice):
        """Affiche les détails d'une facture sous forme de fiche détaillée."""
        invoice_details = f"""
        [cyan bold]Fiche Facture[/cyan bold]

        ─────────────────

        [cyan bold]ID:[/cyan bold] {invoice.id}
        [green bold]Contrat ID:[/green bold] {invoice.contracts_id}
        [yellow bold]Montant Total:[/yellow bold] {invoice.total_amount}€
        [white bold]Montant Payé:[/white bold] {invoice.payed_amount}€
        [magenta bold]Statut:[/magenta bold] {InvoiceView.get_status_label(invoice.status)}
        """

        console.print(
            Panel.fit(
                invoice_details,
                title="\n[bold cyan]Détails Facture[/bold cyan]",
                style="white",
            )
        )

    @staticmethod
    def prompt_invoice_data():
        """Demande les informations pour créer une facture."""
        console.print("\n[bold cyan]Création d'une nouvelle facture[/bold cyan]")
        contracts_id = Prompt.ask("ID du Contrat")
        while not contracts_id.isdigit():
            contracts_id = Prompt.ask(
                "[red]L'ID du Contrat doit être un nombre valide.[/red]"
            )
        contracts_id = int(contracts_id)

        total_amount = Prompt.ask("Montant total (€)")
        while not total_amount.replace(".", "", 1).isdigit():
            total_amount = Prompt.ask("[red]Veuillez entrer un montant valide.[/red]")
        total_amount = float(total_amount)

        payed_amount = Prompt.ask("Montant payé (€)", default="0")
        while not payed_amount.replace(".", "", 1).isdigit():
            payed_amount = Prompt.ask("[red]Veuillez entrer un montant valide.[/red]")
        payed_amount = float(payed_amount)

        console.print("\n[bold cyan]Sélectionnez le statut de la facture :[/bold cyan]")
        console.print("[1] En attente de paiement")
        console.print("[2] Payée")
        console.print("[3] Annulée")
        status = Prompt.ask(
            "Choisissez un ID de statut", choices=["1", "2", "3"], default="1"
        )
        status = int(status)

        return {
            "contracts_id": contracts_id,
            "total_amount": total_amount,
            "payed_amount": payed_amount,
            "status": status,
        }

    @staticmethod
    def prompt_invoice_update(invoice):
        """Permet de modifier une facture existante."""
        console.print("\n[bold cyan]Mise à jour d'une facture[/bold cyan]")
        update_data = {}

        while True:
            console.print("[1] Modifier le montant total (€)")
            console.print("[2] Modifier le montant payé (€)")
            console.print("[3] Modifier le statut")
            console.print("[0] Terminer la modification")

            choice = click.prompt("Entrez le numéro du champ à modifier", type=int)

            if choice == 1:
                new_value = Prompt.ask(
                    f"Montant total actuel : [yellow]{invoice.total_amount}€[/yellow] ➝ Nouveau montant (€)"
                )
                update_data["total_amount"] = (
                    float(new_value)
                    if new_value.replace(".", "", 1).isdigit()
                    else invoice.total_amount
                )

            elif choice == 2:
                new_value = Prompt.ask(
                    f"Montant payé actuel : [white]{invoice.payed_amount}€[/white] ➝ Nouveau montant (€)"
                )
                update_data["payed_amount"] = (
                    float(new_value)
                    if new_value.replace(".", "", 1).isdigit()
                    else invoice.payed_amount
                )

            elif choice == 3:
                console.print(
                    "\n[bold cyan]Sélectionnez le nouveau statut :[/bold cyan]"
                )
                console.print("[1] En attente de paiement")
                console.print("[2] Payée")
