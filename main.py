from abc import ABC, abstractmethod
import time
from turtle import color
import bcrypt
import pwinput
from termcolor import colored
from patterns.facade import SystemFacade
from utils import clear_screen
from _class.person import Admin
import threading
from datetime import datetime
from _class.tracker import Tracker

def initialize_animal_trackers():
    """
    Initializes animal trackers by retrieving all animals from the database,
    recreating their trackers, and starting the location generation and saving threads.
    """

    # Obtain the singleton instance of the SystemFacade
    facade = SystemFacade()

    # Retrieve all animals from the database
    # Returns a list of tuples: (id, name, specie, age, description, territory_id, tracker_id)
    all_animals = facade.list_animais()

    # For each animal, recreate its tracker and start the threads
    for row in all_animals:
        animal_id = row[0]
        animal_name = row[1]
        territory_id = row[5]
        tracker_id = row[6]

        # If the animal has a valid tracker_id, attempt to reactivate it
        if tracker_id is not None:
            # Retrieve the territory to use its x and y limits
            territory_obj = facade.get_territory_by_id(territory_id)
            x_limit = territory_obj.x
            y_limit = territory_obj.y

            # Create an instance of the tracker
            tracker = Tracker(
                state=True, 
                x_limit=x_limit, 
                y_limit=y_limit, 
                id=tracker_id
            )
            tracker.animal_id = animal_id

            # Start location generation
            tracker.start_location_generation()

            # Start periodic location saving
            conn = facade.db.get_connection()
            tracker.start_location_saving(conn, animal_name)


class UserRole(ABC):
    """
    An abstract base class representing the role of a user.
    Subclasses should implement the show_menu method to define
    the specific behavior for displaying the menu for each role.
    """
    @abstractmethod
    def show_menu(self, facade):
        """
        Abstract method to display the menu for the user role.
        This method must be implemented by subclasses.

        :param facade: An instance of the SystemFacade to interact with the system.
        """
        pass

