export class Hipoteca {
    constructor(noEscritura = "", notario = "", finca = "", folio = "", libro = "", area = "", ubicacion = "", descripcion = "", valor_comercial = 0, titular = "", estatus = "", noContratoArrendamiento = "", avaluoBien = "", docDigitalSoporte = "") {
        this._noEscritura = noEscritura;
        this._notario = notario;
        this._finca = finca;
        this._folio = folio;
        this._libro = libro;
        this._area = area;
        this._ubicacion = ubicacion;
        this._descripcion = descripcion;
        this._valor_comercial = parseFloat(valor_comercial);
        this._titular = titular;
        this._estatus = estatus;
        this._noContratoArrendamiento = noContratoArrendamiento;
        this._avaluoBien = avaluoBien;
        this._docDigitalSoporte = docDigitalSoporte;
    }

    get noEscritura() {
        return this._noEscritura;
    }
    set noEscritura(value) {
        
        this._noEscritura = value.trim();
    }

    get notario() {
        return this._notario;
    }
    set notario(value) {
        
        this._notario = value.trim();
    }

    get finca() {
        return this._finca;
    }
    set finca(value) {
        
        this._finca = value.trim();
    }

    get folio() {
        return this._folio;
    }
    set folio(value) {
        
        this._folio = value.trim();
    }

    get libro() {
        return this._libro;
    }
    set libro(value) {
        
        this._libro = value.trim();
    }

    get area() {
        return this._area;
    }
    set area(value) {
        
        this._area = value.trim();
    }

    get ubicacion() {
        return this._ubicacion;
    }
    set ubicacion(value) {
        
        this._ubicacion = value.trim();
    }

    get descripcion() {
        return this._descripcion;
    }
    set descripcion(value) {

        this._descripcion = value.trim();
    }

    get valor_comercial() {
        return this._valor_comercial;
    }
    set valor_comercial(value) {
       
        this._valor_comercial = parseFloat(value.trim());
    }

    get titular() {
        return this._titular;
    }
    set titular(value) {
        
        this._titular = value.trim();
    }

    get estatus() {
        return this._estatus;
    }
    set estatus(value) {
        
        this._estatus = value.trim();
    }

    get noContratoArrendamiento() {
        
        return this._noContratoArrendamiento;
    }
    set noContratoArrendamiento(value) {
        
        this._noContratoArrendamiento = value.trim();
    }

    get avaluoBien() {
        return this._avaluoBien;
    }
    set avaluoBien(value) {
        this._avaluoBien = value;
    }

    get docDigitalSoporte() {
        return this._docDigitalSoporte;
    }
    set docDigitalSoporte(value) {
        this._docDigitalSoporte = value;
    }

    toJSON() {
        return {            
            noEscritura: this._noEscritura,
            notario: this._notario,
            finca: this._finca,
            folio: this._folio,
            libro: this._libro,
            area: this._area,
            ubicacion: this._ubicacion,
            descripcion: this._descripcion,
            valor_comercial: this._valor_comercial,
            titular: this._titular,
            estatus: this._estatus,
            noContratoArrendamiento: this._noContratoArrendamiento,
            avaluoBien: this._avaluoBien,
            docDigitalSoporte: this._docDigitalSoporte
        };
    }
}

export class DerechoDePosesionHipoteca {
    constructor(noEscritura = "", notario = "", area = "", ubicacion = "", descripcion = "", valor_comercial = 0, titular = "", estatus = "", noContratoArrendamiento = "", avaluoBien = "", docDigitalSoporte = "") {
        this._noEscritura = noEscritura;
        this._notario = notario;
        this._area = area;
        this._ubicacion = ubicacion;
        this._descripcion = descripcion;
        this._valor_comercial = valor_comercial;
        this._titular = titular;
        this._estatus = estatus;
        this._noContratoArrendamiento = noContratoArrendamiento;
        this._avaluoBien = avaluoBien;
        this._docDigitalSoporte = docDigitalSoporte;
    }

    get noEscritura() {
        return this._noEscritura;
    }
    set noEscritura(value) {
        this._noEscritura = value;
    }

    get notario() {
        return this._notario;
    }
    set notario(value) {
        this._notario = value;
    }

    get area() {
        return this._area;
    }
    set area(value) {
        this._area = value;
    }

    get ubicacion() {
        return this._ubicacion;
    }
    set ubicacion(value) {
        this._ubicacion = value;
    }

    get descripcion() {
        return this._descripcion;
    }
    set descripcion(value) {
        this._descripcion = value;
    }

    get valor_comercial() {
        return this._valor_comercial;
    }
    set valor_comercial(value) {
        this._valor_comercial = parseFloat(value);
    }

