# Definicion de clase de Usuario

# JSON
import json

# API

class User:
    

    # Constructor
    def __init__(self,first_name = None, last_name=None, username=None, email=None, password=None,
    type_identification = None, identification_number = None,telephone = None, gender = None, nationality = None, status = None):
        self._first_name = first_name
        self._last_name = last_name
        self._username = username
        self._email = email
        self._password = password
        self._type_identification = type_identification
        self._identification_number = identification_number
        self._telephone = telephone
        self._gender = gender
        self._nationality = nationality
        self._status = status
        self._user_dic = {}
    
    @property
    def full_name(self):
        return '{} {}'.format(self._first_name, self._last_name)
    
    @property
    def username(self):
        return str(self._username)
    
    @property
    def telephone(self):
        return str(self._telephone)
    
    @property
    def email(self):
        return str(self._email)
    
    @property
    def user_dic(self):               
        self._user_dic['full_name'] = self.full_name
        self._user_dic['username']=self.username
        self._user_dic['email']=self.email
        self._user_dic['telephone']=self.telephone
        return self._user_dic

    # toString
    def __str__(self):
        return json.dumps(self.user_dic)

if __name__ == '__main__':
    pass