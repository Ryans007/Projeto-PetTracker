import bcrypt
import os    

# Função para limpar o terminal
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Função para criptografar senhas    
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)