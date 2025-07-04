# CLASE DE CLIENTES
from datetime import datetime

class Customer:
    contador = 0
    def __init__(self, nombre, apellido, correo_electronico, tipo_identificacion, numero_identificacion, 
                 numero_nit, numero_telefono, condicion_migratoria, status, genero, profesion, nacionalidad, 
                 lugar_nacimiento, fecha_nacimiento, estado_civil, tipo_persona, obeservacion=None, 
                 fecha_registro=None, codigo_cliente=None):
        Customer.contador+=1
        self._nombre = nombre
        self._apellido = apellido
        self._correo_electronico = correo_electronico
        self._tipo_identificacion = tipo_identificacion
        self._numero_identificacion = numero_identificacion
        self._numero_nit = numero_nit
        self._numero_telefono = numero_telefono
        self._condicion_migratoria = condicion_migratoria
        self._status = status
        self._genero = genero
        self._profesion = profesion
        self._nacionalidad = nacionalidad
        self._lugar_nacimiento = lugar_nacimiento
        self._fecha_nacimiento = fecha_nacimiento
        self._estado_civil = estado_civil
        self._tipo_persona = tipo_persona
        self._obeservacion = obeservacion
        self._fecha_registro = fecha_registro if fecha_registro else datetime.now()
        self._codigo_cliente = codigo_cliente if codigo_cliente else self.generar_codigo_cliente(Customer.contador)
        self._contador_id = Customer.contador
    
    
    
    def generar_codigo_cliente(self, contador):
        status_suffix = {
            'Posible Cliente': 'S',
            'No Aprobado': 'N',
            'Aprobado': '',
            'Revisión de documentos': 'D',
            'Dar de Baja': 'E',
        }
        suffix = status_suffix.get(self._status, '')
        current_date = datetime.now()
        current_year = current_date.year
        return f'{current_year}-{suffix}{contador}'

    # Getters
    @property
    def nombre(self):
        return self._nombre

    @property
    def apellido(self):
        return self._apellido

    @property
    def correo_electronico(self):
        return self._correo_electronico

    # Setters
    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    @apellido.setter
    def apellido(self, value):
        self._apellido = value

    @correo_electronico.setter
    def correo_electronico(self, value):
        self._correo_electronico = value

    # Añadir getters y setters para los demás atributos de la misma forma
    @property
    def tipo_identificacion(self):
        return self._tipo_identificacion

    @tipo_identificacion.setter
    def tipo_identificacion(self, value):
        self._tipo_identificacion = value

    @property
    def numero_identificacion(self):
        return self._numero_identificacion

    @numero_identificacion.setter
    def numero_identificacion(self, value):
        self._numero_identificacion = value

    @property
    def numero_nit(self):
        return self._numero_nit

    @numero_nit.setter
    def numero_nit(self, value):
        self._numero_nit = value

    @property
    def numero_telefono(self):
        return self._numero_telefono

    @numero_telefono.setter
    def numero_telefono(self, value):
        self._numero_telefono = value

    @property
    def condicion_migratoria(self):
        return self._condicion_migratoria

    @condicion_migratoria.setter
    def condicion_migratoria(self, value):
        self._condicion_migratoria = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def genero(self):
        return self._genero

    @genero.setter
    def genero(self, value):
        self._genero = value

    @property
    def profesion(self):
        return self._profesion

    @profesion.setter
    def profesion(self, value):
        self._profesion = value

    @property
    def nacionalidad(self):
        return self._nacionalidad

    @nacionalidad.setter
    def nacionalidad(self, value):
        self._nacionalidad = value

    @property
    def lugar_nacimiento(self):
        return self._lugar_nacimiento

    @lugar_nacimiento.setter
    def lugar_nacimiento(self, value):
        self._lugar_nacimiento = value

    @property
    def fecha_nacimiento(self):
        return self._fecha_nacimiento

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, value):
        self._fecha_nacimiento = value

    @property
    def estado_civil(self):
        return self._estado_civil

    @estado_civil.setter
    def estado_civil(self, value):
        self._estado_civil = value

    @property
    def tipo_persona(self):
        return self._tipo_persona

    @tipo_persona.setter
    def tipo_persona(self, value):
        self._tipo_persona = value

    @property
    def obeservacion(self):
        return self._obeservacion

    @obeservacion.setter
    def obeservacion(self, value):
        self._obeservacion = value

    @property
    def fecha_registro(self):
        return self._fecha_registro

    @fecha_registro.setter
    def fecha_registro(self, value):
        self._fecha_registro = value

    @property
    def codigo_cliente(self):
        return self._codigo_cliente

    @codigo_cliente.setter
    def codigo_cliente(self, value):
        self._codigo_cliente = value
    
    def __str__(self):        
        return f'Cliente: Contador:{self._contador_id}, codigo_cliente:{self._codigo_cliente}'

if __name__ == '__main__':
    
    fiador = Customer('Juan','Lopez','lopez@gmail.com','DPI','323846682','1106369','42256694','RESIDENTE','Aprobado','MASCULINO','AGRONOMO','GUATEMALTECA','COBAN','14-03-1995','SOLTERO','Indivicual (PI)')
    print(fiador)