import click
from crm.database.base import SessionLocal
from crm.views.login_view import LoginView
from crm.services.user_service import UserService
from crm.controllers.home_controller import HomeController

@click.command()
def EnterCrm():
     """
    Commande CLI pour gérer l'authentification
    """
     while True:
            choice = LoginView.login_menu()

            if choice == "1":
                email, password = LoginView.prompt_login()

                db_session = SessionLocal()
                user_service = UserService(db_session)
                
                token = user_service.authenticate(email, password)
                db_session.close()

                if token:
                    LoginView.show_success_login()
                    HomeController.handle_choice()
                else:
                    LoginView.show_error_login()
            elif choice == "0":
                click.echo('Au revoir !')
                exit()
            else:
                LoginView.show_error_login()

    

    