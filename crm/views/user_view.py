from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
import click

console = Console()


class UserView:

    @staticmethod
    def show_menu():
        """Affiche le menu de gestion des utilisateurs."""
        console.print("\n[bold cyan]╭────────────────────╮[/bold cyan]")
        console.print("[bold cyan]│  Menu Utilisateurs │[/bold cyan]")
        console.print("[bold cyan]╰────────────────────╯[/bold cyan]")
        console.print("\n[1] Lister tous les utilisateurs")
        console.print("[2] Voir un utilisateur par ID")
        console.print("[3] Créer un utilisateur")
        console.print("[4] Modifier un utilisateur")
        console.print("[5] Supprimer un utilisateur")
        console.print("[6] Filter les utilisateurs")
        console.print("[0] Retour au menu principal\n")

    @staticmethod
    def display_users(users):
        """
        Affiche tous les utilisateurs sous forme de tableau.
        """
        table = Table(title="\n[bold cyan]Liste des utilisateurs[/bold cyan]\n")

        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Nom")
        table.add_column("Prénom")
        table.add_column("Nom d'utilisateur")
        table.add_column("Email")
        table.add_column("Département")

        for user in users:
            departement_infos = (
                f"{user.department.title} - (id:{user.departments_id})"
                if user.department
                else "Non assigné"
            )
            table.add_row(
                str(user.id),
                user.last_name,
                user.first_name,
                user.username,
                user.email,
                departement_infos,
            )

        # Calcul de la largeur de la table
        table_width = console.measure(table).maximum

        # Affichage dynamique des séparateurs
        console.print("\n" + "═" * table_width, style="bold white")
        console.print(table)
        console.print("\n" + "═" * table_width, style="bold white")

    @staticmethod
    def display_user(user):
        """
        Affiche un utilisateur sous forme de fiche détaillée.
        """

        user_details = f"""
        [cyan bold]Fiche Utilisateur[/cyan bold]

        ─────────────────

        [cyan bold]ID:[/cyan bold] {user.id}
        [cyan bold]Nom:[/cyan bold] {user.last_name} {user.first_name}
        [cyan bold]Email:[/cyan bold] {user.email}
        [cyan bold]Nom d'utilisateur:[/cyan bold] {user.username}
        [cyan bold]Département:[/cyan bold] {user.department_id}


        """

        console.print(
            Panel.fit(
                user_details,
                title="\n[bold cyan]Détails Utilisateur[/bold cyan]",
                style="white",
            )
        )

    @staticmethod
    def prompt_user_data():
        """
        Demande les informations pour créer un utilisateur.
        """
        console.print("\n[bold cyan]Création d'un nouvel utilisateur[/bold cyan]")
        last_name = Prompt.ask("\n[bold cyan]Nom de famille[/bold cyan]").strip()
        first_name = Prompt.ask("[bold cyan]Prénom[/bold cyan]").strip()
        email = Prompt.ask("[bold cyan]Email[/bold cyan]").strip()
        username = Prompt.ask("[bold cyan]Nom d'utilisateur[/bold cyan]").strip()
        password = Prompt.ask(
            "[bold cyan]Mot de passe[/bold cyan]", password=True
        ).strip()
        departments_id = Prompt.ask(
            "[bold cyan]ID du département[/bold cyan]", default="1"
        ).strip()

        return {
            "last_name": last_name,
            "first_name": first_name,
            "email": email,
            "username": username,
            "password": password,
            "departments_id": int(departments_id),
        }

    @staticmethod
    def prompt_user_update(user):
        """
        Demande les informations à modifier pour un utilisateur.
        """
        console.print("\n[bold cyan]Mise à jour d'un utilisateur[/bold cyan]")
        update_data = {}

        while True:
            console.print("[1] Modifier Nom")
            console.print("[2] Modifier Prénom")
            console.print("[3] Modifier Email")
            console.print("[4] Modifier Nom d'utilisateur")
            console.print("[5] Modifier Département")
            console.print("[0] Terminer la modification")

            choice = click.prompt("Choisissez une option", type=int)

            if choice == 1:
                update_data["last_name"] = Prompt.ask(
                    "Nouveau Nom", default=user.last_name
                )
            elif choice == 2:
                update_data["first_name"] = Prompt.ask(
                    "Nouveau Prénom", default=user.first_name
                )
            elif choice == 3:
                update_data["email"] = Prompt.ask("Nouvel Email", default=user.email)
            elif choice == 4:
                update_data["username"] = Prompt.ask(
                    "Nouveau Nom d'utilisateur", default=user.username
                )
            elif choice == 5:
                update_data["departments_id"] = Prompt.ask(
                    "Nouveau ID Département", default=str(user.departments_id)
                )
            elif choice == 0:
                break
            else:
                console.print(
                    "[bold red]Option invalide, veuillez réessayer[bold red]."
                )

        return update_data

    @staticmethod
    def prompt_user_filters():
        """
        Affiche un menu permettant de sélectionner plusieurs critères de filtrage des utilisateurs.
        """
        filters = {}

        console.print(
            "\n[bold cyan]Sélection des filtres pour les utilisateurs[/bold cyan]"
        )

        filter_options = {
            "1": "Nom",
            "2": "Prénom",
            "3": "Email",
            "4": "Nom d'utilisateur",
            "5": "ID du Département",
        }

        for key, option in filter_options.items():
            console.print(f"[{key}] {option}")

        selected_options = Prompt.ask(
            "Entrez les numéros des filtres à appliquer (séparés par une virgule)",
            default="",
        ).split(",")

        for option in selected_options:
            option = option.strip()
            if option == "1":
                filters["last_name"] = Prompt.ask("Entrez un nom")
            elif option == "2":
                filters["first_name"] = Prompt.ask("Entrez un prénom")
            elif option == "3":
                filters["email"] = Prompt.ask("Entrez un email")
            elif option == "4":
                filters["username"] = Prompt.ask("Entrez un nom d'utilisateur")
            elif option == "5":
                filters["departments_id"] = Prompt.ask("Entrez l'ID du département")

        return filters
