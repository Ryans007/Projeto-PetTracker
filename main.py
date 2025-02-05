import os
from _class.facade import SystemFacade  # Importando o Facade


facade = SystemFacade()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def home_screen():
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
            login_screen()
        elif user_input == 2:
            print("Encerrando o programa...")
            exit()
        else:
            print("Opção inválida! Tente novamente.")

def login_screen():
    while True:
        clear_screen()
        print("\n------------------------------ Fazer Login ------------------------------")
        email = input("Digite seu e-mail: ")
        senha = input("Digite sua senha: ")

        # Verificação simples de login com admin
        if email == "admin" and senha == "admin":
            print(f"Login realizado como Administrador: {email}")
            admin_menu(facade)
            break
        else:
            print("Login ou senha inválidos, tente novamente.")

def admin_menu(facade):
    territory = None

    while True:

        if territory is None:
            print("\n------------------------------ Cadastro de Território ------------------------------")
            territory_name = input("Nome do território: ")
            territory_h = int(input("Altura do território: "))
            territory_w = int(input("Largura do território: "))
            
            territory = facade.create_territory(territory_name, territory_h, territory_w)
            print(f"Território '{territory_name}' criado com sucesso!")
            continue 


        clear_screen()
        print(f"\n------------------------------ Menu do Administrador ------------------------------")
        print("1 - Visualizar Territórios")
        print("2 - Criar Território")
        print("3 - Adicionar Usuário")
        print("4 - Adicionar Animal")
        print("5 - Voltar ao Menu Principal")
        print("6 - Encerrar Programa")

        try:
            admin_input = int(input("Escolha sua opção: "))
        except ValueError:
            print("Opção inválida! Digite um número.")
            continue

        if admin_input == 1:
            print("\n------------------------------ Territórios Cadastrados ------------------------------")                      
            print("1 - Visualizar Animais")
            print("2 - Voltar ao Menu Admin")
            print("3 - Encerrar Programa")

            try:
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue
            
            if user_input == 1:
                #territory = user.territory
                print(facade.show_territory(territory))

            elif user_input == 2:
                admin_menu()  

            elif user_input == 3:
                print("Encerrando o programa...")
                exit()

        elif admin_input == 2:
            territory_name = input("\nNome do território: ")
            territory_h = int(input("Altura do território: "))
            territory_w = int(input("Largura do território: "))

            territory = facade.create_territory(territory_name, territory_h, territory_w)
            print(f"Território criado com sucesso!")

        elif admin_input == 3:
            user_name = input("\nNome do usuário: ")
            user_email = input("E-mail do usuário: ")
            user_celphone = input("Celular do usuário: ")

            user = facade.create_user(user_name, user_email, user_celphone, territory)

            admin_menu(facade)

            #territory_name = input("Nome do território onde o usuário será cadastrado: ")
            
            #if territory:
                #user = facade.create_user(user_name, user_email, user_celphone, territory)
                #print(f"Usuário adicionado ao território.")
            #else:
                #print("Território não encontrado!")

        elif admin_input == 4:
            animal_name = input("\nNome do animal: ")
            animal_race = input("Tipo de animal: ")
            animal_age = int(input("Idade do animal: "))

            #territory_name = input("Nome do território onde o animal será cadastrado: ")
            #territory = facade.get_territory_by_name(territory_name)

            #if territory:
                #facade.add_animal_to_territory(admin, animal_name, animal_race, animal_age, territory)
                #print(f"Animal {animal_name} adicionado ao território.")
            #else:
                #print("Território não encontrado!")

        elif admin_input == 5:
            return  

        elif admin_input == 6:
            print("Encerrando o programa...")
            exit()

def user_menu(user, territory):
    while True:
        clear_screen()
        print(f"\n------------------------------ Vizualizar animais ------------------------------")
        print("1 - Visualizar Animais")
        print("2 - Voltar ao Menu Principal")
        print("3 - Encerrar Programa")

        try:
            user_input = int(input("Escolha sua opção: "))
        except ValueError:
            print("Opção inválida! Digite um número.")
            continue

        if user_input == 1:
            #territory = user.territory
            print(facade.show_territory(territory))

        elif user_input == 2:
            return  

        elif user_input == 3:
            print("Encerrando o programa...")
            exit()

if __name__ == "__main__":
    home_screen()
    

