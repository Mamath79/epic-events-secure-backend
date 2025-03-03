from crm.views.home_view import HomeView
from crm.controllers.client_controller import client_menu
from crm.controllers.contract_controller import contract_menu
from crm.controllers.event_controller import event_menu
from crm.controllers.user_controller import user_menu

class HomeController:
    @staticmethod
    def handle_choice():
        """
        Boucle principale du menu d'accueil après authentification
        """
        while True:
            choice = HomeView.show_menu()

            if choice == "1":
                client_menu()  # Menu Clients
            elif choice == "2":
                contract_menu()  # Menu Contrats
            elif choice == "3":
                event_menu()  # Menu Événements
            elif choice == "4":
                user_menu()  # Menu Utilisateurs
            elif choice == "0":
                HomeView.show_logout()
                break  # Retour au login
            else:
                HomeView.show_invalid_option()
                return
