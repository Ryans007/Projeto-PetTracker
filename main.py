import os
from _class.facade import SystemFacade  # Importando o Facade

# Inicializa o Facade
facade = SystemFacade()

def main():
    while True:
        print("-------------------- PetTracker ----------------------")
        print("Pressione a opção desejada: ")
        user_input = int(input("1 - Criar Admin\n2 - Encerrar Programa\n"))

        if user_input == 1:
            # Criando o Admin
            admin_name = input("Nome: ") 
            admin_email = input("E-mail: ")
            admin_celphone = input("Celular: ")
            
            admin = facade.create_admin(admin_name, admin_email, admin_celphone)
            print(f"Você está logado como {admin.name}")

            admin_input = int(input("Pressione a opção desejada\n1 - Criar Território\n2 - Sair\n"))
            
            if admin_input == 1:
                # Criando o Território
                territory_name = input("Nome do território: ")
                territory_h = input("Altura do território: ")
                territory_w = input("Largura do território: ")
                
                territory = facade.create_territory(territory_name, int(territory_h), int(territory_w))

                admin_input = int(input("Pressione a opção desejada\n1 - Adicionar Usuário\n2 - Adicionar Animal\n3 - Sair\n"))

                if admin_input == 1:
                    # Adicionando Usuário
                    user_name = input("Nome do usuário: ")
                    user_email = input("E-mail do usuário: ")
                    user_celphone = input("Celular do usuário: ")
                    
                    user = facade.create_user(user_name, user_email, user_celphone, territory)

                    print("Usuário criado com sucesso!\nAgora, adicione o animal:")

                    # Adicionando Animal
                    animal_name = input("Nome do animal: ")
                    animal_race = input("Tipo de animal: ")
                    animal_age = input("Idade do animal: ")

                    #animal = facade.add_animal_to_territory(animal_name, animal_race, animal_age)

                    # Exibindo os animais no território
                    os.system("cls")
                    user_action = int(input("Escolha a opção desejada:\n 1 - Visualizar Animais\n"))
                    
                    if user_action == 1:
                        os.system("cls")
                        print(f"Animais no território {territory.name}:")
                        print(territory.show_territory())

                elif admin_input == 2:
                    # Adicionando Animal (sem usuário)
                    animal_name = input("Nome do animal: ")
                    animal_race = input("Tipo de animal: ")
                    animal_age = input("Idade do animal: ")

                    #animal = facade.add_animal_to_territory(animal_name, animal_race, animal_age, territory)

                    # Exibindo os animais no território
                    os.system("cls")
                    print(f"Animais no território {territory.name}:")
                    print(territory.show_territory())

        elif user_input == 2:
            print("Encerrando o programa...")
            exit()

if __name__ == "__main__":
    main()
