import json

# CLASE PARA LA SIMULACION DE REGISTRO DE GARANTIAS
class Guarantee:
    contador = 0
    def __init__(self, credit_id, detalle_garantia, descripcion=None):
        Guarantee.contador += 1
        self._count = Guarantee.contador
        
        self.__credit_id = credit_id
        self.__description = descripcion
        self.__detalle_garantia = [DetailGuarantee(**dg) for dg in detalle_garantia]
        self.__suma_total = self.calcular_suma_total()
        self.__guarantee = {}
    
    
    
    @property
    def credit_id(self):
        return self.__credit_id
    
    @credit_id.setter
    def credit_id(self, credit_id):
        self.__credit_id = credit_id
    
    @property
    def descripcion(self):
        return self.__description
    
    @descripcion.setter
    def descripcion(self, descripcion):
        self.__description = descripcion
    
    @property
    def suma_total(self):
        return self.__suma_total
    
    def calcular_suma_total(self):
        return sum(detalle.valor_cobertura for detalle in self.__detalle_garantia)
    
    def toJSON(self):
        self.__guarantee['id'] = self.id
        self.__guarantee['description'] = self.descripcion
        self.__guarantee['suma_total'] = self.suma_total
        return json.dumps(self.__guarantee, indent=4)

    def __str__(self):
        resultado = f'''
        Credito:[
            id:{self._count},
            descripcion:{self.descripcion},
            suma total: {self.suma_total}
        ]    
        '''
        return resultado

class DetailGuarantee:
    contador = 0

    def __init__(self,  tipo_garantia, valor_cobertura=0, **kwargs):
        DetailGuarantee.contador += 1
        
        self.__tipo_garantia = self.crear_tipo_de_garantia(tipo_garantia, **kwargs)
        self.__valor_cobertura = valor_cobertura

   

    @property
    def tipo_garantia(self):
        return self.__tipo_garantia

    @property
    def valor_cobertura(self):
        return self.__valor_cobertura

    def crear_tipo_de_garantia(self, tipo_garantia, **kwargs):
        if tipo_garantia == 'Hipoteca':
            return Hipoteca(**kwargs)
        elif tipo_garantia == 'Derecho de posesión':
            return DerechoDePosesionHipoteca(**kwargs)
        elif tipo_garantia == 'Fiador':
            return Fiador(**kwargs)
        elif tipo_garantia == 'Cheque':
            return Cheque(**kwargs)
        elif tipo_garantia == 'Vehiculo':
            return Vehiculo(**kwargs)
        elif tipo_garantia == 'Mobiliaria':
            return Mobiliaria(**kwargs)
        else:
            raise ValueError(f"Tipo de garantía desconocido: {tipo_garantia}")

class Hipoteca:
    def __init__(self, noEscritura="", notario="", finca="", folio="", libro="", area="", ubicacion="", descripcion="", valor_comercial=0, titular="", estatus="", noContratoArrendamiento="", avaluoBien="", docDigitalSoporte=""):
        self.noEscritura = noEscritura
        self.notario = notario
        self.finca = finca
        self.folio = folio
        self.libro = libro
        self.area = area
        self.ubicacion = ubicacion
        self.descripcion = descripcion
        self.valor_comercial = valor_comercial
        self.titular = titular
        self.estatus = estatus
        self.noContratoArrendamiento = noContratoArrendamiento
        self.avaluoBien = avaluoBien
        self.docDigitalSoporte = docDigitalSoporte

class DerechoDePosesionHipoteca:
    def __init__(self, noEscritura="", notario="", area="", ubicacion="", descripcion="", valor_comercial=0, titular="", estatus="", noContratoArrendamiento="", avaluoBien="", docDigitalSoporte=""):
        self.noEscritura = noEscritura
        self.notario = notario
        self.area = area
        self.ubicacion = ubicacion
        self.descripcion = descripcion
        self.valor_comercial = valor_comercial
        self.titular = titular
        self.estatus = estatus
        self.noContratoArrendamiento = noContratoArrendamiento
        self.avaluoBien = avaluoBien
        self.docDigitalSoporte = docDigitalSoporte

