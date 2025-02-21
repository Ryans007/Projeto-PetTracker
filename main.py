from abc import ABC, abstractmethod
import time
import bcrypt
import pwinput
from termcolor import colored
from _class import territory
from patterns.facade import SystemFacade
from utils import clear_screen
from _class.person import Admin
import threading

# Classe abstrata para os papéis dos usuários
class UserRole(ABC):
    @abstractmethod
    def show_menu(self, facade):
        pass

# Classe para usuários comuns (apenas visualizar territórios)
class RegularUser(UserRole):
    def __init__(self, user_id: int) -> None:
        super().__init__()
        self.user_id = user_id
    def show_menu(self, facade):
        while True:
            clear_screen()
            print("\n------------------------------ Menu do Usuário ------------------------------")
            print("1 - Visualizar Território")
            print("2 - Voltar ao Menu Principal")
            print("3 - Deslogar")
            print("4 - Encerrar Programa")

            try:
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue

            if user_input == 1:
                clear_screen()
                # Cria o evento de parada e inicia a thread da simulação
                stop_event = threading.Event()
                sim_thread = threading.Thread(target=lambda: facade.show_territory_user(self.user_id, stop_event))
                sim_thread.start()
                print("\nA simulação do território foi iniciada em uma nova janela.")
                print("Para voltar ao menu, volte ao terminal do menu e pressione Enter.")
                input() # Aguarda o usuário pressionar Enter no terminal principal
                # Sinaliza para a simulação encerrar e aguarda a thread terminar
                stop_event.set()
                sim_thread.join()
            elif user_input == 2:
                return  # Volta ao menu principal
            elif user_input == 3:
                login_screen(facade)
            elif user_input == 4:
                print("Encerrando o programa...")
                facade.close_connection()
                exit()