    get titular() {
        return this._titular;
    }
    set titular(value) {
        this._titular = value;
    }

    get estatus() {
        return this._estatus;
    }
    set estatus(value) {
        this._estatus = value;
    }

    get noContratoArrendamiento() {
        return this._noContratoArrendamiento;
    }
    set noContratoArrendamiento(value) {
        this._noContratoArrendamiento = value;
    }

    get avaluoBien() {
        return this._avaluoBien;
    }
    set avaluoBien(value) {
        this._avaluoBien = value;
    }

    get docDigitalSoporte() {
        return this._docDigitalSoporte;
    }
    set docDigitalSoporte(value) {
        this._docDigitalSoporte = value;
    }

    toJSON() {
        return {
            Nombre: 'DERECHO DE POSESIÓN HIPOTECA',
            NoEscritura: this._noEscritura,
            Notario: this._notario,
            Area: this._area,
            Ubicacion: this._ubicacion,
            Descripcion: this._descripcion,
            Valor_Comercial: this._valor_comercial,
            Titular: this._titular,
            Estatus: this._estatus,
            NoContrato_de_Arrendamiento: this._noContratoArrendamiento,
            Avaluo_del_Bien: this._avaluoBien,
            Documento_Digital_de_Soporte: this._docDigitalSoporte
        };
    }
}
export class Fiador {
    constructor(codigo_cliente = "", nombre = "", lugar_trabajo = "", ingresos = 0, numeroTelefono = "", fotografia = "") {
        this._codigo_cliente = codigo_cliente;
        this._nombre = nombre;
        this._lugar_trabajo = lugar_trabajo;
        this._ingresos = ingresos;
        this._numeroTelefono = numeroTelefono;
        this._fotografia = fotografia;
    }

    get codigo_cliente() {
        return this._codigo_cliente;
    }
    set codigo_cliente(value) {
        this._codigo_cliente = value;
    }

    get nombre() {
        return this._nombre;
    }
    set nombre(value) {
        this._nombre = value;
    }

    get lugar_trabajo() {
        return this._lugar_trabajo;
    }
    set lugar_trabajo(value) {
        this._lugar_trabajo = value;
    }

    get ingresos() {
        return this._ingresos;
    }
    set ingresos(value) {
        this._ingresos = parseFloat(value);
    }

    get numeroTelefono() {
        return this._numeroTelefono;
    }
    set numeroTelefono(value) {
        this._numeroTelefono = value;
    }

    get fotografia() {
        return this._fotografia;
    }
    set fotografia(value) {
        this._fotografia = value;
    }

    toJSON() {
        return {            
            Codigo_de_Cliente: this._codigo_cliente,
            Nombre: this._nombre,
            Lugar_de_Trabajo: this._lugar_trabajo,
            Ingresos: this._ingresos,
            Numero_de_Telefono: this._numeroTelefono,
            Fotografia: this._fotografia
        };
    }
}
export class Cheque {
    constructor(noCheque = "", nombreCuenta = "", banco = "", cheque_girado_a = "", monto_cheque = 0, fotografia_cheque = "") {
        this._noCheque = noCheque;
        this._nombreCuenta = nombreCuenta;
        this._banco = banco;
        this._cheque_girado_a = cheque_girado_a;
        this._monto_cheque = monto_cheque;
        this._fotografia_cheque = fotografia_cheque;
    }

    get noCheque() {
        return this._noCheque;
    }
    set noCheque(value) {
        this._noCheque = value;
    }

    get nombreCuenta() {
        return this._nombreCuenta;
    }
    set nombreCuenta(value) {
        this._nombreCuenta = value;
    }

    get banco() {
        return this._banco;
    }
    set banco(value) {
        this._banco = value;
    }

    get cheque_girado_a() {
        return this._cheque_girado_a;
    }
    set cheque_girado_a(value) {
        this._cheque_girado_a = value;
    }

    get monto_cheque() {
        return this._monto_cheque;
    }
    set monto_cheque(value) {
        this._monto_cheque = parseFloat(value);
    }

    get fotografia_cheque() {
        return this._fotografia_cheque;
    }
    set fotografia_cheque(value) {
        this._fotografia_cheque = value;
    }

