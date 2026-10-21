"""Generador de texto de reconocimiento de deuda.

Los atributos requeridos se documentan en la función texto().
Revisar las cláusulas con asesoría legal antes de usar el contrato.
"""
from datetime import date, datetime
from decimal import Decimal

from apps.customers.models import Customer

from apps.financings.clases.paymentplan import PaymentPlan
from apps.financings.clases.credit import Credit

from num2words import num2words

EMPRESA = 'INVERSIONES INTEGRALES EL TELAR, SOCIEDAD ANÓNIMA'
REPRESENTANTE = 'EDGAR ARMANDO ALVARADO BERMÚDEZ'


def campo(obj, nombre, defecto=''):
    """Lee un atributo de un objeto Django o una clave de un diccionario."""
    if obj is None:
        return defecto
    valor = obj.get(nombre, defecto) if isinstance(obj, dict) else getattr(obj, nombre, defecto)
    return defecto if valor is None else valor


def nombre(persona):
    completo = persona
    if completo:
        return str(completo).upper()
    partes = [campo(persona, x) for x in ('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido')]
    return ' '.join(str(x) for x in partes if x).upper() or '[NOMBRE PENDIENTE]'


from datetime import datetime

def fecha_es(fecha=None):
    if fecha is None:
        fecha = datetime.now()
    elif hasattr(fecha, 'date') and not isinstance(fecha, datetime):
        # Si pasan un objeto date en lugar de datetime, lo manejamos bien
        pass

    # Diccionarios de traducción
    dias_semana = {
        0: "lunes", 1: "martes", 2: "miércoles", 3: "jueves",
        4: "viernes", 5: "sábado", 6: "domingo"
    }
    
    meses = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }

    dias_map = {
        1: "uno", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco",
        6: "seis", 7: "siete", 8: "ocho", 9: "nueve", 10: "diez",
        11: "once", 12: "doce", 13: "trece", 14: "catorce", 15: "quince",
        16: "dieciséis", 17: "diecisiete", 18: "dieciocho", 19: "diecinueve", 20: "veinte",
        21: "veintiuno", 22: "veintidós", 23: "veintitrés", 24: "veinticuatro", 25: "veinticinco",
        26: "veintiséis", 27: "veintisiete", 28: "veintiocho", 29: "veintinueve", 30: "treinta",
        31: "treinta y uno"
    }

    def convertir_anio(anio):
        # Lógica general para años del siglo XXI (2000 a 2099)
        if 2000 <= anio < 2100:
            decena = anio % 100
            base = "dos mil"
            if decena == 0:
                return base
            elif decena < 10:
                unidades = ["", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"]
                return f"{base} {unidades[decena]}"
            elif 10 <= decena < 20:
                decenas_10 = {10: "diez", 11: "once", 12: "doce", 13: "trece", 14: "catorce", 15: "quince", 16: "dieciséis", 17: "diecisiete", 18: "dieciocho", 19: "diecinueve"}
                return f"{base} {decenas_10[decena]}"
            elif 20 <= decena < 30:
                decenas_20 = {20: "veinte", 21: "veintiuno", 22: "veintidós", 23: "veintitrés", 24: "veinticuatro", 25: "veinticinco", 26: "veintiséis", 27: "veintisiete", 28: "veintiocho", 29: "veintinueve"}
                return f"{base} {decenas_20[decena]}"
            else:
                d = decena // 10
                u = decena % 10
                dec_nombres = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
                uni_nombres = ["", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"]
                if u == 0:
                    return f"{base} {dec_nombres[d]}"
                else:
                    return f"{base} {dec_nombres[d]} y {uni_nombres[u]}"
        return str(anio)

    dia_sem = dias_semana[fecha.weekday()]
    dia_num = dias_map.get(fecha.day, str(fecha.day))
    mes_nombre = meses[fecha.month]
    anio_palabra = convertir_anio(fecha.year)

    return f"{dia_num} de {mes_nombre} de {anio_palabra}"


def dinero(monto):
    from apps.financings.formato import formatear_numero

    return formatear_numero(monto)


def ordinal(numero, mayuscula=True):
    nombres = {
        1: 'primera',
        2: 'segunda',
        3: 'tercera',
        4: 'cuarta',
        5: 'quinta',
        6: 'sexta',
        7: 'séptima',
        8: 'octava',
        9: 'novena',
        10: 'décima'
    }

    resultado = nombres.get(numero, f'número {numero}')

    return resultado.upper() if mayuscula else resultado

def ordinal_m(n, genero='m'):
    """
    Convierte un número entero en su respectivo ordinal en español.
    genero: 'f' para femenino (primera, segunda), 'm' para masculino (primero, segundo).
    """
    unidades_m = ["", "primer", "segundo", "tercero", "cuarto", "quinto", "sexto", "séptimo", "octavo", "noveno"]
    unidades_f = ["", "primera", "segunda", "tercera", "cuarta", "quinta", "sexta", "séptima", "octava", "novena"]
    
    decenas_m = ["", "décimo", "vigésimo", "trigésimo"]
    decenas_f = ["", "décima", "vigésima", "trigésima"]
    
    if n < 1:
        return str(n)
    
    if n <= 9:
        return unidades_f[n] if genero == 'f' else unidades_m[n]
        
    decena = n // 10
    unidad = n % 10
    
    if decena < len(decenas_m):
        d_str = decenas_f[decena] if genero == 'f' else decenas_m[decena]
        if unidad == 0:
            return d_str
        else:
            u_str = unidades_f[unidad] if genero == 'f' else unidades_m[unidad]
            return f"{d_str} {u_str}"
            
    # Si pasa de 39, regresa el número abreviado por seguridad
    return str(n) + ("ª" if genero == 'f' else "º")

def numero_en_letras(numero, mayuscula=True):
    resultado = num2words(numero,lang='es')

    return resultado.upper() if mayuscula else resultado

def datos_personales(persona):
    return (
        f"Yo, {nombre(persona)}, de {numero_en_letras(persona.get_edad(), False)} años de edad, "
        f"{persona.get_estado_civil().lower()}, "
        f"{persona.get_nacionalidad().lower()}, "
        f"{persona.profession_trade.lower()}, de este domicilio, "
        'me identifico con el Documento Personal de Identificación -DPI- '
        f"Código Único de Identificación número {persona.get_numero_identificacion_en_letras()}; "
        'extendido por el Registro Nacional de las Personas -RENAP-, de la República de Guatemala; '
    )


def plan_pagos(plan):
    """Sustituir por la función real de cálculo de cuotas del proyecto."""
    cliente = plan.customer_id
    
    gracia = plan.plazo_gracia if plan.plazo_gracia else 0
    dia = datetime.now().date()
    
    plazo = plan.plazo if plan.plazo else 1
    tasa_interes = plan.get_tasa()
    forma_pago = plan.forma_de_pago if plan.forma_de_pago else 'NIVELADA'
    fecha_inicio = plan.fecha_inicio if plan.fecha_inicio else dia
    credito = Credit('', plan.total_value_of_the_product_or_service, plazo, tasa_interes, forma_pago, 'MENSUAL', fecha_inicio.strftime('%Y-%m-%d'), 'CONSUMO', cliente, None,None,gracia)
    plan_pago = PaymentPlan(credito)
    
    cuotas = plan_pago.generar_plan()
    return cuotas


def texto(credito, garantias):
    """Construye cuatro secciones textuales sin leer PDF ni utilizar OCR.

    Campos esperados:
      credito: customer/deudor, plazo, monto, fecha_contrato, numero_cuenta_empresa,
               direccion_empresa, municipio_empresa, departamento_empresa,
               cuenta_desembolso, banco_desembolso, numero_acta, fecha_acta, pagos.
      deudor/fiador: nombre_completo (o primer_nombre, etc.), edad, estado_civil,
                     nacionalidad, profesion, dpi, direccion, zona, municipio,
                     departamento; fiador además entidad_laboral.
      garantia: tipo, descripcion, datos_registrales, propietario (opcional).
      pago: mes, cuota, fecha_pago.

    Los datos faltantes se marcan con [CORCHETES] para revisión.
    """
    fiadores_list = []
    sucursal =  credito.sucursal

    if credito.fiador:
        if isinstance(credito.fiador, list):
            for f_data in credito.fiador:
                f_obj = Customer.objects.filter(id=f_data.get('id')).first()
                if f_obj:
                    fiadores_list.append(f_obj)
                    
        elif isinstance(credito.fiador, dict):
            f_obj = Customer.objects.filter(id=credito.fiador.get('id')).first()

            if f_obj:
                fiadores_list.append(f_obj)
    
    garantias = list(garantias or [])
    deudor = campo(credito, 'customer_id')
    pagos = plan_pagos(credito)
    fecha = fecha_es()
    monto =  credito.total_value_of_the_product_or_service
    plazo = credito.plazo
    numero_cuenta = ''
    nombre_banco = ''
    acta = ''

    pagina_1 = [
        f'En la ciudad de Cobán del departamento de Alta Verapaz, a {fecha}. NOSOTROS: '
        f'por una parte {datos_personales(deudor)}'
    ]
    for fiador in fiadores_list:
        pagina_1.append(datos_personales(fiador))
    pagina_1.append(
        f'Yo, {REPRESENTANTE}, de cuarenta y un años de edad, '
        'soltero, guatemalteco, Ingeniero Civil, de este domicilio, me identifico '
        'con el Documento Personal de Identificación -DPI- Código Único de '
        'Identificación número un mil ochocientos treinta y siete espacio once mil '
        'ochocientos ochenta y dos espacio un mil seiscientos uno; extendido por '
        'el Registro Nacional de las Personas -RENAP-, de la República de Guatemala; '
        f'actúo en mi calidad de ADMINISTRADOR ÚNICO Y REPRESENTANTE LEGAL de {EMPRESA}, '
        'calidad que acredito con mi nombramiento, el cual está contenido en el acta notarial que contiene mi nombramiento, autorizada en la ciudad de Cobán Alta Verapaz, de fecha diecisiete de junio del año dos mil veinticuatro, por el Notario Adán Leal Natareno, la que se encuentra debidamente inscrita en el Registro Mercantil bajo el número SETECIENTOS CUARENTA Y SIETE MIL SEISCIENTOS CINCO (747605), '
        'folio SETECIENTOS NOVENTA Y SIETE (797), del libro OCHOCIENTOS TREINTA Y TRES (833), de Auxiliares de Comericio, según expediente número SETENTA Y TRES MIL CUARENTA GUION DOS MIL VEINTICUATRO (73040-2024), según expediente número SETENTA Y ' 
        f'TRES MIL CUARENTA GUION DOS MIL VEINTICUATRO (73040-2024), según inscripción de fecha veinticinco de junio del año dos mil veinticuatro; según documento emitido por el Registro Mercantil con número quinientos veintisiete mil cuatrocientos noventa y tres; documento en el que hago consta que la empresa denominada {EMPRESA}, se encuentra debidamente inscrita en el Registro Mercantil, bajo el número CIENTO SESENTA Y SEIS MIL CIENTO VEINTE (166120), folio OCHOCIENTOS CINCUENTA Y NUEVE (859), del libro '
        'consignadas, hallamos en el libre ejercicio de nuestros derechos civiles y que por el presente acto celebramos CONTRATO DE RECONOCIMIENTO DE DEUDA, conteniendo en las cláusulas siguentes: ' 
        
    )

    pagina_2 = [
        f'PRIMERA: Yo, {nombre(deudor)}, declaro que me reconozco LISA Y LLANA '
        f'DEUDORA de la entidad {EMPRESA}, por medio de su ADMINISTRADOR ÚNICO Y REPRESENTANTE LEGAL, representada por el señor {REPRESENTANTE}, '
        f'por la cantidad de  {numero_en_letras(monto)} QUETZALES (Q. {dinero(monto)}). '
        'El reconocimiento se regirá bajo las condiciones siguientes: '
        f'a) DE LA FORMA DE PAGO: El pago de la deuda será a través de {numero_en_letras(plazo)} '
        'ABONOS MENSUALES, distribuidos de la siguiente manera: '
    ]
    if pagos:
        for i, pago in enumerate(pagos, start=1):
            mes = ordinal_m(pago['mes'])
            cuota = dinero(pago['cuota'])
            fecha_pago = fecha_es(pago['fecha_final'])
            etiqueta = 'último' if i == len(pagos) else f' {mes}'
            pagina_2.append(f'El {etiqueta} pago será por Q. {cuota}; ')

        for i, pago in enumerate(pagos, start=1):
            mes = ordinal_m(pago['mes'])
            cuota = dinero(pago['cuota'])
            fecha_pago = fecha_es(pago['fecha_final'])
            etiqueta = 'último' if i == len(pagos) else f' {mes}'
            pagina_2.append(f'debiendo hacer el {etiqueta} el dia {fecha_pago}; ')
    else:
        pagina_2.append('[PLAN DE PAGOS PENDIENTE DE GENERAR]; ')

    pagina_2.append(
        'los pagos deberán efectuarse mediante depósito a la cuenta monetaria número '
        f'{sucursal.numero_de_cuenta_banco} del Banco {sucursal.nombre_banco} a nombre de {EMPRESA}, '
        f'ubicada en {sucursal.get_direccion()}, sin necesidad de requerimiento o cobro alguno; '
        f'b) Manifiesto yo, {nombre(deudor)}, que la cantidad que me fue otorgada por la entidad {EMPRESA}, la invertiré exclusivamente en:  '
        'tal y como conta en mi solicitud de crédito, por medio de transferencia bancaria'
        f'a la cuenta { numero_cuenta} del Banco '
        f'{nombre_banco}, a nombre de {nombre(deudor)}; '
        f'c) La falta de pago de la cantidad adeudada, dará derecho a {EMPRESA}, por medio de su ADMINISTRADOR ÚNICO Y REPRESENTANTE LEGRAL, representada por el señor {REPRESENTANTE}, '
        'a dar por vencido el plazo y al cobro de la cantidad adeudada, intereses y costas '
        'procesales y del presente documento debidamente legalizado por Notario en sus firmas servirá de titulo ejecutivo para iniciar el juicio correspondiente; y en esta forma se podra dar vencido el plazo si se le da al dinero mutuado, un destino diferente para el cual fue concedido, según la solicitud de crédito; y, resolucion emitida por  '
        f'de la entidad: {EMPRESA}, por medio de su ADMINISTRADOR ÚNICO Y REPRESENTANTE LEGAL, contenida en el Acta   , de fecha {fecha_es()}, mediante la cual fue autorizada el presente crédito; '
        f'd) Para los efectos legales, yo, {nombre(deudor)}, '
    )

    pagina_3 = [
        'renuncio al fuero de mi domicilio y me sujeto expresamente a los tribunales '
        'que la acreedora elija, señalando desde ya como lugar para recibir citaciones, '
        f'notificaciones y emplazamientos en la siguiente dirección: {deudor.get_direccion().street}, '
        f'zona {deudor.get_direccion().number}, '
        f'{deudor.get_direccion().state}, '
        f'{deudor.get_direccion().city}; '
        f'casa plenamente conocida, lugar donde resido actualmente; y acepto como buenas, exactas, de plazo vencido, líquidas y exigibles las cantidades que a consecuencia de este crédito se me presenten en caso de incumplimiento a cualquiera de las estipulaciones de este contrato, y si cambiará de dirección tengo la obligación de comunicarlo a la entidad {EMPRESA}, por medio de su ADMINISTRADOR ÚNICO Y REPRESENTANTE LEGAL, representada por el señor {REPRESENTANTE}, caso contrario las citaciones, notificaciones y emplazamientos se me harán en la dirección antes indicada y se tendrán como válidas;'
        
        'e) DE LAS GARANTÍAS DE PAGO: '
    ]
    numero_garantia = 0
    
    

    for garantia in garantias:
        numero_garantia += 1
        # Extraemos los valores del diccionario de forma segura
        tipo = garantia.get('tipo', '[TIPO]')
        valor = garantia.get('valor', 0)
        descripcion = garantia.get('descripcion', '[DESCRIPCIÓN]')

        propietario = deudor

        pagina_3.append(

            f'DE LA {ordinal(numero_garantia)} GARANTÍA: Yo, {nombre(propietario)}, garantizo la deuda, intereses, multa por morosidad y costas procesales con garantía {tipo} sobre {descripcion}, con los siguientes datos registrales: ; '

        ) 
    for fiador in fiadores_list:
        numero_garantia += 1
        pagina_3.append(
            f'DE LA {ordinal(numero_garantia)} GARANTÍA: Yo, {nombre(fiador)}, '
            f'me constituyo en FIADOR SOLIDARIO Y MANCOMUNADO de {nombre(deudor)}, '
            'garantizando la deuda, intereses, multa por morosidad y costas procesales '
            f'con el salario que devengo como empleado de {fiador.info_laboral()}. '
            f'Yo, {nombre(fiador)}, renuncio al fuero de mi domicilio y me someto expresamente a los tribunales que la Entidad Acreedora elija, señalando desde ya como lugar para recibir citaciones, notificaciones y emplazamientos en la siguiente dirección:'
            f'{fiador.get_direccion().street}, '
            f'zona {fiador.get_direccion().number}, '
            f'{fiador.get_direccion().state}, '
            f'{fiador.get_direccion().city}; '
        )
    pagina_3.append(
        f'SEGUNDA: Por mi parte Yo, {REPRESENTANTE}, en mi calidad de ADMINISTRADOR ÚNICO Y REPRESENTANTE LEGAL de la entidad denominada {EMPRESA}, expreso que en los términos relacionados ACEPTO EXPRESAMENTE, para mi '
        'representada el contenido íntegro del presente contrato. '
        'TERCERA: Todos los que intervenimos en este contrato, en las calidades '
        'en que actuamos, declaramos que ACEPTAMOS EXPRESAMENTE, el contenido íntegro del presente.'
    )

    comparecientes = [deudor, *fiadores_list]
    identificaciones = '; '.join(f'{nombre(p)}: {p.get_numero_identificacion_en_letras()}' for p in comparecientes)
    pagina_4 = [
        'Leemos lo escrito y bien impuestos de su contenido, objeto, valor y demás '
        'efectos legales, lo aceptamos, ratificamos y firmamos. '
        f'En la ciudad de Cobán del departamento de Alta Verapaz, a {fecha}. '
        'Como Notario en ejercicio DOY FE: Que las firmas que anteceden son AUTÉNTICAS, '
        'por haber sido puestas hoy a mi presencia en el CONTRATO DE RECONOCIMIENTO, día de hoy a mi presencia por los señores: '
        f'{", ".join(nombre(p) for p in comparecientes)} y '
        f'{REPRESENTANTE}, de la entidad denominada {EMPRESA}, '
        f'quienes se identifican con los Documentos Personales de '
        f'Identificación -DPI- números: {identificaciones}; y el representante legal '
        'con DPI número un mil ochocientos treinta y siete espacio once mil '
        'ochocientos ochenta y dos espacio un mil seiscientos uno, extendidos por '
        'el Registro Nacional de las Personas -RENAP-, de la República de Guatemala, '
        'quienes vuelven a firmar junto conmigo la presente acta de legalización de firmas. ANTE MÍ:'
    ]
    return [pagina_1, pagina_2, pagina_3, pagina_4]