# Classe para administradores (acesso total)
class AdminUser(UserRole):
    def show_menu(self, facade):
        while True:
            clear_screen()
            print("\n------------------------------ Menu do Administrador ------------------------------")
            print("1 - Opções de Territórios")
            print("2 - Opções de Usuários")
            print("3 - Opções de Animais")
            print("4 - Voltar ao Menu Principal")
            print("5 - Deslogar")
            print("6 - Encerrar Programa")

            try:
                admin_input = int(input("Escolha sua opção: "))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue

            if admin_input == 1:
                self.territory_options(facade)
            elif admin_input == 2:
                self.user_options(facade)
            elif admin_input == 3:
                self.animal_options(facade)
            elif admin_input == 4:
                return  # Volta ao menu principal
            elif admin_input == 5:
                login_screen(facade)
            elif admin_input == 6:
                print("Encerrando o programa...")
                facade.close_connection()
                exit()

    def territory_options(self, facade):
        while True:
            clear_screen()
            print("\n------------------------------ Gerenciar Territórios ------------------------------")
            print("1 - Vizualizar Territórios")
            print("2 - Criar Território")
            print("3 - Deletar Território")
            print("4 - Voltar ao Menu Admin")

            try:
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue

            if user_input == 1:
                clear_screen()
                print(f"------------------------------ Territórios ------------------------------")
                territories = facade.list_territories()
                print("Territórios cadastrados: ")
                for territory in territories:
                    print(f"ID: {territory.id}, Nome: {territory.name}, X: {territory.x}, Y: {territory.y}")
                try:
                    territory_id = int(input("Digite o ID do território que deseja visualizar: "))
                    # Cria o evento de parada e inicia a thread da simulação
                    stop_event = threading.Event()
                    sim_thread = threading.Thread(target=lambda: facade.show_territory_admin(territory_id, stop_event))
                    sim_thread.start()
                    print("\nA simulação do território foi iniciada em uma nova janela.")
                    print("Para voltar ao menu, volte ao terminal do menu e pressione Enter.")
                    input() # Aguarda o usuário pressionar Enter no terminal principal
                    # Sinaliza para a simulação encerrar e aguarda a thread terminar
                    stop_event.set()
                    sim_thread.join()
                except ValueError:
                    print("ID inválido! Digite um número.")  

            elif user_input == 2:
                clear_screen()
                print(f"------------------------------ Novo Território ------------------------------")
                print(f"Pressione Enter para cancelar...")
                
                name = input("Nome do território: ")
                if name.strip() == "":
                    print(colored("Criação de território cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                x = input("Coordenada X: ")
                if x.strip() == "":
                    print(colored("Criação de território cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                x_int = int(x)
                
                y = input("Coordenada Y: ")
                if y.strip() == "":
                    print(colored("Criação de território cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                y_int = int(y)
                
                facade.create_territory(name, x_int, y_int)
                print(colored("Território criado com sucesso!", "green"))
                time.sleep(1.5)

            elif user_input == 3:
                clear_screen()
                print(f"------------------------------ Excluir Território ------------------------------")
                territories = facade.list_territories()
                print("Territórios cadastrados: ")
                for territory in territories:
                    print(f"ID: {territory.id}, Nome: {territory.name}, X: {territory.x}, Y: {territory.y}")
                print("Pressione Enter para cancelar...")
                
                id_delete = input("\nID do território para deletar: ")
                if id_delete.strip() == "":
                    print(colored("Exclusão de território cancelada...", "yellow"))
                    time.sleep(1.5)
                    return
                
                id_delete_int = int(id_delete) 
                facade.delete_territory(id_delete_int)
                print(colored("Território excluído com sucesso!", "green"))
                time.sleep(1.5)

            elif user_input == 4:
                return  # Volta ao menu do admin

    def user_options(self, facade):
        while True:
            clear_screen()
            print("\n------------------------------ Gerenciar Usuários ------------------------------")
            print("1 - Listar Usuários")
            print("2 - Criar Usuário")
            print("3 - Excluir Usuário")
            print("4 - Voltar ao Menu Admin")

            try:
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue

            if user_input == 1:
                users = facade.list_users()
                print("\nUsuários cadastrados:")
                for user in users:
                    print(f"ID: {user.id}, Nome: {user.name}, E-mail: {user.email}, Celular: {user.celphone}")
                input("\nPressione Enter para continuar...")

            elif user_input == 2:
                clear_screen()
                territories = facade.show_territory_null()
                
                if territories:
                    print(f"------------------------------ Novo Usuário ------------------------------")
                    print("Pressione Enter para cancelar...")
                    
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
                    territories = facade.show_territory_null()
                    for territorie in territories:
                        print(f"ID: {territorie.id}, Nome: {territorie.name}, X: {territorie.x}, Y: {territorie.y}")
                
                        territory_id = input("ID do território: ")
                        if territory_id.strip() == "":
                            print(colored("Criação de usuário cancelada...", "yellow"))
                            time.sleep(1.5)
                            return 
                        territory_id_int = int(territory_id)
                        facade.create_user(name, password, email, phone, territory_id_int)
                        print(colored("Usuário criado com sucesso!", "green"))
                        time.sleep(1.5)
                else:
                    print(colored("Não foi possívei criar o usuário!\nTodos os territórios possuem dono", "red"))
                    input("\nPressione Enter para continuar...")

            elif user_input == 3:
                clear_screen()
                print(f"------------------------------ Excluir Usuário ------------------------------")
                users = facade.list_users()
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
                facade.delete_user(id_delete_int)
                print(colored("Usuário excluído com sucesso!", "green"))
                time.sleep(1.5)

            elif user_input == 4:
                return

    def animal_options(self, facade):
        while True:
            clear_screen()
            print("\n------------------------------ Gerenciar Animais ------------------------------")
            print("1 - Listar Animais")
            print("2 - Adicionar Animal")
            print("3 - Excluir Animal")
            print("4 - Voltar ao Menu Admin")
            
            try:
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue

            if user_input == 1:
                animals = facade.list_animais()
                print("\nAnimais cadastrados:")
                for animal in animals:
                    print(f"ID: {animal[0]}, Nome: {animal[1]}, Espécie: {animal[2]}, Idade: {animal[3]}")
                input("\nPressione Enter para continuar...")

            elif user_input == 2:
                clear_screen()
                print(f"------------------------------ Novo Animal ------------------------------")
                print("Pressione Enter para cancelar...")
                
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
                  
                territory_id = int(input("ID do território: "))
                if str(territory_id).strip() == "":
                    print(colored("Criação do animal cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                
                facade.add_animal_to_territory(name, specie, age, territory_id)
                print(colored("Animal adicionado com sucesso!", "green"))
                time.sleep(1.5)

            elif user_input == 3:
                clear_screen()
                print(f"------------------------------ Excluir Animal ------------------------------")
                animals = facade.list_animais()
                print("Usuários cadastrados: ")
                for animal in animals:
                     print(f"ID: {animal[0]}, Nome: {animal[1]}, Espécie: {animal[2]}, Idade: {animal[3]}, Descrição: {animal[4]}, ID território: {animal[5]},ID rastreador: {animal[6]}")
                print("Pressione Enter para cancelar...")
                
                id_delete = input("\nID do animal para excluir: ")
                if id_delete.strip() == "":
                    print(colored("Criação do animal cancelada...", "yellow"))
                    time.sleep(1.5)
                    return 
                
                id_delete_int = int(id_delete)
                facade.delete_animal(id_delete_int)
                print(colored("Animal excluído com sucesso!", "green"))
                time.sleep(1.5)

            elif user_input == 4:
                return

# Tela de login
def login_screen(facade):
    while True:
        clear_screen()
        print("\n------------------------------ Fazer Login ------------------------------")
        email = input("Digite seu e-mail: ")
        senha = pwinput.pwinput(prompt="Digite sua senha: ", mask="*")

        admin = facade.get_admin_by_email(email)
        user = facade.get_user_by_email(email)

        if admin and bcrypt.checkpw(senha.encode(), admin[3]):
            facade.admin = Admin(admin[1], admin[2], admin[3], admin[4])
            role = AdminUser()
        elif user and bcrypt.checkpw(senha.encode(), user[3]):
            territory_id = user[5]
            role = RegularUser(territory_id)
        else:
            print("Login ou senha inválidos, tente novamente.")
            time.sleep(1.5)
            continue

        role.show_menu(facade)
        break

# Inicialização
if __name__ == "__main__":
    facade = SystemFacade()
    #facade.create_admin("ryan", "ryan@gmail.com", "1234", "9387-5652")
    login_screen(facade)
