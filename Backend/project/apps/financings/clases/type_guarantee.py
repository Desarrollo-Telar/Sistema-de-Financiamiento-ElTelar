import json

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
    
    def toJson(self):
        js = {
            'Nombre':'HIPOTECA',
            'No.Escritura':self.noEscritura,
            'Notario':self.notario,
            'Finca':self.finca,
            'Folio':self.folio,
            'Libro':self.libro,
            'Area':self.area,
            'Ubicación':self.ubicacion,
            'Descripción':self.descripcion,
            'Valor Comercial':self.valor_comercial,
            'Titular':self.titular,
            'Estatus':self.estatus,
            'No.Contrato de Arrendamiento':self.noContratoArrendamiento,
            'Avaluo del Bien':self.avaluoBien,
            'Documento Digital de Soporte':self.docDigitalSoporte
        }
        return json.dumps(js, indent=4, ensure_ascii=False)
    
    def __str__(self):
        return f'Hipoteca\nNo.Escritura: {self.noEscritura}'

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
    
    def toJson(self):
        js = {
            'Nombre':'DERECHO DE POSESIÓN HIPOTECA',
            'No.Escritura':self.noEscritura,
            'Notario':self.notario,           
            'Area':self.area,
            'Ubicacion':self.ubicacion,
            'Descripcion':self.descripcion,
            'Valor_Comercial':self.valor_comercial,
            'Titular':self.titular,
            'Estatus':self.estatus,
            'No.Contrato_de_Arrendamiento':self.noContratoArrendamiento,
            'Avaluo_del_Bien':self.avaluoBien,
            'Documento_Digital_de_Soporte':self.docDigitalSoporte
        }
        return json.dumps(js, indent=4, ensure_ascii=False)

class Fiador:
    def __init__(self, codigo_cliente="", nombre="", lugar_trabajo="", ingresos=0, numeroTelefono="", fotografia=""):
        self.codigo_cliente = codigo_cliente
        self.nombre = nombre
        self.lugar_trabajo = lugar_trabajo
        self.ingresos = ingresos
        self.numeroTelefono = numeroTelefono
        self.fotografia = fotografia

    def toJson(self):
        js = {
            'Nombre':'FIADOR',
            'Codigo_de_Cliente':self.codigo_cliente,
            'Nombre':self.nombre,           
            'Lugar de Trabajo':self.lugar_trabajo,
            'Ingresos':self.ingresos,
            'Numero de Telefono':self.descripcion,
            'Valor Comercial':self.valor_comercial,
            'Titular':self.titular,
            'Estatus':self.estatus,
            'No.Contrato de Arrendamiento':self.noContratoArrendamiento,
            'Avaluo del Bien':self.avaluoBien,
            'Documento Digital de Soporte':self.docDigitalSoporte
        }
        return json.dumps(js, indent=4, ensure_ascii=False)

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

if __name__ == '__main__':
    garantia = Hipoteca()
    print(garantia.toJson())