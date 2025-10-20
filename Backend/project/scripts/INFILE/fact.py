from django.utils import timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Union
from pathlib import Path

# MODELS
from apps.financings.models import Invoice

# ==========================
# CONFIGURACIÓN GLOBAL
# ==================================
# Namespaces
DTE_NS = "http://www.sat.gob.gt/dte/fel/0.2.0"
DS_NS = "http://www.w3.org/2000/09/xmldsig#"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"


ET.register_namespace('dte', DTE_NS)
ET.register_namespace('ds', DS_NS)
ET.register_namespace('xsi', XSI_NS) 

DECIMAL_PLACES = Decimal("0.01")
IVA_RATE = Decimal("0.12")
MONEDA = "GTQ"

# ==========================
# FUNCIONES DE CÁLCULO (Se mantienen igual)
# ==========================
def to_decimal(value: Union[str, float, int, Decimal]) -> Decimal:
    """Convierte un valor a Decimal con validación y redondeo a dos decimales."""
    try:
        return Decimal(str(value)).quantize(DECIMAL_PLACES, rounding=ROUND_HALF_UP)
    except (InvalidOperation, TypeError, ValueError):
        return Decimal("0.00")

def calculo_monto_gravable(monto: Union[str, float, int, Decimal]) -> Decimal:
    """Calcula el monto base sin IVA a partir de un monto con IVA incluido."""
    monto_decimal = to_decimal(monto)
    return (monto_decimal / Decimal("1.12")).quantize(DECIMAL_PLACES, rounding=ROUND_HALF_UP)

def calculo_monto_impuesto(monto: Union[str, float, int, Decimal]) -> Decimal:
    """Calcula el valor del impuesto (IVA) a partir de un monto con IVA."""
    monto_gravable = calculo_monto_gravable(monto)
    return (monto_gravable * IVA_RATE).quantize(DECIMAL_PLACES, rounding=ROUND_HALF_UP)

