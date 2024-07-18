class Hipoteca {
    constructor(noEscritura = "", notario = "", finca = "", folio = "", libro = "", area = "", ubicacion = "", descripcion = "", valor_comercial = 0, titular = "", estatus = "", noContratoArrendamiento = "", avaluoBien = "", docDigitalSoporte = "") {
        this.noEscritura = noEscritura;
        this.notario = notario;
        this.finca = finca;
        this.folio = folio;
        this.libro = libro;
        this.area = area;
        this.ubicacion = ubicacion;
        this.descripcion = descripcion;
        this.valor_comercial = valor_comercial;
        this.titular = titular;
        this.estatus = estatus;
        this.noContratoArrendamiento = noContratoArrendamiento;
        this.avaluoBien = avaluoBien;
        this.docDigitalSoporte = docDigitalSoporte;
    }

    toJson() {
        const js = {
            Nombre: 'HIPOTECA',
            NoEscritura: this.noEscritura,
            Notario: this.notario,
            Finca: this.finca,
            Folio: this.folio,
            Libro: this.libro,
            Area: this.area,
            Ubicación: this.ubicacion,
            Descripción: this.descripcion,
            Valor_Comercial: this.valor_comercial,
            Titular: this.titular,
            Estatus: this.estatus,
            NoContrato_de_Arrendamiento: this.noContratoArrendamiento,
            Avaluo_del_Bien: this.avaluoBien,
            Documento_Digital_de_Soporte: this.docDigitalSoporte
        };
        return JSON.stringify(js, null, 4);
    }

    toString() {
        return `Hipoteca\nNo.Escritura: ${this.noEscritura}`;
    }
}

class DerechoDePosesionHipoteca {
    constructor(noEscritura = "", notario = "", area = "", ubicacion = "", descripcion = "", valor_comercial = 0, titular = "", estatus = "", noContratoArrendamiento = "", avaluoBien = "", docDigitalSoporte = "") {
        this.noEscritura = noEscritura;
        this.notario = notario;
        this.area = area;
        this.ubicacion = ubicacion;
        this.descripcion = descripcion;
        this.valor_comercial = valor_comercial;
        this.titular = titular;
        this.estatus = estatus;
        this.noContratoArrendamiento = noContratoArrendamiento;
        this.avaluoBien = avaluoBien;
        this.docDigitalSoporte = docDigitalSoporte;
    }

    toJson() {
        const js = {
            Nombre: 'DERECHO DE POSESIÓN HIPOTECA',
            NoEscritura: this.noEscritura,
            Notario: this.notario,
            Area: this.area,
            Ubicacion: this.ubicacion,
            Descripcion: this.descripcion,
            Valor_Comercial: this.valor_comercial,
            Titular: this.titular,
            Estatus: this.estatus,
            NoContrato_de_Arrendamiento: this.noContratoArrendamiento,
            Avaluo_del_Bien: this.avaluoBien,
            Documento_Digital_de_Soporte: this.docDigitalSoporte
        };
        return JSON.stringify(js, null, 4);
    }
}

class Fiador {
    constructor(codigo_cliente = "", nombre = "", lugar_trabajo = "", ingresos = 0, numeroTelefono = "", fotografia = "") {
        this.codigo_cliente = codigo_cliente;
        this.nombre = nombre;
        this.lugar_trabajo = lugar_trabajo;
        this.ingresos = ingresos;
        this.numeroTelefono = numeroTelefono;
        this.fotografia = fotografia;
    }

    toJson() {
        const js = {
            Nombre: 'FIADOR',
            Codigo_de_Cliente: this.codigo_cliente,
            Nombre: this.nombre,
            Lugar_de_Trabajo: this.lugar_trabajo,
            Ingresos: this.ingresos,
            Numero_de_Telefono: this.numeroTelefono,
            Fotografia: this.fotografia
        };
        return JSON.stringify(js, null, 4);
    }
}

class Cheque {
    constructor(noCheque = "", nombreCuenta = "", banco = "", cheque_girado_a = "", monto_cheque = 0, fotografia_cheque = "") {
        this.noCheque = noCheque;
        this.nombreCuenta = nombreCuenta;
        this.banco = banco;
        this.cheque_girado_a = cheque_girado_a;
        this.monto_cheque = monto_cheque;
        this.fotografia_cheque = fotografia_cheque;
    }

    toJson() {
        const js = {
            Nombre: 'CHEQUE',
            noCheque: this.noCheque,
            NombreCuenta: this.nombreCuenta,
            Banco: this.banco,
            Cheque_girado_a: this.cheque_girado_a,
            Monto_cheque: this.monto_cheque,
            Fotografia_Cheque: this.fotografia_cheque
        };
        return JSON.stringify(js, null, 4);
    }
}

class Vehiculo {
    constructor(placa = "", marca = "", color = "", noChasis = "", noMotor = "", valor_comercial = 0, fotografias = [], tarjetaCirculacion = "", titulo = "", noPoliza = "", montoSeguro = 0, noContratoArrendamiento = "") {
        this.placa = placa;
        this.marca = marca;
        this.color = color;
        this.noChasis = noChasis;
        this.noMotor = noMotor;
        this.valor_comercial = valor_comercial;
        this.fotografias = fotografias;
        this.tarjetaCirculacion = tarjetaCirculacion;
        this.titulo = titulo;
        this.noPoliza = noPoliza;
        this.montoSeguro = montoSeguro;
        this.noContratoArrendamiento = noContratoArrendamiento;
    }

    toJson() {
        const js = {
            Nombre: 'VEHICULO',
            Placa: this.placa,
            Marca: this.marca,
            Color: this.color,
            NoChasis: this.noChasis,
            NoMotor: this.noMotor,
            Valor_Comercial: this.valor_comercial,
            Fotografias: this.fotografias,
            TarjetaCirculacion: this.tarjetaCirculacion,
            Titulo: this.titulo,
            NoPoliza: this.noPoliza,
            MontoSeguro: this.montoSeguro,
            NoContratoArrendamiento: this.noContratoArrendamiento
        };
        return JSON.stringify(js, null, 4);
    }
}

class Mobiliaria {
    constructor(descripcionBien = "", documentoAcredita = "", imagenDocumentoAcredita = "", fotografiaBien = "", noPoliza = "", montoSeguro = 0) {
        this.descripcionBien = descripcionBien;
        this.documentoAcredita = documentoAcredita;
        this.imagenDocumentoAcredita = imagenDocumentoAcredita;
        this.fotografiaBien = fotografiaBien;
        this.noPoliza = noPoliza;
        this.montoSeguro = montoSeguro;
    }

    toJson() {
        const js = {
            Nombre: 'MOBILIARIA',
            DescripcionBien: this.descripcionBien,
            DocumentoAcredita: this.documentoAcredita,
            ImagenDocumentoAcredita: this.imagenDocumentoAcredita,
            FotografiaBien: this.fotografiaBien,
            NoPoliza: this.noPoliza,
            MontoSeguro: this.montoSeguro
        };
        return JSON.stringify(js, null, 4);
    }
}