    toJSON() {
        return {
            noCheque: this._noCheque,
            NombreCuenta: this._nombreCuenta,
            Banco: this._banco,
            Cheque_girado_a: this._cheque_girado_a,
            Monto_cheque: this._monto_cheque,
            Fotografia_Cheque: this._fotografia_cheque
        };
    }
}
export class Vehiculo {
    constructor(placa = "", marca = "", color = "", noChasis = "", noMotor = "", valor_comercial = 0, fotografias = [], tarjetaCirculacion = "", titulo = "", noPoliza = "", montoSeguro = 0, noContratoArrendamiento = "") {
        this._placa = placa;
        this._marca = marca;
        this._color = color;
        this._noChasis = noChasis;
        this._noMotor = noMotor;
        this._valor_comercial = valor_comercial;
        this._fotografias = fotografias;
        this._tarjetaCirculacion = tarjetaCirculacion;
        this._titulo = titulo;
        this._noPoliza = noPoliza;
        this._montoSeguro = montoSeguro;
        this._noContratoArrendamiento = noContratoArrendamiento;
    }

    get placa() {
        return this._placa;
    }
    set placa(value) {
        this._placa = value;
    }

    get marca() {
        return this._marca;
    }
    set marca(value) {
        this._marca = value;
    }

    get color() {
        return this._color;
    }
    set color(value) {
        this._color = value;
    }

    get noChasis() {
        return this._noChasis;
    }
    set noChasis(value) {
        this._noChasis = value;
    }

    get noMotor() {
        return this._noMotor;
    }
    set noMotor(value) {
        this._noMotor = value;
    }

    get valor_comercial() {
        return this._valor_comercial;
    }
    set valor_comercial(value) {
        this._valor_comercial = parseFloat(value);
    }

    get fotografias() {
        return this._fotografias;
    }
    set fotografias(value) {
        this._fotografias = value;
    }

    get tarjetaCirculacion() {
        return this._tarjetaCirculacion;
    }
    set tarjetaCirculacion(value) {
        this._tarjetaCirculacion = value;
    }

    get titulo() {
        return this._titulo;
    }
    set titulo(value) {
        this._titulo = value;
    }

    get noPoliza() {
        return this._noPoliza;
    }
    set noPoliza(value) {
        this._noPoliza = value;
    }

    get montoSeguro() {
        return this._montoSeguro;
    }
    set montoSeguro(value) {
        this._montoSeguro = parseFloat(value);
    }

    get noContratoArrendamiento() {
        return this._noContratoArrendamiento;
    }
    set noContratoArrendamiento(value) {
        this._noContratoArrendamiento = value;
    }

    toJSON() {
        return {            
            Placa: this._placa,
            Marca: this._marca,
            Color: this._color,
            NoChasis: this._noChasis,
            NoMotor: this._noMotor,
            Valor_Comercial: this._valor_comercial,
            Fotografias: this._fotografias,
            TarjetaCirculacion: this._tarjetaCirculacion,
            Titulo: this._titulo,
            NoPoliza: this._noPoliza,
            MontoSeguro: this._montoSeguro,
            NoContratoArrendamiento: this._noContratoArrendamiento
        };
    }
}
export class Mobiliaria {
    constructor(descripcionBien = "", documentoAcredita = "", imagenDocumentoAcredita = "", fotografiaBien = "", noPoliza = "", montoSeguro = 0) {
        this._descripcionBien = descripcionBien;
        this._documentoAcredita = documentoAcredita;
        this._imagenDocumentoAcredita = imagenDocumentoAcredita;
        this._fotografiaBien = fotografiaBien;
        this._noPoliza = noPoliza;
        this._montoSeguro = montoSeguro;
    }

    get descripcionBien() {
        return this._descripcionBien;
    }
    set descripcionBien(value) {
        this._descripcionBien = value;
    }

    get documentoAcredita() {
        return this._documentoAcredita;
    }
    set documentoAcredita(value) {
        this._documentoAcredita = value;
    }

    get imagenDocumentoAcredita() {
        return this._imagenDocumentoAcredita;
    }
    set imagenDocumentoAcredita(value) {
        this._imagenDocumentoAcredita = value;
    }

    get fotografiaBien() {
        return this._fotografiaBien;
    }
    set fotografiaBien(value) {
        this._fotografiaBien = value;
    }

    get noPoliza() {
        return this._noPoliza;
    }
    set noPoliza(value) {
        this._noPoliza = value;
    }

    get montoSeguro() {
        return this._montoSeguro;
    }
    set montoSeguro(value) {
        this._montoSeguro = parseFloat(value);
    }

    toJSON() {
        return {            
            DescripcionBien: this._descripcionBien,
            DocumentoAcredita: this._documentoAcredita,
            ImagenDocumentoAcredita: this._imagenDocumentoAcredita,
            FotografiaBien: this._fotografiaBien,
            NoPoliza: this._noPoliza,
            MontoSeguro: this._montoSeguro
        };
    }
}