# Classe para usuários comuns (apenas visualizar territórios)
class RegularUser(UserRole):
    """
    A class representing a regular user role.
    Inherits from UserRole and implements the show_menu method.
    """
    def __init__(self, user_id: int) -> None:
        """
        Initializes a RegularUser instance.

        :param user_id: The unique identifier of the user.
        """
        super().__init__()
        self.user_id = user_id
    def show_menu(self, facade):
        """
        Displays the menu for the regular user and handles user input.

        :param facade: An instance of the SystemFacade to interact with the system.
        """
        while True:
            clear_screen()
            print(colored(f"------------------------------ {colored("Menu do Usuário", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
            print("1 - Visualizar Território")
            print("2 - Deslogar")
            print("3 - Encerrar Programa")

            try:
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue

            if user_input == 1:
                clear_screen()
                print(colored(f"------------------------------ {colored("Opções de Vizualização", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
                print("1 - Vizualização em Tempo Real")
                print("2 - Vizualizar Histórico")
                user_input = input("Escolha sua opção: ")
                if user_input == "":
                    return
                user_input = int(user_input)
                if user_input == 1:
                    # Create an event to signal the thread to stop
                    stop_event = threading.Event()
                    # Start a new thread to show the territory in real-time
                    sim_thread = threading.Thread(target=lambda: facade.show_territory_user(self.user_id, stop_event))
                    sim_thread.start()
                    print("\nA simulação do território foi iniciada em uma nova janela.")
                    print("Para voltar ao menu, volte ao terminal do menu e pressione Enter.")
                    input() # Wait for the user to press Enter in the main terminal
                    # Signal the simulation to stop and wait for the thread to finish
                    stop_event.set()
                    sim_thread.join()
                if user_input == 2:
                    clear_screen()
                    print(colored(f"------------------------------ {colored("Histórico Territórios", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
                    # List animals in the user's territory
                    animals = facade.list_animals_in_territory_user(self.user_id)
                    print("Animais cadastrados:")
                    if animals:
                        existing_ids = []
                        for animal in animals:
                            existing_ids.append(animal.id)
                            print(f"ID: {animal.id}, Nome: {animal.name}")
                        try:
                            animal_id = input("Digite o ID do animal que você deseja vizualizar o histórico: ")
                            if animal_id == "":
                                return
                            animal_id = int(animal_id)
                            if animal_id not in existing_ids:
                                print(colored("Erro: Terrotório Inexistente!", "red"))
                                time.sleep(1.5)
                                return
                            # Show location history for the selected animal
                            locations = facade.show_location_history(animal_id)
                            for location in locations:
                                print(f"Nome: {location[1]}, x: {location[2]}, y: {location[3]}, horario: {datetime.fromtimestamp(location[4]).strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]}")
                            input("\nPressione Enter para continuar...")
                        except ValueError:
                            print("ID inválido! Digite um número.")  
                    else:
                        print(colored("Nenhum animal cadastrado no território!", "red"))
                        time.sleep(1.5)
            elif user_input == 2:
                # Log out and return to the login screen
                login_screen(facade)
            elif user_input == 3:
                # Close the program
                print("Encerrando o programa...")
                facade.close_connection()
                exit()


class AdminUser(UserRole):
    def show_menu(self, facade):
        """
        Displays the administrator menu and processes user input for various options.
        
        :param facade: An instance of the SystemFacade for system interactions.
        """
        while True:
            clear_screen() # Clear the screen before displaying menu options

            # Print the header for the administrator menu using colored output
            print(colored(f"------------------------------ {colored("Menu do Administrador", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))

            # Display the menu options for admin users
            print("1 - Opções de Territórios") # Territory options
            print("2 - Opções de Usuários") # User options
            print("3 - Opções de Animais") # Animal options
            print("4 - Voltar ao Menu Principal") # Return to the main menu
            print("5 - Deslogar") # Log out
            print("6 - Encerrar Programa") # Exit the program

            try:
                # Attempt to read the user's menu selection and convert it to an integer
                admin_input = int(input("Escolha sua opção: "))
            except ValueError:
                # If conversion fails, notify the user and continue the loop
                print("Opção inválida! Digite um número.")
                continue

            # Process the user's input by calling corresponding methods
            if admin_input == 1:
                self.territory_options(facade) # Handle territory options
            elif admin_input == 2:
                self.user_options(facade)   # Handle user options
            elif admin_input == 3:
                self.animal_options(facade)     # Handle animal options
            elif admin_input == 4:
                return  # Return to the main menu
            elif admin_input == 5:
                login_screen(facade) # Log out: return to the login screen
            elif admin_input == 6:
                # Inform the user that the program is exiting, close the connection, then exit
                print("Encerrando o programa...")
                facade.close_connection()
                exit()

    def territory_options(self, facade):
        """
        Displays the territory management menu and handles administrator input to view,
        create, or delete territories.
        
        :param facade: An instance of SystemFacade for database interactions.
        """
        while True:
            clear_screen() # Clear the terminal screen

            # Display the header for territory management using colored output
            print(colored(f"------------------------------ {colored("Gerenciar Territórios", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
            print("1 - Vizualizar Territórios") # Option to view territories
            print("2 - Criar Território")  # Option to create a new territory
            print("3 - Deletar Território") # Option to delete a territory
            print("4 - Voltar ao Menu Admin") # Option to return to the admin menu

            try:
                # Read and convert the user's menu selection to an integer
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                # Inform the user of an invalid option if conversion fails
                print("Opção inválida! Digite um número.")
                continue

            if user_input == 1:
                clear_screen() # Clear screen to display territory details
                # Print header for viewing territories
                print(colored(f"------------------------------ {colored("Territórios", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
                territories = facade.list_territories()
                print("Territórios cadastrados: ")
                existing_ids = [] # List to store IDs of existing territories
                # Iterate over each territory to display details and record its ID
                for territory in territories:
                    existing_ids.append(territory.id)
                    print(f"ID: {territory.id}, Nome: {territory.name}, X: {territory.x}, Y: {territory.y}")

                 # Prompt the user to enter the territory ID for viewing
                territory_id = input("Digite o ID do território que deseja visualizar: ")
                if territory_id == "": # Check for cancellation (empty input)
                    return
                territory_id = int(territory_id)
                if territory_id not in existing_ids:
                    # If the territory ID does not exist, notify the user and pause briefly
                    print(colored("Error: Território inexistente", "red"))
                    time.sleep(1.5)
                    return
                
                clear_screen() # Clear screen to display visualization options
                # Print header for visualization options
                print(colored(f"------------------------------ {colored("Opções de Vizualização", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
                print("1 - Vizualização em Tempo Real") # Option for real-time visualization
                print("2 - Vizualizar Histórico") # Option to view history
                print("3 - Deletar Histórico") # Option to delete history
                user_input = input("Escolha sua opção: ")
                if user_input == "":
                    return
                user_input = int(user_input)

                if user_input == 1:
                    # Start real-time simulation in a separate thread
                    stop_event = threading.Event() # Create an event to signal thread stopping
                    sim_thread = threading.Thread(target=lambda: facade.show_territory_admin(territory_id, stop_event))
                    sim_thread.start()
                    print("\nA simulação do território foi iniciada em uma nova janela.")
                    print("Para voltar ao menu, volte ao terminal do menu e pressione Enter.")
                    input()  # Wait for user to press Enter
                    # Signal the simulation to stop and wait for the thread to finish
                    stop_event.set()
                    sim_thread.join()
                elif user_input == 2:
                    clear_screen()  # Clear screen to show history
                    # Print header for territory history
                    print(colored(f"------------------------------ {colored("Histórico Territórios", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
                    animals = facade.list_animals_in_territory(territory_id)
                    print("Animais cadastrados:")
                    if animals:
                        existing_ids = []  # List to store animal IDs
                        for animal in animals:
                            existing_ids.append(animal.id)
                            print(f"ID: {animal.id}, Nome: {animal.name}")
                        try:
                            # Prompt the user to select an animal to view its history
                            animal_id = input("Digite o ID do animal que você deseja vizualizar o histórico: ")
                            if animal_id == "":
                                return
                            animal_id = int(animal_id)
                            if animal_id not in existing_ids:
                                # If the entered animal ID is not valid, inform the user
                                print(colored("Error: Animal Inexistente", "red"))
                                time.sleep(1.5)
                                return
                            # Retrieve and display location history for the chosen animal
                            locations = facade.show_location_history(animal_id)
                            for location in locations:
                                print(f"Nome: {location[1]}, x: {location[2]}, y: {location[3]}, horario: {datetime.fromtimestamp(location[4]).strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]}")
                            input("\nPressione Enter para continuar...")
                        except ValueError:
                            # Notify the user if an invalid animal ID was entered
                            print("ID inválido! Digite um número.")  
                    else:
                        # Notify if there are no animals registered in the territory
                        print(colored("Nenhum animal cadastrado no território!", "red"))
                        time.sleep(1.5)
                elif user_input == 3:
                    # Delete location history from the facade
                    facade.delete_location_history()
                    print(colored("Histórico deletado com sucesso!", "green"))
                    time.sleep(1.5)        
            elif user_input == 2:
                clear_screen() # Clear screen to initiate territory creation
                # Display header for creating a new territory
                print(colored(f"------------------------------ {colored("Novo Território", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
                print(f"Pressione Enter para cancelar...")
                
                # Prompt for territory details
                name = input("Nome do território: ")
                if name.strip() == "":
                    print(colored("Criação de território cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                lat1 = input("Primeira Latitude: ")
                if lat1.strip() == "":
                    print(colored("Criação de território cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                lat1_float = float(lat1)
                
                long1 = input("Primeira Longitude: ")
                if long1.strip() == "":
                    print(colored("Criação de território cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                long1_float = float(long1)
            
                lat2 = input("Segunda Latitude: ")
                if lat2.strip() == "":
                    print(colored("Criação de território cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                lat2_float = float(lat2)
                
                long2 = input("Segunda Longitude: ")
                if long2.strip() == "":
                    print(colored("Criação de território cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                long2_float = float(long2)
                
                # Create the new territory via the facade interface
                facade.create_territory(name, lat1_float, long1_float, lat2_float, long2_float)
                print(colored("Território criado com sucesso!", "green"))
                time.sleep(1.5)

            elif user_input == 3:
                clear_screen()  # Clear screen for territory deletion
                # Display header for territory deletion
                print(colored(f"------------------------------ {colored("Excluir Território", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
                territories = facade.list_territories() # Retrieve territories from the facade
                print("Territórios cadastrados: ")
                for territory in territories:
                    print(f"ID: {territory.id}, Nome: {territory.name}, X: {territory.x}, Y: {territory.y}")
                print("Pressione Enter para cancelar...")
                
                id_delete = input("\nID do território para deletar: ")
                # Delete the specified territory via the facade
                if id_delete.strip() == "":
                    print(colored("Exclusão de território cancelada...", "yellow"))
                    time.sleep(1.5)
                    return
                
                id_delete_int = int(id_delete) 
                facade.delete_territory(id_delete_int)
                print(colored("Território excluído com sucesso!", "green"))
                time.sleep(1.5)

            elif user_input == 4:
                return  # Return to the admin menu

    def user_options(self, facade):
        """
        Displays the user management menu and processes administrator actions
        related to listing, creating, and deleting users.
        
        :param facade: An instance of SystemFacade for interacting with the system.
        """
        while True:
            clear_screen()  # Clear the screen before displaying menu options
            print(colored(f"------------------------------ {colored("Gerenciar Usuários", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
            print("1 - Listar Usuários")      # Option to list all users
            print("2 - Criar Usuário")        # Option to create a new user
            print("3 - Excluir Usuário")      # Option to delete a user
            print("4 - Voltar ao Menu Admin") # Option to return to the admin menu

            try:
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                # Notify the user of an invalid selection
                print("Opção inválida! Digite um número.")
                continue

            if user_input == 1:
                # Retrieve and display all users
                users = facade.list_users()
                print("\nUsuários cadastrados:")
                for user in users:
                    print(f"ID: {user.id}, Nome: {user.name}, E-mail: {user.email}, Celular: {user.celphone}")
                input("\nPressione Enter para continuar...")

            elif user_input == 2:
                clear_screen() # Clear the screen for new user creation
                territories = facade.show_territory_null() # Get territories without an assigned owner
                
                if territories:
                    print(colored(f"------------------------------ {colored("Novo Usuário", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
                    print("Pressione Enter para cancelar...")
                    
                    # Prompt for user details
                    name = input("Nome: ")
                    if name.strip() == "":
                        print(colored("Criação de usuário cancelada...", "yellow"))
                        time.sleep(1.5)
                        return 
                    
                    password = pwinput.pwinput(prompt="Senha: ", mask="*")
                    if password.strip() == "":
                        print(colored("Criação de usuário cancelada...", "yellow"))
                        time.sleep(1.5)
                        return 
                    
                    email = input("E-mail: ")
                    if email.strip() == "":
                        print(colored("Criação de usuário cancelada...", "yellow"))
                        time.sleep(1.5)
                        return 
                    
                    phone = input("Celular: ")
                    if phone.strip() == "":
                        print(colored("Criação de usuário cancelada...", "yellow"))
                        time.sleep(1.5)
                        return
                    # Display available territories without an owner
                    territories = facade.show_territory_null()
                    existing_ids = []
                    for territorie in territories:
                        existing_ids.append(territorie.id)
                        print(f"ID: {territorie.id}, Nome: {territorie.name}, X: {territorie.x}, Y: {territorie.y}")
                    territory_id = input("ID do território: ")
                    if int(territory_id) not in existing_ids:
                        print(colored("Erro: Território Inexistente!", "red"))
                        time.sleep(1.5)
                        return
                    if territory_id.strip() == "":
                        print(colored("Criação de usuário cancelada...", "yellow"))
                        time.sleep(1.5)
                        return 
                    
                    # Create the new user via the facade
                    territory_id_int = int(territory_id)
                    facade.create_user(name, password, email, phone, territory_id_int)
                    print(colored("Usuário criado com sucesso!", "green"))
                    time.sleep(1.5)
                else:
                    # Clear screen and notify if no available territory exists
                    clear_screen()                   
                    
                    territories = facade.show_territory_null()                    
                    
                    if not territories:
                        print(colored("Não foi possível criar o usuário! Não existe nenhum território disponível.", "red"))
                    else:
                        print(colored("Não foi possível criar o usuário! Todos os territórios disponíveis já possuem dono.", "red"))
                    
                    input("\nPressione Enter para continuar...")

            elif user_input == 3:
                clear_screen()  # Clear screen for user deletion
                print(colored(f"------------------------------ {colored("Excluir Usuário", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
                users = facade.list_users() # Retrieve all users
                print("Usuários cadastrados: ")
                for user in users:
                    print(f"ID: {user.id}, Nome: {user.name}, E-mail: {user.email}, Celular: {user.celphone}")
                print("Pressione Enter para cancelar...")
                
                id_delete = input("\nID do usuário para excluir: ")
                if id_delete.strip() == "":
                    print(colored("Exclusão de usuário cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                
                id_delete_int = int(id_delete)
                # Delete the user via the facade
                facade.delete_user(id_delete_int)
                print(colored("Usuário excluído com sucesso!", "green"))
                time.sleep(1.5)

            elif user_input == 4:
                return # Return to the admin menu

    def animal_options(self, facade):
        """
        Displays the animal management menu and processes administrator actions
        for listing, adding, or deleting animals.
        
        :param facade: An instance of SystemFacade for system interactions.
        """
        while True:
            clear_screen()  # Clear screen before displaying animal options
            print(colored(f"------------------------------ {colored("Gerenciar Animais", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
            print("1 - Listar Animais")         # Option to list all animals
            print("2 - Adicionar Animal")       # Option to add a new animal
            print("3 - Excluir Animal")         # Option to delete an animal
            print("4 - Voltar ao Menu Admin")   # Option to return to the admin menu
            
            try:
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                # Notify user if input is not a valid number
                print("Opção inválida! Digite um número.")
                continue

            if user_input == 1:
                # List all animals
                animals = facade.list_animais()
                print("\nAnimais cadastrados:")
                if animals:
                    for animal in animals:
                        print(f"ID: {animal[0]}, Nome: {animal[1]}, Espécie: {animal[2]}, Idade: {animal[3]}")
                    input("\nPressione Enter para continuar...")
                else:
                    print(colored("Nenhum animal castrado no território!", "red"))
                    time.sleep(1.5)
                    
            elif user_input == 2:
                clear_screen() # Clear screen to add a new animal
                print(colored(f"------------------------------ {colored("Novo Animal", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
                print("Pressione Enter para cancelar...")
                
                # Prompt for new animal details
                name = input("Nome: ")
                if name.strip() == "":
                    print(colored("Criação do animal cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                
                specie = input("Espécie: ")
                if specie.strip() == "":
                    print(colored("Criação do animal cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                
                age = int(input("Idade: "))
                if str(age).strip() == "":
                    print(colored("Criação do animal cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                
                # List existing territories for animal association
                territories = facade.list_territories()
                print("Territórios cadastrados: ")
                existing_ids = []
                for territory in territories:
                    existing_ids.append(territory.id)
                    print(f"ID: {territory.id}, Nome: {territory.name}, X: {territory.x}, Y: {territory.y}")  
                territory_id = int(input("ID do território: "))
                if territory_id not in existing_ids:
                    # Notify if the chosen territory does not exist
                    print(colored("Erro: Território Inexistente", "red"))
                    time.sleep(1.5)
                    return
                if str(territory_id).strip() == "":
                    print(colored("Criação do animal cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                
                # Create a new animal associated with the territory via the facade
                facade.add_animal_to_territory(name, specie, age, territory_id)
                print(colored("Animal adicionado com sucesso!", "green"))
                time.sleep(1.5)

            elif user_input == 3:
                clear_screen() # Clear screen for animal deletion
                print(colored(f"----------------------------------------------- {colored("Excluir Animal", "light_blue")} {colored("----------------------------------------------", "light_cyan")}", "light_cyan"))
                animals = facade.list_animais() # Retrieve the list of animals
                print("Animais cadastrados:")
                if animals:
                    existing_ids = [] # List to store animal IDs
                    for animal in animals:
                        existing_ids.append(animal[0])
                        print(f"ID: {animal[0]}, Nome: {animal[1]}, Espécie: {animal[2]}, Idade: {animal[3]}, Descrição: {animal[4]}, ID território: {animal[5]},ID rastreador: {animal[6]}")
                    print("Pressione Enter para cancelar...\n")
                    id_delete = input("ID do animal para excluir: ")
                    if int(id_delete) not in existing_ids:
                        print(colored("Erro: Animal Inexistente", "red"))
                        time.sleep(1.5)
                        return
                    if id_delete.strip() == "":
                        print(colored("Criação do animal cancelada...", "yellow"))
                        time.sleep(1.5)
                        return                    
                    id_delete_int = int(id_delete)
                    # Delete the selected animal via the facade
                    facade.delete_animal(id_delete_int)
                    print(colored("Animal excluído com sucesso!", "green"))
                    time.sleep(1.5)
                else:
                    # Inform the admin if there are no animals to delete
                    print(colored("Nenhum animal para excluir!", "red"))
                    time.sleep(1.5)
            elif user_input == 4:
                return # Return to the admin menu

# Login screen function that handles user authentication and redirects based on role
def login_screen(facade):
    while True:
        clear_screen()  # Clear the terminal screen before displaying the login form
        # Display the login header using colored text
        print(colored(f"------------------------------ {colored("Fazer Login", "light_blue")} {colored("------------------------------", "light_cyan")}", "light_cyan"))
        email = input("Digite seu e-mail: ") # Prompt the user to enter their email
        senha = pwinput.pwinput(prompt="Digite sua senha: ", mask="*") # Prompt the user to enter their password (masked)

        # Retrieve admin and user records using the entered email
        admin = facade.get_admin_by_email(email)
        user = facade.get_user_by_email(email)

        # Verify if the credentials match an admin account using bcrypt
        if admin and bcrypt.checkpw(senha.encode(), admin[3]):
            # If admin authentication is successful, assign admin attributes and instantiate AdminUser role
            facade.admin = Admin(admin[1], admin[2], admin[3], admin[4])
            role = AdminUser()
        # Verify if the credentials match a regular user account
        elif user and bcrypt.checkpw(senha.encode(), user[3]):
            # If user authentication is successful, extract the user ID and instantiate RegularUser role
            user_id = user[0]
            role = RegularUser(user_id)
        else:
            # Notify the user if the login or password is invalid and repeat the loop
            print("Login ou senha inválidos, tente novamente.")
            time.sleep(1.5)
            continue
        
        # Display the corresponding menu for the authenticated role
        role.show_menu(facade)
        break

# Program initialization entry point
if __name__ == "__main__":
    facade = SystemFacade() # Obtain the SystemFacade singleton instance
    # Uncomment the following lines for initial setup actions, if necessary:
    # facade.create_admin("admin", "admin@admin.com", "admin", "9387-5652")
    # facade.delete_location_history())

    initialize_animal_trackers() # Initialize animal trackers from existing records in the database

    # Launch the login screen for user authentication
    login_screen(facade)
