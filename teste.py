# Teste seus códigos aquiii
from abc import ABC, abstractmethod
import os
import time
import pwinput
from termcolor import colored
from patterns.facade import SystemFacade

# Função para limpar a tela
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

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
            print("1 - Visualizar Territórios")
            print("2 - Voltar ao Menu Principal")
            print("3 - Encerrar Programa")

            try:
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue

            if user_input == 1:
                territories = facade.list_territories()
                print("\nTerritórios cadastrados:")
                for territory in territories:
                    print(f"ID: {territory[0]}, Nome: {territory[1]}, X: {territory[2]}, Y: {territory[3]}")
                input("\nPressione Enter para continuar...")

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
            print("1 - Listar Territórios")
            print("2 - Criar Território")
            print("3 - Deletar Território")
            print("4 - Voltar ao Menu Admin")

            try:
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue

            if user_input == 1:
                territories = facade.list_territories()
                print("\nTerritórios cadastrados:")
                for territory in territories:
                    print(f"ID: {territory[0]}, Nome: {territory[1]}, X: {territory[2]}, Y: {territory[3]}")
                input("\nPressione Enter para continuar...")

            elif user_input == 2:
                name = input("Nome do território: ")
                x = int(input("Coordenada X: "))
                y = int(input("Coordenada Y: "))
                facade.create_territory(name, x, y)
                print(colored("Território criado com sucesso!", "green"))
                time.sleep(1.5)

            elif user_input == 3:
                id_delete = int(input("ID do território para deletar: "))
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
                    print(f"ID: {user[0]}, Nome: {user[1]}, E-mail: {user[2]}, Celular: {user[4]}")
                input("\nPressione Enter para continuar...")

            elif user_input == 2:
                name = input("Nome: ")
                password = input("Senha: ")
                email = input("E-mail: ")
                phone = input("Celular: ")
                territory_id = int(input("ID do território: "))
                facade.create_user(name, password, email, phone, territory_id)
                print(colored("Usuário criado com sucesso!", "green"))
                time.sleep(1.5)

            elif user_input == 3:
                id_delete = int(input("ID do usuário para excluir: "))
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
                name = input("Nome: ")
                specie = input("Espécie: ")
                age = int(input("Idade: "))
                territory_id = int(input("ID do território: "))
                facade.add_animal_to_territory(name, specie, age, territory_id)
                print(colored("Animal adicionado com sucesso!", "green"))
                time.sleep(1.5)

            elif user_input == 3:
                id_delete = int(input("ID do animal para excluir: "))
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

        if admin and admin[3] == senha:
            role = AdminUser()
        elif user and user[3] == senha:
            role = RegularUser()
        else:
            print("Login ou senha inválidos, tente novamente.")
            continue

        role.show_menu(facade)
        break

# Inicialização
if __name__ == "__main__":
    facade = SystemFacade()
    login_screen(facade)
