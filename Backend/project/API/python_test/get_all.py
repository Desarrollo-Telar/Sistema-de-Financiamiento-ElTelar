import requests

# JSON
import json

# URLS
from API.urls.urls_api import URL as urls



# LISTAR
def get_for_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        return data
    else:
        return None



# USUARIOS
def users():
    return get_for_url(urls['api_url_usuarios'])

# CLIENTES
customers = get_for_url(urls['api_url_cliente'])
# DIRECCIONES
address = get_for_url(urls['api_url_direccion'])
# CONDICCION MIGRATORIO
condicion_migratoria = get_for_url(urls['api_url_condicion_migratoria'])
# REFERENCIA
referencia = get_for_url(urls['api_url_referencia'])
# INFORMACION LABORAL
informacion_laboral = get_for_url(urls['api_url_informacion_laboral'])
# OTRA INFORMACION LABORAL
otra_informacion = get_for_url(urls['api_url_otra_informacion_laboral'])
# PLAN DE INVERSION
plan_inversion = get_for_url(urls['api_url_investment_plan'])