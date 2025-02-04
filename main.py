from _class.person import Admin
from _class.territory import Territory
from _class.tracker import Tracker
import os

def main():
  # admin = Admin("Rogerio", "rogerio@gmail.com", "9233-9483")
  
  # territory = Territory("IFPB", 23, 45, 50, 70)
  
  # tracker = Tracker(id = 12, state = True)
  
  # admin.add_animal("Pedro", "Gato", 12, tracker, territory)
  
  # admin.add_user("Gabriel", "gabriel@gmail.com", "7645-3657", territory)
  
  # for user in admin.user_list:
  #   print(territory.show_territory())
    
  while True:
    print("--------------------PetTracker----------------------")
    print("Pressione a opção desejada: ")
    user_input = int(input("1 - Criar Admin"))
    
    if user_input == 1:
      admin_name = input("Nome: ") 
      admin_email = input("E-mail: ")
      admin_celphone = input("Celular: ")
      
      admin = Admin(admin_name, admin_email, admin_celphone)
      
      print(f"Você está logado como {admin.name}")
      
      admin_input = int(input("Pressione a opção desejada\n1-Criar Territorio"))
      
      if admin_input == 1:
        territory_name = input("Nome do territorio: ")
        territory_h = input("Altura do territorio: ")
        territory_w = input("Largura do territorio: ")
        
        territory = Territory(territory_name, int(territory_h), int(territory_w), admin.name)   
        
        admin_input = int(input("Pressione a opção desejada\n1-Adicionar Usúario\n2-Adicionar Animal"))
        
        if admin_input == 1:
          user_name = input("Nome do usúario: ")
          user_email = input("E-mail do usúario: ")
          user_celphone = input("Celular do usúario: ")
          
          user = admin.add_user(user_name, user_email, user_celphone, territory)
          
          print("Agora adicione o animal: ")
          
          animal_name = input("Nome do animal: ")
          animal_race = input("Tipo de animal: ")
          animal_age = input("Idade do animal: ")

          os.system("cls")
          
          user_action = int(input("Escolha a opção desejada:\n 1-Vizualizar Animal"))
          
          if user_action == 1:
              os.system("cls")
              for user in admin.user_list:
                print(territory.show_territory())
          
          
      

if __name__ == "__main__":
  main()