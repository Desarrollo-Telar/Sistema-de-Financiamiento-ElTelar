
import json

# Modelos
from apps.customers.models import Customer
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome
from apps.financings.models import Guarantees, DetailsGuarantees

# Funcionalidades
from django.db.models import Value, F
from django.db.models.functions import Concat

TIPO_GARANTIA = 'FIADOR'

def especificaciones(codigo_cliente, nombre, lugar_trabajo, ingresos,numero_telefono):
    texto = { 
        "Codigo_de_Cliente": codigo_cliente, 
        "Nombre": nombre, 
        "Lugar_de_Trabajo": lugar_trabajo, 
        "Ingresos": ingresos, 
        "Numero_de_Telefono": numero_telefono, 
        "fotografia": "" 
    }

    return texto

def filtro_cliente(nombre_completo):
    customers = Customer.objects.annotate(
        full_name=Concat(F('first_name'), Value(' '), F('last_name'))
    ).filter(full_name__icontains=nombre_completo).first()
    return customers

def buscar_informacion_laboral(cliente):
    informacion_laboral = WorkingInformation.objects.filter(customer_id=cliente.id).first()
    otra_fuente_ingreso = OtherSourcesOfIncome.objects.filter(customer_id=cliente.id).first()

    informacion_ingresos = None
    lugar_trabajo = None

    if informacion_laboral is not None:
        informacion_ingresos = informacion_laboral.f_salary()
        lugar_trabajo = informacion_laboral.company_name
        return informacion_ingresos,lugar_trabajo
    
    if otra_fuente_ingreso is not None:
        informacion_ingresos = otra_fuente_ingreso.f_salary()
        lugar_trabajo = otra_fuente_ingreso.source_of_income
        return informacion_ingresos,lugar_trabajo
    
    return informacion_ingresos,lugar_trabajo
    
    


def filtro_fiador(customers):
    if customers is not None:
        ingresos_chamba, lugar_chamba = buscar_informacion_laboral(customers)

        codigo_cliente = customers.customer_code
        nombre = f'{customers.first_name} {customers.last_name}'
        lugar_trabajo = lugar_chamba
        ingresos = ingresos_chamba
        numero_telefono = customers.telephone
        return especificaciones(codigo_cliente, nombre, lugar_trabajo, ingresos, numero_telefono)
    
    return None

def registrar_garantia(nombre_cliente, nombre_fiador):

    cliente = filtro_cliente(nombre_cliente)
    fiadors = filtro_cliente(nombre_fiador)
    listado = []

    if cliente is not None:
        
        garantias = Guarantees.objects.filter(credit_id__customer_id=cliente.id)
        valor = False
        if garantias is not None:
            
            for garantia in garantias:
                garantias_registradas = DetailsGuarantees.objects.filter(garantia_id=garantia.id, tipo_garantia='FIADOR')

                for registro in garantias_registradas:
                    registro.delete()

                if fiadors is not None:   
                    nuevo_detalle_garantia = DetailsGuarantees.objects.create(
                        garantia_id=garantia,
                        tipo_garantia='FIADOR',
                        especificaciones =filtro_fiador(fiadors),
                        valor_cobertura = 0
                    )
                else:
                    nuevo_detalle_garantia = DetailsGuarantees.objects.create(
                        garantia_id=garantia,
                        tipo_garantia='FIADOR',
                        especificaciones = { 
                            "Codigo_de_Cliente": "NO ESTA REGISTRADO", 
                            "Nombre": nombre_fiador, 
                            "Lugar_de_Trabajo": "NO ESTA REGISTRADO", 
                            "Ingresos": "NO ESTA REGISTRADO", 
                            "Numero_de_Telefono": "NO ESTA REGISTRADO", 
                            "fotografia": "" 
                        },
                        valor_cobertura = 0
                    )
                
                
                valor = True

                informacion = {
                    'nombre_cliente':nombre_cliente,
                    'nombre_fiador':nombre_fiador,
                    'vinculado':valor,
                    'codigo_credito':garantia.credit_id.codigo_credito
                }

                listado.append(informacion)

    else:
        informacion = {
            'nombre_cliente':nombre_cliente,
            'nombre_fiador':nombre_fiador,
            'vinculado':False
        }
        
        listado.append(informacion)
    
    print(listado)



