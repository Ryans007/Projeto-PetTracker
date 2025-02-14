from abc import ABC, abstractmethod
#import os
import time
import bcrypt
import pwinput
from termcolor import colored
from patterns.facade import SystemFacade
from utils import clear_screen
from _class.person import Admin

# Classe abstrata para os papéis dos usuários
class UserRole(ABC):
    @abstractmethod
    def show_menu(self, facade):
        pass

# Classe para usuários comuns (apenas visualizar territórios)
class RegularUser(UserRole):
    def show_menu(self, facade):
        while True:
            clear_screen()
            print("\n------------------------------ Menu do Usuário ------------------------------")
            print("1 - Visualizar Território")
            print("2 - Voltar ao Menu Principal")
            print("3 - Encerrar Programa")

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
                    print(f"ID: {territory[0]}, Nome: {territory[1]}, X: {territory[2]}, Y: {territory[3]}")
                    #print(facade.show_territory(territory))
                    try:
                        territory_id = int(input("Digite o ID do território que deseja visualizar: "))

                        territory = None
                        for t in territories:
                            if t[0] == territory_id:  
                                territory = t
                                break
                        if territory:
                            print(f"Visualizando território ID {territory[0]} - {territory[1]}")
                            #print(territory)
                            #print(facade.show_territory(territory[2], territory[3]))
                            facade.show_territory(territory[2], territory[3])
                            time.sleep(10)
                        else:
                            print(colored("Território não encontrado!", "red"))
                    except ValueError:
                        print("ID inválido! Digite um número.")  
            elif user_input == 2:
                return  # Volta ao menu principal

            elif user_input == 3:
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
            print("5 - Encerrar Programa")

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
                    facade.show_territory(territory_id)
                    time.sleep(10)
                except ValueError:
                    print("ID inválido! Digite um número.")  

            elif user_input == 2:
                clear_screen()
                print(f"------------------------------ Novo Território ------------------------------")
                name = input("\nNome do território: ")
                x = int(input("Coordenada X: "))
                y = int(input("Coordenada Y: "))
                facade.create_territory(name, x, y)
                print(colored("Território criado com sucesso!", "green"))
                time.sleep(1.5)

            elif user_input == 3:
                clear_screen()
                print(f"------------------------------ Excluir Território ------------------------------")
                territories = facade.list_territories()
                print("Territórios cadastrados: ")
                for territory in territories:
                    print(f"ID: {territory.id}, Nome: {territory.name}, X: {territory.x}, Y: {territory.y}")
                id_delete = int(input("\nID do território para deletar: "))
                facade.delete_territory(id_delete)
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
                    print(f"ID: {user._Person__id}, Nome: {user.name}, E-mail: {user.email}, Celular: {user.celphone}")
                input("\nPressione Enter para continuar...")

            elif user_input == 2:
                clear_screen()
                print(f"------------------------------ Novo Usuário ------------------------------")
                name = input("\nNome: ")
                password = input("Senha: ")
                email = input("E-mail: ")
                phone = input("Celular: ")
                territory_id = int(input("ID do território: "))
                facade.create_user(name, password, email, phone, territory_id)
                print(colored("Usuário criado com sucesso!", "green"))
                time.sleep(1.5)

            elif user_input == 3:
                clear_screen()
                print(f"------------------------------ Excluir Usuário ------------------------------")
                users = facade.list_users()
                print("Usuários cadastrados: ")
                for user in users:
                    print(f"ID: {user._Person__id}, Nome: {user.name}, E-mail: {user.email}, Celular: {user.celphone}")
                id_delete = int(input("\nID do usuário para excluir: "))
                facade.delete_user(id_delete)
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
                name = input("\nNome: ")
                specie = input("Espécie: ")
                age = int(input("Idade: "))
                territory_id = int(input("ID do território: "))
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
                id_delete = int(input("\nID do animal para excluir: "))
                facade.delete_animal(id_delete)
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
            role = RegularUser()
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
