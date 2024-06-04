import requests

# JSON
import json

# LISTAR USUARIOS
def get_users():
    url = 'http://127.0.0.1:8000/users/api/users/'
    response = requests.get(url)

    if response.status_code == 200:
        user_data = response.json()
        
        return user_data
    else:
        return None



def comparar(atributo,valor):
    dato = get_users() 
    for comparacion in dato:
        if(comparacion['{}'.format(atributo)] == valor):
            print(comparacion['{}'.format(atributo)])
            return True
    
    return False
    



if __name__ == '__main__':
    
    print(comparar('email','eloicx@gmail.com'))
    
    