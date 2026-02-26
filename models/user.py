import bcrypt

class User:
    def __init__(self, username, password):
        self._id = -1
        self.username = username
        self._hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    
    @property
    def id(self):
        return self._id
    
    @property
    def hashed_password(self):
        return self._hashed_password
    
    def set_new_pass(self, old_password, new_password):
        
        if bcrypt.checkpw(old_password, self._hashed_password):
            self._hashed_password = bcrypt.hashpw(new_password, bcrypt.gensalt())
            return self._hashed_password
        else:
            print("Hasło nie pasuje")

        