class Fiador:
    def __init__(self, codigo_cliente="", nombre="", lugar_trabajo="", ingresos=0, numeroTelefono="", fotografia=""):
        self.codigo_cliente = codigo_cliente
        self.nombre = nombre
        self.lugar_trabajo = lugar_trabajo
        self.ingresos = ingresos
        self.numeroTelefono = numeroTelefono
        self.fotografia = fotografia

class Cheque:
    def __init__(self, noCheque="", nombreCuenta="", banco="", cheque_girado_a="", monto_cheque=0, fotografia_cheque=""):
        self.noCheque = noCheque
        self.nombreCuenta = nombreCuenta
        self.banco = banco
        self.cheque_girado_a = cheque_girado_a
        self.monto_cheque = monto_cheque
        self.fotografia_cheque = fotografia_cheque

class Vehiculo:
    def __init__(self, placa="", marca="", color="", noChasis="", noMotor="", valor_comercial=0, fotografias=None, tarjetaCirculacion="", titulo="", noPoliza="", montoSeguro=0, noContratoArrendamiento=""):
        if fotografias is None:
            fotografias = []
        self.placa = placa
        self.marca = marca
        self.color = color
        self.noChasis = noChasis
        self.noMotor = noMotor
        self.valor_comercial = valor_comercial
        self.fotografias = fotografias
        self.tarjetaCirculacion = tarjetaCirculacion
        self.titulo = titulo
        self.noPoliza = noPoliza
        self.montoSeguro = montoSeguro
        self.noContratoArrendamiento = noContratoArrendamiento

class Mobiliaria:
    def __init__(self, descripcionBien="", documentoAcredita="", imagenDocumentoAcredita="", fotografiaBien="", noPoliza="", montoSeguro=0):
        self.descripcionBien = descripcionBien
        self.documentoAcredita = documentoAcredita
        self.imagenDocumentoAcredita = imagenDocumentoAcredita
        self.fotografiaBien = fotografiaBien
        self.noPoliza = noPoliza
        self.montoSeguro = montoSeguro

# Ejemplo de uso con los datos JSON proporcionados
json_data = '''
[{
    "id": 1,
    "credit_id": 1,
    "description": "",
    "Detalle Garantia": [{
        "id": 1,
        "tipo_garantia": "Hipoteca",
        "valor_cobertura": 750,
        "noEscritura": "12345",
        "notario": "Notario 1",
        "finca": "Finca 1",
        "folio": "Folio 1",
        "libro": "Libro 1",
        "area": "100m2",
        "ubicacion": "Ubicación 1",
        "descripcion": "Descripción 1",
        "valor_comercial": 100000,
        "titular": "Titular 1",
        "estatus": "Activo",
        "noContratoArrendamiento": "12345",
        "avaluoBien": "Avaluo 1",
        "docDigitalSoporte": "Doc 1"
    },
    {
        "id": 2,
        "tipo_garantia": "Derecho de posesión",
        "valor_cobertura": 750,
        "noEscritura": "54321",
        "notario": "Notario 2",
        "area": "200m2",
        "ubicacion": "Ubicación 2",
        "descripcion": "Descripción 2",
        "valor_comercial": 200000,
        "titular": "Titular 2",
        "estatus": "Activo",
        "noContratoArrendamiento": "54321",
        "avaluoBien": "Avaluo 2",
        "docDigitalSoporte": "Doc 2"
    }]
}]
'''

data = json.loads(json_data)
creditos = [Guarantee(
    id=item["id"],
    credit_id=item["credit_id"],
    descripcion=item["description"],
    detalle_garantia=item["Detalle Garantia"]
) for item in data]

# Ejemplo de acceso a los datos
for credito in creditos:
    print(f'Credito ID: {credito.id}, Suma Total: {credito.suma_total}')
    for detalle in credito._Guarantee__detalle_garantia:
        print(f'  Detalle Garantia ID: {detalle.id}, Valor Cobertura: {detalle.valor_cobertura}')
        print(f'    Tipo de Garantia: {type(detalle.tipo_garantia).__name__}')
detalle =  [
    DetailGuarantee(tipo_garantia='Hipoteca',valor_comercial=500,)
]
garantia = Guarantee(1,1,)