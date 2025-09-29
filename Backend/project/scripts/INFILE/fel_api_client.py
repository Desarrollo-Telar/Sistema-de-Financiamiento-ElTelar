import os
import requests
import uuid
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class FELApiClient:
    BASE_URL = "https://certificador.feel.com.gt/fel/procesounificado/transaccion/v2/xml"

    def __init__(self):
        """
        Inicializa el cliente con las credenciales cargadas desde el archivo .env
        """
        self.usuario_firma = os.getenv("USUARIO_FIRMA")
        self.llave_firma = os.getenv("LLAVE_FIRMA")
        self.usuario_api = os.getenv("USUARIO_API")
        self.llave_api = os.getenv("LLAVE_API")

        # Validación básica
        if not all([self.usuario_firma, self.llave_firma, self.usuario_api, self.llave_api]):
            raise ValueError("Faltan variables de entorno para la configuración de la API FEL")

    def _generar_identificador(self):
        """Genera un identificador único para la transacción."""
        return str(uuid.uuid4())

    def _crear_headers(self):
        """Crea los headers requeridos por la API FEL."""
        return {
            "Content-Type": "application/xml",
            "UsuarioFirma": self.usuario_firma,
            "LlaveFirma": self.llave_firma,
            "UsuarioApi": self.usuario_api,
            "LlaveApi": self.llave_api,
            "identificador": self._generar_identificador()
        }

    def enviar_xml(self, xml_content: str):
        """
        Envía el contenido XML directamente a la API FEL.
        """
        try:
            headers = self._crear_headers()

            response = requests.post(
                self.BASE_URL,
                headers=headers,
                data=xml_content.encode("utf-8")
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "status": "error",
                    "http_code": response.status_code,
                    "response": response.text
                }

        except Exception as e:
            return {"status": "exception", "message": str(e)}
