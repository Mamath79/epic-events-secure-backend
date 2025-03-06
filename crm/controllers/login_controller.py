import click
from sentry_sdk import capture_exception
from crm.database.base import SessionLocal
from crm.views.login_view import LoginView
from crm.services.user_service import UserService
from crm.controllers.home_controller import HomeController
from crm.utils.logger import log_info, log_error

@click.command()
def EnterCrm():
    """
    Commande CLI pour gérer l'authentification.
    """
    while True:
        try:
            choice = LoginView.login_menu()

            if choice == "1":
                email, password = LoginView.prompt_login()

                with SessionLocal() as session:
                    user_service = UserService(session)
                    token = user_service.authenticate(email, password)

                if token:
                    log_info(f"Utilisateur {email} authentifié avec succès.")
                    LoginView.show_success_login()
                    HomeController.handle_choice()
                else:
                    log_error(f"Échec d'authentification pour l'utilisateur {email}.")
                    LoginView.show_error_login()

            elif choice == "0":
                click.echo("Au revoir !")
                exit()

            else:
                click.echo("Option invalide, veuillez réessayer.")
        
        except Exception as e:
            log_error(f"Erreur lors de l'authentification : {str(e)}")
            capture_exception(e)
            click.echo("⚠️ Une erreur est survenue. Veuillez réessayer.")
