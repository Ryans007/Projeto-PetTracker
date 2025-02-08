import bcrypt    

# Função para criptografar senhas    
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)