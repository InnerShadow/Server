import bcrypt

class Encoder:
    def __init__(self):
        pass


    def getSaltAndHash(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return salt, hashed_password
    

    def checkpw(self, try_password : str, passwords_hash : str):
        return bcrypt.checkpw(try_password.encode('utf-8'), passwords_hash)
    
