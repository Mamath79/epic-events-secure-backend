import click
from sentry_sdk import capture_exception
from crm.views.home_view import HomeView
from crm.controllers.client_controller import client_menu
from crm.controllers.contract_controller import contract_menu
from crm.controllers.event_controller import event_menu
from crm.controllers.user_controller import user_menu
from crm.utils.logger import log_error, log_info


class HomeController:
    @staticmethod
    def handle_choice():
        """
        Boucle principale du menu d'accueil après authentification.
        Gère la navigation et capture les erreurs éventuelles.
        """
        while True:
            try:
                choice = HomeView.show_menu()

                # Vérification de l'entrée utilisateur
                if not choice.isdigit():
                    log_error("Entrée invalide : un nombre était attendu.")
                    click.echo("\nVeuillez entrer un numéro valide.\n")
                    continue  # Redemande l'entrée

                choice = int(choice)

                if choice == 1:
                    log_info("Accès au menu Clients")
                    client_menu()
                elif choice == 2:
                    log_info("Accès au menu Contrats")
                    contract_menu()
                elif choice == 3:
                    log_info("Accès au menu Événements")
                    event_menu()
                elif choice == 4:
                    log_info("Accès au menu Utilisateurs")
                    user_menu()
                elif choice == 0:
                    HomeView.show_logout()
                    log_info("Déconnexion réussie")
                    break  # Retour au login
                else:
                    log_error(f"Option invalide sélectionnée : {choice}")
                    click.echo("\nOption invalide, veuillez réessayer.\n")

            except Exception as e:
                log_error(f"Erreur dans le menu principal : {str(e)}")
                capture_exception(e)
                click.echo("\nUne erreur s'est produite. Veuillez réessayer.\n")
