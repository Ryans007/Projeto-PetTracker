from _class.person import *

def main():
  admin = Admin("Rogerio", "rogerio@gmail.com", "9233-9483")
  
  territory = Territory("IFPB", 23, 45, 50, 70)
  
  tracker = Tracker(id = 12, state = True)
  
  admin.add_animal("Pedro", "Gato", 12, tracker, territory)
  
  admin.add_user("Gabriel", "gabriel@gmail.com", "7645-3657", territory)
  
  print(admin)
  
  for user in admin.user_list:
    print(user)

if __name__ == "__main__":
  main()