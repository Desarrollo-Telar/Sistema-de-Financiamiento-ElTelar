

import sys
import os

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# JSON
import json

from .get_all import users

def comparar(lista,atributo, valor):
    dic = {}
    for x in lista:
        if (x['{}'.format(atributo)] == valor):
            dic['user_id'] = x['user_id']
    
    return dic





if __name__ == '__main__':
    
   

    print(users())

   
    