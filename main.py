from _class.facade import SystemFacade
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

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
        senha = input("Digite sua senha: ")

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
            print(f"\n------------------------------ Territórios ------------------------------")
            # territories = facade.list_territories()
            # print("Territórios cadastrados: ")
            # for territory in territories:
            #     print(f"ID: {territory[0]}, Nome: {territory[1]}, X: {territory[2]}, Y: {territory[3]}")

            print("\n1 - Visualizar Território")
            print("2 - Voltar ao Menu Admin")
            print("3 - Encerrar Programa")

            try:
                user_input = int(input("Escolha sua opção: "))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue

            if user_input == 1:
                print(facade.show_territory(territory))

                # try:
                #     territory_id = int(input("Digite o ID do território que deseja visualizar: "))

                #     territory = None
                #     for t in territories:
                #         if t[0] == territory_id:  
                #             territory = t
                #             break

                #     if territory:
                #         print(f"Visualizando território ID {territory[0]} - {territory[1]}")
                #         print(territory)
                #         print(facade.show_territory(territory))
                #     else:
                #         print("Território não encontrado!")
                # except ValueError:
                #     print("ID inválido! Digite um número.")    
                           
            elif user_input == 2:
                admin_menu(facade)

            elif user_input == 3:
                print("Encerrando o programa...")
                exit() 
            

        elif admin_input == 2:
            territory_name = input("\nNome do território: ")
            territory_x = int(input("Coordenada X do território: "))
            territory_y = int(input("Coordenada Y do território: "))
            facade.create_territory(territory_name, territory_x, territory_y)
            print(f"Território criado com sucesso!")

        elif admin_input == 3:
            user_name = input("\nNome do usuário: ")
            user_email = input("E-mail do usuário: ")
            user_celphone = input("Celular do usuário: ")
            territory_id = int(input("ID do território: "))
            facade.create_user(user_name, user_email, user_celphone, territory_id)
            print(f"Usuário adicionado com sucesso!")

        elif admin_input == 4:
            animal_name = input("\nNome do animal: ")
            animal_specie = input("Espécie do animal: ")
            animal_age = int(input("Idade do animal: "))
            territory_id = int(input("ID do território: "))
            facade.add_animal_to_territory(animal_name, animal_specie, animal_age, territory_id)
            print(f"Animal adicionado com sucesso!")

        elif admin_input == 5:
            return

        elif admin_input == 6:
            print("Encerrando o programa...")
            facade.close_connection()
            exit()

if __name__ == "__main__":
    home_screen()