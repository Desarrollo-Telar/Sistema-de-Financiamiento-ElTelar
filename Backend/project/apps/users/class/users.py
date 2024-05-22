# Definicion de clase de Usuario

import json

class User:
    contador = 0

    # Constructor
    def __init__(self, id,first_name = None, last_name=None, username=None, email=None, telephone = None):
        User.contador+=1
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._username = username
        self._email = email
        self._telephone = telephone
        self._user_dic = {}
    
    @property
    def id(self):
        return str(self._id)
    
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
        self._user_dic['contador']=User.contador
        self._user_dic['id'] = self.id
        self._user_dic['full_name'] = self.full_name
        self._user_dic['username']=self.username
        self._user_dic['email']=self.email
        self._user_dic['telephone']=self.telephone
        return self._user_dic

    # toString
    def __str__(self):
        return json.dumps(self.user_dic)