listado_clientes = [
    "DAVID RONAL ENRIQUE BOL YAT",
    "BILLY ROMAN PONCE PINELO",
    "SONIA MARLENE DELGADO LÓPEZ DE PONCE",
    "MILSY KANDYNIA GARZONA CANO DE CÚ",
    "EDGAR ROLANDO TZUL CHÉN",
    "ALIDA REGINA GÓMEZ VALIENTE DE QUEJ",
    "ANA ELIZABETH CACAO",
    "BYRON ANTONIO ACTE CACAO",
    "VIVIANA PRISCILA AYALA TELLO",
    "ERWIN ARMANDO TOT PAÁU",
    "LEIDY LIZET JALAL CHUB DE CAAL",
    "CARLOS HUMBERTO DE JESUS WELLMAN REYES",
    "WILMMER EDENILZON POP SANCHEZ",
    "ERWIN RAFAEL XOL AC",
    "FREDY MIGUEL SAGUI CORADO",
    "JORGE MARIO CHUN",
    "JONATHAN RONALDO ASIG MAAS",
    "VIVIANA PRISCILA AYALA TELLO",
    "AUGUSTÍN GARCÍA SIS",
    "LUIS FERNANDO URBINA GONZÁLEZ",
    "MÍLVIA CONSUELO PÉREZ IGLESIAS",
    "RENSSO GUSTAVO LIGORRIA MEZA",
    "RACHELL LINDA EUNICE CHOC YAT",
    "DUNIA CLAUDETH GARZONA CANO",
    "MAYRA LUCRECIA SIERRA",
    "VIVIANA PRISCILA AYALA TELLO",
    "YOSELIN TAMARA LEAL ARRIOLA",
    "EDDER EMILIO CAAL BOL",
    "ADRIÁN ALÁN ELÍAS YAXCAL CUCUL",
    "VIVIANA PRISCILA AYALA TELLO",
    "JOSE DAVID NAVARRO QUIROA",
    "MERCEDES JOSEFINA TORRES GÁLVEZ",
    "SILVIA ISMENE ANAHI CHOCÓN OLIVIA",
    "YENIFER CELESTE AMARILIS CUCUL CAAL",
    "VIVIANA PRISCILA AYALA TELLO",
    "HUGO KEYNER QUIB CAAL",
    "ALEX GEOVANNY POP BAC",
    "GERSON MOISES ORELLANA GONZÁLEZ",
    "BRYAN RUBÉN DARÍO CASTILLO FERNÁNDEZ",
    "PEDRO EFRAIN CAN PAAU",
    "NELIDA PATRICIA HERNANDEZ SUCUP DE POP",
    "MARÍA ROSAURA MACZ ARTOLA",
    "KARLA YESENIA YAT LOAYZA DE CHEN",
    "JORGE MARIO CHUN",
    "LUIS DAVID CHEN CHAJ",
    "CLAUDIA ESMERALDA GABRIELA SAGÜI CAAL",
    "ALIDA REGINA GÓMEZ VALIENTE DE QUEJ",
    "LIDIA AMABILIA OXOM SACRAB DE CHÚN",
    "MARTHA OLIVIA TZUB POOÚ DE TENI",
    "VIVIANA PRISCILA AYALA TELLO",
    "HAMILTON MANOLO MÓ COL",
    "MÍLVIA CONSUELO PÉREZ IGLESIAS",
    "FILIBERTO CAAL XEP",
    "SHERLY VIVIANA LEAL SAGUI",
    "BLANCA FLORIDALMA QUEJ CHIQUIN DE JOR",
    "ANA SILVIA MARTÍNEZ CASTAÑEDA",
    "RENSSO GUSTAVO LIGORRIA MEZA",
    "MILSY KANDYNIA GARZONA CANO DE CÚ",
    "BRYAN RUBÉN DARÍO CASTILLO FERNÁNDEZ"
]


