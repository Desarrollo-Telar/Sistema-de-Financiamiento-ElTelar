import os
import django

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()



import json

from apps.FinancialInformation.models import GastoCliente, Reference, WorkingInformation, OtherSourcesOfIncome

# --- 1. Definición de la estructura del Nodo (más general para carga dinámica) ---
class NodoDinamico:
    def __init__(self, id_paso, texto, clave_validacion=None, id_si=None, id_no=None):
        self.id_paso = id_paso
        self.texto = texto
        self.clave_validacion = clave_validacion # <--- Nueva propiedad
        self.id_si = id_si 
        self.id_no = id_no
        self.nodo_si = None
        self.nodo_no = None

    def es_pregunta(self):
        return self.id_si is not None and self.id_no is not None

# --- 2. Carga dinámica del árbol desde JSON ---
def cargar_arbol_desde_json(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    configuracion_arbol = datos["estructura_arbol"]
    
    # Paso 2.1: Crear todos los objetos Nodo primero
    diccionario_nodos = {}
    for id_p, info in configuracion_arbol.items():
        diccionario_nodos[id_p] = NodoDinamico(
            id_p=id_p,
            texto=info['texto'],
            clave_validacion=info.get('clave_validacion'),  # <--- ¡ESTE ES EL CAMBIO CLAVE!
            id_si=info.get('id_si'),
            id_no=info.get('id_no')
        )
        
    # Paso 2.2: Conectar los nodos (vincular objetos)
    for id_p, nodo in diccionario_nodos.items():
        if nodo.id_si in diccionario_nodos:
            nodo.nodo_si = diccionario_nodos[nodo.id_si]
        if nodo.id_no in diccionario_nodos:
            nodo.nodo_no = diccionario_nodos[nodo.id_no]
            
    # El nodo raíz es el primero (id "1")
    return diccionario_nodos["1"]



def evaluar_condicion(cliente_id, clave):
    """
    Función auxiliar que ejecuta la consulta ORM real basada 
    en la clave de validación del nodo.
    """
    if clave == "tiene_info_laboral":
        # Verifica si existe al menos un registro laboral para este cliente
        informacion_laboral = False
        if WorkingInformation.objects.filter(customer_id=cliente_id).exists():
            informacion_laboral = True

        elif OtherSourcesOfIncome.objects.filter(customer_id=cliente_id).exists():
            informacion_laboral = True
    

        return informacion_laboral
        
    elif clave == "tiene_gastos":
        # Verifica si existen registros de gastos
        return GastoCliente.objects.filter(customer=cliente_id).exists()
        
    elif clave == "tiene_referencias":
        # Verifica si existen referencias personales
        return Reference.objects.filter(customer_id=cliente_id).exists()
        
    return False


def ejecutar_checklist_dinamico(raiz, cliente_id):
    print(f"\n--- Evaluando Checklist Automático para Cliente ID: {cliente_id} ---")
    nodo_actual = raiz
    ultimo_nodo_accion = None
    
    while nodo_actual is not None:
        if nodo_actual.es_pregunta():
            # CONSULTA AUTOMÁTICA A LA BASE DE DATOS
            # Evaluamos la clave de validación del nodo actual
            tiene_registro = evaluar_condicion(cliente_id, nodo_actual.clave_validacion)
            
            if tiene_registro:
                print(f"[BD - SI] El cliente cumple: {nodo_actual.texto}")
                nodo_actual = nodo_actual.nodo_si
            else:
                print(f"[BD - NO] El cliente NO cumple: {nodo_actual.texto}")
                nodo_actual = nodo_actual.nodo_no
        else:
            # Es un nodo de acción (Guardar información o ir al Perfil)
            print(f"[RESULTADO EVALUADO] -> {nodo_actual.texto}")
            
            # Guardamos este nodo porque representa la acción o destino final
            if nodo_actual.id_paso != "finalizar_flujo":
                ultimo_nodo_accion = nodo_actual
                
            # Avanzamos (en tu flujo, las acciones van hacia 'finalizar_flujo' o mueren en None)
            nodo_actual = nodo_actual.nodo_si if nodo_actual.nodo_si else None
            
    # Retorna el objeto del último nodo de acción alcanzado para usarlo en tus vistas
    return ultimo_nodo_accion

# --- Ejecución del Programa ---
if __name__ == "__main__":
    try:
        # 1. Cargar el árbol dinámicamente
        raiz_dinamica = cargar_arbol_desde_json('arbol_checklist.json')
        
        # 2. Ejecutar el checklist
        ejecutar_checklist_dinamico(raiz_dinamica)
        
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'arbol_checklist.json'. Por favor, asegúrese de crearlo.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")