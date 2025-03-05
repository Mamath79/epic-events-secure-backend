from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

class CompanyView:

    @staticmethod
    def show_menu():
        """Affiche le menu de gestion des entreprises."""
        console.print("\n[bold cyan]╭───────────────────╮[/bold cyan]")
        console.print("[bold cyan]│ Menu Entreprises │[/bold cyan]")
        console.print("[bold cyan]╰───────────────────╯[/bold cyan]")
        console.print("[1] Lister toutes les Entreprises")
        console.print("[2] Voir une Entreprise par ID")
        console.print("[3] Créer une Entreprise")
        console.print("[4] Modifier une Entreprise")
        console.print("[5] Supprimer une Entreprise")
        console.print("[0] Retour au menu Client")
    
    @staticmethod
    def display_companies(companies):
        """Affiche la liste des entreprises sous forme de tableau."""
        table = Table(title="📌 Liste des Entreprises")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Nom", style="green")
        table.add_column("SIRET", style="yellow")

        for company in companies:
            table.add_row(str(company.id), company.title, company.siret or "N/A")

        console.print(table)

    @staticmethod
    def display_company(company):
        """Affiche les détails d'une entreprise spécifique."""
        console.print("\n📌 [bold cyan]Détails de l'Entreprise[/bold cyan]")
        console.print(f"[cyan]ID :[/cyan] {company.id}")
        console.print(f"[green]Nom :[/green] {company.title}")
        console.print(f"[yellow]SIRET :[/yellow] {company.siret or 'N/A'}")

    @staticmethod
    def prompt_company_data():
        """Demande les informations pour créer une entreprise."""
        title = Prompt.ask("[bold cyan]Nom de l'entreprise[/bold cyan]").strip()
        siret = Prompt.ask("[bold cyan]SIRET de l'entreprise (laisser vide si inconnu)[/bold cyan]", default="").strip()

        if not title:
            console.print("[red]❌ Le nom de l'entreprise est requis.[/red]")
            return None

        return {
            "title": title,
            "siret": siret  # ✅ Pas de transformation ici, on passe la donnée brute
        }

    @staticmethod
    def prompt_company_update(company):
        """Permet de modifier une entreprise existante."""
        console.print(f"\n📌 Modification de l'entreprise [cyan]{company.title}[/cyan]")

        update_data = {}

        new_title = Prompt.ask(f"Nom actuel : [green]{company.title}[/green] ➝ Nouveau nom", default=company.title).strip()
        if new_title != company.title:
            update_data["title"] = new_title

        new_siret = Prompt.ask(f"SIRET actuel : [yellow]{company.siret or 'N/A'}[/yellow] ➝ Nouveau SIRET (laisser vide si inchangé)", default=company.siret or "").strip()
        if new_siret != company.siret:
            update_data["siret"] = new_siret or None

        if not update_data:
            console.print("[yellow]⚠️ Aucune modification effectuée.[/yellow]")
            return None
        
        return update_data

    @staticmethod
    def display_message(message, msg_type="info"):
        """Affiche un message en fonction du type (success, error, info)."""
        colors = {
            "success": "green",
            "error": "red",
            "info": "cyan"
        }
        console.print(f"[{colors.get(msg_type, 'white')}] {message} [/{colors.get(msg_type, 'white')}]")
