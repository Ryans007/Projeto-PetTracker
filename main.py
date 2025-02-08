from patterns.facade import SystemFacade
import os
import time
import pwinput
from termcolor import colored
from utils import clear_screen

def home_screen():
    facade = SystemFacade()

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! GAMBIARRA não mexer se não for ajeitar :D
    #já ta criado no banco de dados, só descomentar essa linha se precisar criar a adm dnv
    #facade.create_admin("admin", "admin@admin.com", "admin", "83 40028922")
    while True:
        clear_screen()
        print("------------------------------ PetTracker ------------------------------")
        print("1 - Fazer Login")
        print("2 - Encerrar Programa")

        try:
            user_input = int(input("Escolha sua opção: "))
        except ValueError:
            print("Opção inválida! Digite um número.")
            continue

        if user_input == 1:
            login_screen(facade)
        elif user_input == 2:
            print("Encerrando o programa...")
            facade.close_connection()
            exit()
        else:
            print("Opção inválida! Tente novamente.")

def login_screen(facade):
    while True:
        clear_screen()
        print("\n------------------------------ Fazer Login ------------------------------")
        email = input("Digite seu e-mail: ")
        senha = pwinput.pwinput(prompt="Digite sua senha: ", mask="*")

        admin = facade.get_admin_by_email(email)

        if admin and admin[3] == senha:
            print(f"Login realizado como Administrador: {email}")
            admin_menu(facade)
            break
        else:
            print("Login ou senha inválidos, tente novamente.")

def admin_menu(facade):
    while True:
        clear_screen()
        print(f"\n------------------------------ Menu do Administrador ------------------------------")
        # print("1 - Visualizar Territórios")
        # print("2 - Criar Território")
        # print("3 - Adicionar Usuário")
        # print("4 - Adicionar Animal")
        # print("5 - Visualizar Animais")
        # print("6 - Visualizar Usuários")
        # print("7 - Voltar ao Menu Principal")
        # print("8 - Encerrar Programa")
        
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
            clear_screen()
            print(f"------------------------------ Territórios ------------------------------")
            territories = facade.list_territories()
            print("Territórios cadastrados: ")
            for territory in territories:
                print(f"ID: {territory[0]}, Nome: {territory[1]}, X: {territory[2]}, Y: {territory[3]}")

            print("\n1 - Visualizar Território")
            print("2 - Criar Território")
            print("3 - Deletar Território")
            print("4 - Voltar ao Menu Admin")
            print("5 - Encerrar Programa")

            try:
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue
            if user_input == 1:
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
                clear_screen()
                print(f"------------------------------ Novo Território ------------------------------")
                territory_name = input("\nNome do território: ")
                territory_x = int(input("Coordenada X do território: "))
                territory_y = int(input("Coordenada Y do território: "))
                facade.create_territory(territory_name, territory_x, territory_y)
                print(colored("Território criado com sucesso!", "green"))
                time.sleep(1.5)
            elif user_input == 3:
                clear_screen()
                print(f"------------------------------ Excluir Território ------------------------------")
                territories = facade.list_territories()
                print("Territórios cadastrados: ")
                for territory in territories:
                    print(f"ID: {territory[0]}, Nome: {territory[1]}, X: {territory[2]}, Y: {territory[3]}")
                id_delete = int(input("ID que você deseja excluir: "))
                facade.delete_territory(id_delete)
                print(colored("Território excluido com sucesso!", "green"))
                time.sleep(1.5) 
            elif user_input == 4:
                admin_menu(facade)
            elif user_input == 5:
                print("Encerrando o programa...")
                exit() 

        elif admin_input == 2:
            clear_screen()
            print(f"------------------------------ Usuários ------------------------------")
            
            users = facade.list_users()
            print("Usuários cadastrados: ")
            for users in users:
                print(f"ID: {users[0]}, Nome: {users[1]}, E-mail: {users[2]}, Celular: {users[4]}")

            print("\n1 - Criar Usuário")
            print("2 - Excluir Usuário")
            print("3 - Voltar ao Menu Admin")
            print("4 - Encerrar Programa")

            try:
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue
            if user_input == 1:
              clear_screen()
              print(f"------------------------------ Novo Usuário ------------------------------")
              user_name = input("\nNome do usuário: ")
              user_password = input("Senha do usuário: ")
              user_email = input("E-mail do usuário: ")
              user_celphone = input("Celular do usuário: ")
              territory_id = int(input("ID do território: "))
              facade.create_user(user_name, user_password, user_email, user_celphone, territory_id)
              print(colored("Usuário adicionado com sucesso!", "green"))
              time.sleep(1.5)
            elif user_input == 2:
                clear_screen()
                print(f"------------------------------ Excluir Usuário ------------------------------")
                users = facade.list_users()
                print("Usuários cadastrados: ")
                for users in users:
                    print(f"ID: {users[0]}, Nome: {users[1]}, E-mail: {users[2]}, Celular: {users[4]}")
                id_delete = int(input("\nID que você deseja excluir: "))
                facade.delete_user(id_delete)
                print(colored("Usuário excluido com sucesso!", "green"))
                time.sleep(1.5)       
            elif user_input == 3:
              admin_menu(facade)
            elif user_input == 4:
                  print("Encerrando o programa...")
                  exit() 
        elif admin_input == 3:
            clear_screen()
            print(f"------------------------------ Animais ------------------------------")
            animals = facade.list_animais()
            print("Animais cadastrados: ")
            for animal in animals:
                print(f"ID: {animal[0]}, Nome: {animal[1]}, Espécie: {animal[2]}, Idade: {animal[3]}, Descrição: {animal[4]}, ID território: {animal[5]},ID rastreador: {animal[6]}")
            print("\n1 - Criar Animal")
            print("2 - Excluir Animal")
            print("3 - Voltar ao Menu Admin")
            print("4 - Encerrar Programa")

            try:
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue
            
            if user_input == 1:
              clear_screen()
              print(f"------------------------------ Novo Animal ------------------------------")
              animal_name = input("\nNome do animal: ")
              animal_specie = input("Espécie do animal: ")
              animal_age = int(input("Idade do animal: "))
              territory_id = int(input("ID do território: "))
              facade.add_animal_to_territory(animal_name, animal_specie, animal_age, territory_id)
              print(colored("Animal adicionado com sucesso!", "green"))
              time.sleep(1.5)
              
            elif user_input == 2:
                clear_screen()
                print(f"------------------------------ Excluir Animal ------------------------------")
                animals = facade.list_animais()
                print("Usuários cadastrados: ")
                for animal in animals:
                     print(f"ID: {animal[0]}, Nome: {animal[1]}, Espécie: {animal[2]}, Idade: {animal[3]}, Descrição: {animal[4]}, ID território: {animal[5]},ID rastreador: {animal[6]}")
                id_delete = int(input("\nID que você deseja excluir: "))
                facade.delete_animal(id_delete)
                print(colored("Animal excluido com sucesso!", "green"))
                time.sleep(1.5)    
            elif user_input == 3:
                admin_menu(facade)
            elif user_input == 4:
                exit()
        elif admin_input == 4:
          home_screen()
        elif admin_input == 5:
            print("Encerrando o programa...")
            facade.close_connection()
            exit()

if __name__ == "__main__":
    home_screen()