# ==========================
# FUNCIÓN PRINCIPAL: GENERAR XML
# ==========================
def generar_xml_recibo(recibo) -> str:
    # Simulación de las operaciones de la DB que no causan error de XML
    try:
        recibo.factura = True
        recibo.save()
    except:
        pass # Ignoramos el error de la DB para enfocarnos en el XML
    
    now_local = timezone.localtime(timezone.now()) 

    now_formatted = now_local.strftime("%Y-%m-%dT%H:%M:%S%z")
    fecha_emision_sat = now_formatted[:-2] + ":" + now_formatted[-2:]
    codigo_establecimiento = recibo.sucursal.codigo_establecimiento

   

    """
    Genera un XML para el recibo siguiendo el formato FEL de SAT Guatemala.
    """
    
    GTDocumento = ET.Element(f"{{{DTE_NS}}}GTDocumento", {
        "Version": "0.1",
        f"{{{XSI_NS}}}schemaLocation": f"{DTE_NS} {DTE_NS}", 
    })
    
    SAT = ET.SubElement(GTDocumento, f"{{{DTE_NS}}}SAT", {"ClaseDocumento": "dte"})
    DTE = ET.SubElement(SAT, f"{{{DTE_NS}}}DTE", {"ID": "DatosCertificados"})
    DatosEmision = ET.SubElement(DTE, f"{{{DTE_NS}}}DatosEmision", {"ID": "DatosEmision"})

    # --------------------------
    # Datos Generales
    # --------------------------
    ET.SubElement(DatosEmision, f"{{{DTE_NS}}}DatosGenerales", {
        "CodigoMoneda": MONEDA,
        "FechaHoraEmision": fecha_emision_sat, 
        "Tipo": "FACT"
    })

    # --------------------------
    # Emisor (Datos fijos o configurables)
    # --------------------------
    Emisor = ET.SubElement(DatosEmision, f"{{{DTE_NS}}}Emisor", {
        "AfiliacionIVA": "GEN",
        "CodigoEstablecimiento": f"{codigo_establecimiento}",
        "CorreoEmisor": "",
        "NITEmisor": "108241297",
        "NombreComercial": "EL TELAR",
        "NombreEmisor": "INVERSIONES INTEGRALES EL TELAR, SOCIEDAD ANÓNIMA"
    })

    DireccionEmisor = ET.SubElement(Emisor, f"{{{DTE_NS}}}DireccionEmisor")
    ET.SubElement(DireccionEmisor, f"{{{DTE_NS}}}Direccion").text = "8 AVENIDA COLONIA FRENTE A CONDADO MINERVA 1-12, ZONA 1"
    ET.SubElement(DireccionEmisor, f"{{{DTE_NS}}}CodigoPostal").text = "16001"
    ET.SubElement(DireccionEmisor, f"{{{DTE_NS}}}Municipio").text = "COBÁN"
    ET.SubElement(DireccionEmisor, f"{{{DTE_NS}}}Departamento").text = "ALTA VERAPAZ"
    ET.SubElement(DireccionEmisor, f"{{{DTE_NS}}}Pais").text = "GT"

    # --------------------------
    # Receptor
    # --------------------------
    
    receptor = ET.SubElement(DatosEmision, f"{{{DTE_NS}}}Receptor", {
        "CorreoReceptor": "",
        "IDReceptor": str(recibo.cliente.number_nit),
        "NombreReceptor": str(recibo.cliente)
    })

    direccion_receptor = ET.SubElement(receptor, "dte:DireccionReceptor")

    ET.SubElement(direccion_receptor, "dte:Direccion").text =  "CIUDAD"
    ET.SubElement(direccion_receptor, "dte:CodigoPostal").text =  "01001"
    ET.SubElement(direccion_receptor, "dte:Municipio").text =  "GUATEMALA"
    ET.SubElement(direccion_receptor, "dte:Departamento").text =  "GUATEMALA"
    ET.SubElement(direccion_receptor, "dte:Pais").text = "GT"

    # --------------------------
    # Frases
    # --------------------------
    Frases = ET.SubElement(DatosEmision, f"{{{DTE_NS}}}Frases")
    ET.SubElement(Frases, f"{{{DTE_NS}}}Frase", {
        "CodigoEscenario": "1",
        "TipoFrase": "1"
    })

    # --------------------------
    # Items dinámicos
    # --------------------------
    Items = ET.SubElement(DatosEmision, f"{{{DTE_NS}}}Items")
    items_data = []

    if to_decimal(recibo.interes_pagado) > 0:
        items_data.append({
            "descripcion": "Pago de Interés",
            "cantidad": Decimal("1.00"),
            "precio_unitario": to_decimal(recibo.interes_pagado)
        })

    if to_decimal(recibo.mora_pagada) > 0:
        items_data.append({
            "descripcion": "Otros Gastos Administrativos",
            "cantidad": Decimal("1.00"),
            "precio_unitario": to_decimal(recibo.mora_pagada)
        })

    total_iva = Decimal("0.00")
    gran_total = Decimal("0.00")

    for idx, item in enumerate(items_data, start=1):
        monto_gravable = calculo_monto_gravable(item["precio_unitario"])
        iva = calculo_monto_impuesto(item["precio_unitario"])

        Item = ET.SubElement(Items, f"{{{DTE_NS}}}Item", {
            "BienOServicio": "S",
            "NumeroLinea": str(idx)
        })

        ET.SubElement(Item, f"{{{DTE_NS}}}Cantidad").text = f"{item['cantidad']:.2f}"        
        ET.SubElement(Item, f"{{{DTE_NS}}}Descripcion").text = item["descripcion"]
        ET.SubElement(Item, f"{{{DTE_NS}}}PrecioUnitario").text = f"{item['precio_unitario']:.2f}"
        ET.SubElement(Item, f"{{{DTE_NS}}}Precio").text = f"{item['precio_unitario']:.2f}"
        ET.SubElement(Item, f"{{{DTE_NS}}}Descuento").text = "0.00"

        # Impuestos
        Impuestos = ET.SubElement(Item, f"{{{DTE_NS}}}Impuestos")
        Impuesto = ET.SubElement(Impuestos, f"{{{DTE_NS}}}Impuesto")
        ET.SubElement(Impuesto, f"{{{DTE_NS}}}NombreCorto").text = "IVA"
        ET.SubElement(Impuesto, f"{{{DTE_NS}}}CodigoUnidadGravable").text = "1"
        ET.SubElement(Impuesto, f"{{{DTE_NS}}}MontoGravable").text = f"{monto_gravable:.2f}"
        ET.SubElement(Impuesto, f"{{{DTE_NS}}}MontoImpuesto").text = f"{iva:.2f}"

        ET.SubElement(Item, f"{{{DTE_NS}}}Total").text = f"{item['precio_unitario']:.2f}"

        total_iva += iva
        gran_total += item["precio_unitario"]

    # --------------------------
    # Totales
    # --------------------------
    Totales = ET.SubElement(DatosEmision, f"{{{DTE_NS}}}Totales")
    TotalImpuestos = ET.SubElement(Totales, f"{{{DTE_NS}}}TotalImpuestos")
    ET.SubElement(TotalImpuestos, f"{{{DTE_NS}}}TotalImpuesto", {
        "NombreCorto": "IVA",
        "TotalMontoImpuesto": f"{total_iva:.2f}"
    })
    ET.SubElement(Totales, f"{{{DTE_NS}}}GranTotal").text = f"{gran_total:.2f}"

    
    # Convertir a XML
    xml_str = ET.tostring(GTDocumento, encoding="utf-8")
    
    
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="    ", encoding="utf-8")
    return pretty_xml.decode("utf-8")

# ==========================
# FUNCIÓN PARA GUARDAR XML 
# ==========================
from scripts.INFILE.fel_api_client import FELApiClient
def guardar_xml_recibo(recibo, nombre_archivo: str = "recibo.xml") -> str:
    """
    Genera y guarda el XML del recibo en la carpeta 'temp'
    """
    # Carpeta 'temp' en el mismo nivel que este archivo
    base_dir = Path(__file__).resolve().parent
    temp_dir = base_dir / "temp"

    # Crear carpeta si no existe
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Ruta final del archivo
    ruta_archivo = temp_dir / nombre_archivo

    # Generar el XML
    xml_content = generar_xml_recibo(recibo)
    fel_client = FELApiClient()

    

    # Enviar XML a la API FEL
    respuesta_api = fel_client.enviar_xml(xml_content, recibo)
    print("Respuesta de la API FEL:", respuesta_api)
   

    # Guardar el archivo
    ruta_archivo.write_text(xml_content, encoding="utf-8")

    return str(ruta_archivo)