listado_fiadores = [
    "OSCAR MAGALIEL SOTO GODÍNEZ",
    "MARIA FERNANDA MARTINEZ CRUZ DE PONCE",
    "MELANY GISSELL VENTURA DELGADO",
    "DUNIA CLAUDETH GARZONA CANO",
    "MARIO RENÉ YALIBAT PACAY",
    "ANA ELIZABETH RIVEIRO CACAO",
    "ALIDA REGINA GÓMEZ VALIENTE DE QUEJ",
    "MARVIN RIGOBERTO ACTÉ CACAO",
    "HERBERT ROLANDO TAROT CASTRO",
    "JOSÉ ARMANDO TOT MORÁN",
    "FILIBERTO CAAL XEP",
    "MARTHA GABRIELA REYES CRUZ",
    "BLANCA LISSETH QUEVEDO YAT",
    "FREDY MIGUEL SAGUI CORADO",
    "ERWIN RAFAEL XOL AC",
    "VICTORIA MARIBEL CAAL BARRIOS",
    "HARY DARÍO HUN CAAL",
    "HERBERT ROLANDO TAROT CASTRO",
    "HAMILTON ESECHIAS GAMARRO TIUL",
    "LUIS EDUARDO URBINA GARCIA",
    "FLOR DE MARIA IGLESIAS PERDOMO",
    "KARLA PATRICIA REYES CRUZ",
    "EDWIN JOSUÉ GARCÍA REYES",
    "MILSY KANDYNIA GARZONA CANO DE CÚ",
    "JORGE MARIO CHUN",
    "HERBERT ROLANDO TAROT CASTRO",
    "IVANNA RENATA ALVARADO CATELLANOS",
    "LINDA ANGELINA GUADALUPE CAAL BOL",
    "HUGO ROLANDO POP",
    "HERBERT ROLANDO TAROT CASTRO",
    "ESTEFANY ABIGAIL LEAL MAQUIM",
    "VITALINO ALEXANDER DE LOS SANTOS GOMEZ",
    "ALLAN OMAR PACAY CÚ",
    "ANGEL DONALDO CUCUL CAAL",
    "HERBERT ROLANDO TAROT CASTRO",
    "ALEX GEOVANNY POP BAC",
    "SUANY ELIZABETH QUIB CAL DE POP",
    "PERLA NAHOMY MARROQUÍN MILIÁN",
    "AIANA ALEYDA BETSABÉ MAAS TUCHEZ",
    "ALEX ESTUARDO JOSUÉ MACZ RAMIREZ",
    "GERWY OSWALDO POP CUCUL",
    "FRANCISCO SALVADOR HERRERA YALIBAT",
    "MARIO ANTONIO CHEN CAAL",
    "VICTORIA MARIBEL CAAL BARRIOS",
    "ORFA NOHEMY GRANILLO LINARES DE CHEN",
    "MARIO RODOLFO ICAL BOTZOC",
    "ANA ELIZABETH RIVEIRO CACAO",
    "ERWIN LIZARDO OXOM SACRAB",
    "LILI MAGALI COY MACZ",
    "HERBERT ROLANDO TAROT CASTRO",
    "ALBERTO DE JESUS MACZ",
    "FLOR DE MARIA IGLESIAS PERDOMO",
    "LEIDY LIZET JALAL CHUB DE CAAL",
    "SHEYLA ANAGALI MAGALI LEAL SAGUI",
    "BAULIDIO JOR LOPEZ",
    "NIDIA MARISOL CASTAÑEDA ALONZO",
    "KARLA PATRICIA REYES CRUZ",
    "DUNIA CLAUDETH GARZONA CANO",
    "AIANA ALEYDA BETSABÉ MAAS TUCHEZ"
]

def limpiar_fiadores(clientes, fiadores):
    clientes_vistos = set()
    fiadores_actualizados = []

    for idx, cliente in enumerate(clientes):
        if cliente in clientes_vistos:
            # Cliente repetido: eliminamos el fiador en esa posición
            fiadores_actualizados.append(None)
        else:
            clientes_vistos.add(cliente)
            fiadores_actualizados.append(fiadores[idx])

    return fiadores_actualizados


def main_vincular():
    fiadores_limpios = limpiar_fiadores(listado_clientes, listado_fiadores)

    for cliente, fiador in zip(listado_clientes, fiadores_limpios):
        if fiador is not None:
            registrar_garantia(cliente, fiador)
    
    listado = []

    for fiador in fiadores_limpios:

        if fiador is not None:
            verificar = filtro_cliente(fiador)
            if verificar is None:
                listado.append(fiador)


    print(listado)
