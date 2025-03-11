from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel

console = Console()


class CompanyView:

    @staticmethod
    def show_menu():
        """Affiche le menu de gestion des entreprises."""
        console.print("\n[bold cyan]╭───────────────────╮[/bold cyan]")
        console.print("[bold cyan]│  Menu Entreprises │[/bold cyan]")
        console.print("[bold cyan]╰───────────────────╯[/bold cyan]")
        console.print("\n[1] Lister toutes les entreprises")
        console.print("[2] Voir une entreprise par ID")
        console.print("[3] Créer une entreprise")
        console.print("[4] Modifier une entreprise")
        console.print("[5] Supprimer une entreprise")
        console.print("[0] Retour au menu principal\n")

    @staticmethod
    def display_companies(companies):
        """Affiche la liste des entreprises sous forme de tableau."""
        table = Table(title="\n[bold cyan]Liste des entreprises[/bold cyan]\n")

        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Nom", style="green", no_wrap=True)
        table.add_column("SIRET", style="yellow", no_wrap=True)

        for company in companies:
            table.add_row(str(company.id), company.title, company.siret or "N/A")

        # Calcul de la largeur de la table
        table_width = console.measure(table).maximum

        # Affichage dynamique des séparateurs
        console.print("\n" + "═" * table_width, style="bold white")
        console.print(table)
        console.print("\n" + "═" * table_width, style="bold white")

    @staticmethod
    def display_company(company):
        """Affiche les détails d'une entreprise spécifique."""
        company_details = f"""
        [cyan bold]Fiche Entreprise[/cyan bold]

        ─────────────────

        [cyan bold]ID:[/cyan bold] {company.id}
        [green bold]Nom:[/green bold] {company.title}
        [yellow bold]SIRET:[/yellow bold] {company.siret or "N/A"}
        """

        console.print(
            Panel.fit(
                company_details,
                title="\n[bold cyan]Détails Entreprise[/bold cyan]",
                style="white",
            )
        )

    @staticmethod
    def prompt_company_data():
        """Demande les informations pour créer une entreprise."""
        console.print("\n[bold cyan]Création d'une nouvelle entreprise[/bold cyan]")
        title = Prompt.ask("\n[bold cyan]Nom de l'entreprise[/bold cyan]").strip()
        siret = Prompt.ask(
            "[bold cyan]SIRET de l'entreprise (laisser vide si inconnu)[/bold cyan]",
            default="",
        ).strip()

        if not title:
            console.print("[bold red]Le nom de l'entreprise est requis.[/bold red]")
            return None

        return {
            "title": title,
            "siret": siret or None,
        }

    @staticmethod
    def prompt_company_update(company):
        """Permet de modifier une entreprise existante."""
        console.print(
            f"\n[bold cyan]Modification de l'entreprise {company.title}[/bold cyan]"
        )

        update_data = {}

        new_title = Prompt.ask(
            f"Nom actuel : [green]{company.title}[/green] ➝ Nouveau nom",
            default=company.title,
        ).strip()
        if new_title and new_title != company.title:
            update_data["title"] = new_title

        new_siret = Prompt.ask(
            f"SIRET actuel : [yellow]{company.siret or 'N/A'}[/yellow] ➝ Nouveau SIRET (laisser vide si inchangé)",
            default=company.siret or "",
        ).strip()
        if new_siret != company.siret:
            update_data["siret"] = new_siret or None

        if not update_data:
            console.print("[bold yellow]Aucune modification effectuée.[/bold yellow]")
            return None

        return update_data

    @staticmethod
    def display_message(message, msg_type="info"):
        """Affiche un message en fonction du type (success, error, info)."""
        colors = {"success": "green", "error": "red", "info": "cyan"}
        console.print(
            f"[{colors.get(msg_type, 'white')}] {message} [/{colors.get(msg_type, 'white')}]"
        )
