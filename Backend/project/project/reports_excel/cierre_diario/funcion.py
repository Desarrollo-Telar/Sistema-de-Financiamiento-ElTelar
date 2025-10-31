def safe_list_get(data, index=0, default=None):
    """
    Obtiene elemento de forma segura manejando:
    - None
    - Listas
    - Diccionarios individuales
    - Índices fuera de rango
    """
    if data is None:
        return default
        
    # Si es una lista
    if isinstance(data, list):
        try:
            return data[index] if index < len(data) else default
        except IndexError:
            return default
            
    # Si es un diccionario y el índice es 0, retornar el diccionario mismo
    elif isinstance(data, dict):
        return data if index == 0 else default
        
    # Para cualquier otro tipo
    else:
        return default