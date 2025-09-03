import xml.etree.ElementTree as ET
from datetime import datetime

# Namespaces
ns = {
    "dte": "http://www.sat.gob.gt/dte/fel/0.2.0",
    "ds": "http://www.w3.org/2000/09/xmldsig#",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance"
}

# Registrar namespaces para que aparezcan en el XML
ET.register_namespace("dte", ns["dte"])
ET.register_namespace("ds", ns["ds"])
ET.register_namespace("xsi", ns["xsi"])

def generar_factura_xml(receptor_data,nombre_archivo="FACTURA_GENERADA.xml"):
    fecha_actual = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-06:00")

    # Nodo raíz
    root = ET.Element("{http://www.sat.gob.gt/dte/fel/0.2.0}GTDocumento", {
        "Version": "0.1",
        "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation": "http://www.sat.gob.gt/dte/fel/0.2.0"
    })

    sat = ET.SubElement(root, "{http://www.sat.gob.gt/dte/fel/0.2.0}SAT", {"ClaseDocumento": "dte"})
    dte = ET.SubElement(sat, "{http://www.sat.gob.gt/dte/fel/0.2.0}DTE", {"ID": "DatosCertificados"})
    datos_emision = ET.SubElement(dte, "{http://www.sat.gob.gt/dte/fel/0.2.0}DatosEmision", {"ID": "DatosEmision"})

    # Datos generales
    ET.SubElement(datos_emision, "{http://www.sat.gob.gt/dte/fel/0.2.0}DatosGenerales", {
        "CodigoMoneda": "GTQ",
        "FechaHoraEmision": fecha_actual,
        "Tipo": "FACT"
    })

    # Emisor
    emisor = ET.SubElement(datos_emision, "{http://www.sat.gob.gt/dte/fel/0.2.0}Emisor", {
        "AfiliacionIVA": "GEN",
        "CodigoEstablecimiento": "1",
        "CorreoEmisor": "demo@demo.com.gt",
        "NITEmisor": "1000000000K",
        "NombreComercial": "DEMO",
        "NombreEmisor": "DEMO, SOCIEDAD ANONIMA"
    })

    direccion_emisor = ET.SubElement(emisor, "{http://www.sat.gob.gt/dte/fel/0.2.0}DireccionEmisor")
    ET.SubElement(direccion_emisor, "{http://www.sat.gob.gt/dte/fel/0.2.0}Direccion").text = "CUIDAD"
    ET.SubElement(direccion_emisor, "{http://www.sat.gob.gt/dte/fel/0.2.0}CodigoPostal").text = "01001"
    ET.SubElement(direccion_emisor, "{http://www.sat.gob.gt/dte/fel/0.2.0}Municipio").text = "GUATEMALA"
    ET.SubElement(direccion_emisor, "{http://www.sat.gob.gt/dte/fel/0.2.0}Departamento").text = "GUATEMALA"
    ET.SubElement(direccion_emisor, "{http://www.sat.gob.gt/dte/fel/0.2.0}Pais").text = "GT"

    # Receptor
    receptor = ET.SubElement(datos_emision, "{http://www.sat.gob.gt/dte/fel/0.2.0}Receptor", {
        "CorreoReceptor": receptor_data.get("correo", ""),
        "IDReceptor": receptor_data.get("id", ""),
        "NombreReceptor": receptor_data.get("nombre", "")
    })

    direccion_receptor = ET.SubElement(receptor, "{http://www.sat.gob.gt/dte/fel/0.2.0}DireccionReceptor")
    ET.SubElement(direccion_receptor, "{http://www.sat.gob.gt/dte/fel/0.2.0}Direccion").text = "CUIDAD"
    ET.SubElement(direccion_receptor, "{http://www.sat.gob.gt/dte/fel/0.2.0}CodigoPostal").text = "01001"
    ET.SubElement(direccion_receptor, "{http://www.sat.gob.gt/dte/fel/0.2.0}Municipio").text = "GUATEMALA"
    ET.SubElement(direccion_receptor, "{http://www.sat.gob.gt/dte/fel/0.2.0}Departamento").text = "GUATEMALA"
    ET.SubElement(direccion_receptor, "{http://www.sat.gob.gt/dte/fel/0.2.0}Pais").text = "GT"

    # Frases
    frases = ET.SubElement(datos_emision, "{http://www.sat.gob.gt/dte/fel/0.2.0}Frases")
    ET.SubElement(frases, "{http://www.sat.gob.gt/dte/fel/0.2.0}Frase", {"CodigoEscenario": "1", "TipoFrase": "1"})
    ET.SubElement(frases, "{http://www.sat.gob.gt/dte/fel/0.2.0}Frase", {"CodigoEscenario": "1", "TipoFrase": "2"})

    # Items
    items = ET.SubElement(datos_emision, "{http://www.sat.gob.gt/dte/fel/0.2.0}Items")
    item = ET.SubElement(items, "{http://www.sat.gob.gt/dte/fel/0.2.0}Item", {
        "BienOServicio": "B",
        "NumeroLinea": "1"
    })
    ET.SubElement(item, "{http://www.sat.gob.gt/dte/fel/0.2.0}Cantidad").text = "1.00"
    ET.SubElement(item, "{http://www.sat.gob.gt/dte/fel/0.2.0}UnidadMedida").text = "UND"
    ET.SubElement(item, "{http://www.sat.gob.gt/dte/fel/0.2.0}Descripcion").text = "PRODUCTO1"
    ET.SubElement(item, "{http://www.sat.gob.gt/dte/fel/0.2.0}PrecioUnitario").text = "120.00"
    ET.SubElement(item, "{http://www.sat.gob.gt/dte/fel/0.2.0}Precio").text = "120.00"
    ET.SubElement(item, "{http://www.sat.gob.gt/dte/fel/0.2.0}Descuento").text = "0.00"

    impuestos = ET.SubElement(item, "{http://www.sat.gob.gt/dte/fel/0.2.0}Impuestos")
    impuesto = ET.SubElement(impuestos, "{http://www.sat.gob.gt/dte/fel/0.2.0}Impuesto")
    ET.SubElement(impuesto, "{http://www.sat.gob.gt/dte/fel/0.2.0}NombreCorto").text = "IVA"
    ET.SubElement(impuesto, "{http://www.sat.gob.gt/dte/fel/0.2.0}CodigoUnidadGravable").text = "1"
    ET.SubElement(impuesto, "{http://www.sat.gob.gt/dte/fel/0.2.0}MontoGravable").text = "107.14"
    ET.SubElement(impuesto, "{http://www.sat.gob.gt/dte/fel/0.2.0}MontoImpuesto").text = "12.86"

    ET.SubElement(item, "{http://www.sat.gob.gt/dte/fel/0.2.0}Total").text = "120.00"

    # Totales
    totales = ET.SubElement(datos_emision, "{http://www.sat.gob.gt/dte/fel/0.2.0}Totales")
    total_impuestos = ET.SubElement(totales, "{http://www.sat.gob.gt/dte/fel/0.2.0}TotalImpuestos")
    ET.SubElement(total_impuestos, "{http://www.sat.gob.gt/dte/fel/0.2.0}TotalImpuesto", {
        "NombreCorto": "IVA",
        "TotalMontoImpuesto": "12.86"
    })
    ET.SubElement(totales, "{http://www.sat.gob.gt/dte/fel/0.2.0}GranTotal").text = "120.00"

    # Adenda
    adenda = ET.SubElement(sat, "{http://www.sat.gob.gt/dte/fel/0.2.0}Adenda")
    ET.SubElement(adenda, "Codigo_cliente").text = "C01"
    ET.SubElement(adenda, "Observaciones").text = "ESTA ES UNA ADENDA"

    # Guardar el archivo
    tree = ET.ElementTree(root)
    tree.write(nombre_archivo, encoding="UTF-8", xml_declaration=True)

    print(f"Archivo XML generado: {nombre_archivo}")


