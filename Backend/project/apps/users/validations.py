import re


def validar_correo(correo):
    # Expresión regular básica para validar el formato del correo electrónico
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Lista de dominios conocidos
    dominios_conocidos = ['gmail.com', 'yahoo.com', 'outlook.com']  # Agrega más dominios según sea necesario
    
    # Validar el formato del correo electrónico
    if not re.match(regex, correo):
        return False
    
    # Obtener el dominio del correo electrónico
    dominio = correo.split('@')[-1]
    
    # Verificar si el dominio está en la lista de dominios conocidos
    if dominio not in dominios_conocidos:
        return False
    
    return True


