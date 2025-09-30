import os
import requests
import uuid
from dotenv import load_dotenv

# modelo
from apps.financings.models import Invoice

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

    def enviar_xml(self, xml_content: str, recibo_instance):
        """
        Envía el contenido XML directamente a la API FEL y guarda
        el registro en Invoice si la certificación es exitosa.
        """
        try:
            headers = self._crear_headers()

            response = requests.post(
                self.BASE_URL,
                headers=headers,
                data=xml_content.encode("utf-8")
            )
            
            # Intentar decodificar la respuesta JSON
            try:
                result_data = response.json()
            except requests.exceptions.JSONDecodeError:
                # Si no es JSON (por ej., un error XML directo o HTML), manejarlo como error genérico
                return {
                    "status": "error",
                    "http_code": response.status_code,
                    "response": response.text
                }


            if response.status_code == 200 and result_data.get('resultado') is True:
                # La certificación fue exitosa: ¡Guardar en la entidad Invoice!
                
                # Campos a guardar, extraídos de la respuesta de la API:                
                serie = result_data.get('serie') # Lo usarás para serie_autorizacion
                uuid_autorizacion = result_data.get('uuid') # Lo usarás para numero_autorizacion
                xml_certificado = result_data.get('xml_certificado') # Lo usarás para xml_certificado

                # Asumo que el modelo Recibo (recibo_instance) ya tiene los datos del receptor
                # que necesitas para NIT, Nombre y Correo, si no, deberás extraerlos del XML original
                # o del recibo. Para este ejemplo, usaré datos del 'recibo_instance'.
                
                # 📌 Importante: Asegúrate de que tu modelo 'Recibo' tenga los campos:
                # nit_receptor, nombre_receptor, correo_receptor, etc.
                
                factura, created = Invoice.objects.get_or_create(recibo_id= recibo_instance)

                factura.numero_autorizacion = uuid_autorizacion
                factura.serie_autorizacion = serie
                factura.xml_certificado = xml_certificado
                factura.nit_receptor = recibo_instance.cliente.number_nit
                factura.save()

                # Retornar la respuesta exitosa
                return result_data
                
            else:
                # La API devolvió un código 200 pero resultado=False, o un código diferente a 200
                return {
                    "status": "error",
                    "http_code": response.status_code,
                    "response_data": result_data # Retorna los datos de error si existen
                }

        except Exception as e:
            # Error de red, conexión, o cualquier otra excepción no controlada
            return {"status": "exception", "message": str(e)}
