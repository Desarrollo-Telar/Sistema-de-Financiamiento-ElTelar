import os
import requests
from dotenv import load_dotenv

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class ReceptorApiClient:
    """
    Cliente para consumir la API de consulta de receptores de FEEL (FEL)
    mediante el endpoint https://consultareceptores.feel.com.gt/rest/action
    """
    
    BASE_URL = "https://consultareceptores.feel.com.gt/rest/action"

    def __init__(self):
        """
        Inicializa el cliente cargando el Código y Clave de Emisor 
        desde las variables de entorno.
        """
        # Se asume que estas variables de entorno son para el emisor
        self.emisor_codigo = os.getenv("USUARIO_API")
        self.emisor_clave = os.getenv("LLAVE_API")

        # 📌 Validación básica
        if not all([self.emisor_codigo, self.emisor_clave]):
            raise ValueError("Faltan variables de entorno (EMISOR_CODIGO y/o EMISOR_CLAVE) para la API de Consulta de Receptores FEL")

    def consultar_nit(self, nit_a_consultar: str):
        """
        Realiza la consulta del NIT de un posible receptor a la API de FEEL.

        Args:
            nit_a_consultar (str): El NIT que se desea consultar (ej: '1808964K' o 'CF').

        Returns:
            dict: El resultado de la API (JSON) o un diccionario de error.
        """
        
        # 1. Preparar el Body (Payload) de la solicitud
        payload = {
            "emisor_codigo": self.emisor_codigo,
            "emisor_clave": self.emisor_clave,
            "nit_consulta": nit_a_consultar
        }

        # 2. Preparar los Headers
        headers = {
            "Content-Type": "application/json"
        }

        try:
            # 3. Realizar la solicitud POST
            response = requests.post(
                self.BASE_URL,
                headers=headers,
                json=payload  # Usamos 'json' para enviar el diccionario como JSON
            )
            
            # 4. Manejar la respuesta
            # La API de FEEL generalmente devuelve 200, incluso si hay errores
            # internos, por lo que es importante revisar el cuerpo de la respuesta.
            
            # Intentar decodificar la respuesta como JSON
            try:
                result_data = response.json()
            except requests.exceptions.JSONDecodeError:
                # Si la respuesta no es un JSON válido
                return {
                    "status": "error",
                    "http_code": response.status_code,
                    "message": "La API no devolvió una respuesta JSON válida.",
                    "response": response.text
                }

            # 5. Retornar el resultado (ya sea éxito o error reportado por la API)
            return result_data

        except requests.exceptions.RequestException as e:
            # Capturar errores de conexión, timeout, DNS, etc.
            return {"status": "exception", "message": f"Error de conexión con la API: {e}"}

# ----------------------------------------------------------------------
# Ejemplo de Uso (Asegúrate de configurar tu archivo .env primero)
# ----------------------------------------------------------------------

# 1. Asegúrate de tener un archivo .env con:
# EMISOR_CODIGO="tu_codigo_emisor"
# EMISOR_CLAVE="tu_clave_emisor_o_llave_api"

def ejemplo_uso_consulta_receptor(nit_consulta):
    try:
        # Inicializar el cliente (tomará credenciales del .env)
        cliente = ReceptorApiClient()

        # NIT a consultar (ejemplo)
        
        nit_a_consultar = nit_consulta  # O "CF"
        
        print(f"Consultando NIT: {nit_a_consultar}...")
        
        # Realizar la consulta
        resultado = cliente.consultar_nit(nit_a_consultar)
        
        # Imprimir resultado
        print("Resultado de la Consulta:")
        print(resultado)

    except ValueError as e:
        print(f"Error de Configuración: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def consulta_receptor(nit_consulta):
    try:
        log_system_event(
            f'EVALUACION DE NIT DEL RECEPTOR: {nit_consulta}',
            'INFO',
            'scripts.INFILE.consulta_nit.consulta_receptor',
            'Facturas'
        )
        # Inicializar el cliente (tomará credenciales del .env)
        cliente = ReceptorApiClient()

        # NIT a consultar (ejemplo)
        
        nit_a_consultar = nit_consulta  # O "CF"
        
        print(f"Consultando NIT: {nit_a_consultar}...")
        
        # Realizar la consulta
        resultado = cliente.consultar_nit(nit_a_consultar)
        
        # Imprimir resultado
        print("Resultado de la Consulta:")
        print(resultado)
        
        mensaje_resultado = resultado.get('mensaje','')

        if mensaje_resultado == 'NIT no válido':
            log_system_event(
                f'EVALUACION DE NIT NO VALIDO DEL RECEPTOR: {nit_consulta}',
                'WARNING',
                'scripts.INFILE.consulta_nit.consulta_receptor',
                'Facturas'
            )
            return False
        
        return True

    except ValueError as e:
        print(f"Error de Configuración: {e}")
        log_system_event(
            f'EVALUACION DE NIT NO VALIDO DEL RECEPTOR: {nit_consulta}',
            'ERROR',
            'scripts.INFILE.consulta_nit.consulta_receptor',
            'Facturas',
            e
        )

        return False
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        log_system_event(
            f'EVALUACION DE NIT NO VALIDO DEL RECEPTOR: {nit_consulta}',
            'ERROR',
            'scripts.INFILE.consulta_nit.consulta_receptor',
            'Facturas',
            e
        )
        return False
# Ejecutar el ejemplo
# ejemplo_uso_consulta_receptor()