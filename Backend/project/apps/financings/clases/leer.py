import pdfplumber
import pandas as pd

file_path = 'apps/financings/clases/Movs_XXXXXXXXXX8868_Últimos5Movimientos.csv'

df = pd.read_csv(file_path)
df.head(5)

"""
# Leer el archivo de texto
with open(file_path, 'r', encoding='latin1') as file:
    lines = file.readlines()

# Inicializar lista para almacenar los datos
data = []

# Recorrer las líneas del archivo
for line in lines:
    # Dividir las líneas por tabulaciones o espacios
    parts = line.split()
    
    # Verificar si la línea tiene el número correcto de elementos para ser válida
    if len(parts) >= 9:
        date = parts[0]  # Fecha
        print(parts[7])
        reference = parts[3]  # Referencia
        try:
            credit = float(parts[7].replace(',', ''))  # Crédito
            if credit > 0:  # Si el valor de crédito es mayor que cero
                data.append((date, reference, credit))
        except ValueError:
            continue

# Crear un DataFrame con los datos extraídos
df = pd.DataFrame(data, columns=['Fecha', 'Referencia', 'Crédito (+)'])

# Mostrar el DataFrame resultante
print(df.head())

"""
"""

# Ruta al archivo PDF
file_path = 'apps/financings/clases/Movs_XXXXXXXXXX8868_01_08_2024_04_09_2024.pdf'


# Abrir el archivo PDF
with pdfplumber.open(file_path) as pdf:
    # Extraer todas las páginas
    pages = [page.extract_text() for page in pdf.pages]

# Unir el texto de todas las páginas
text = "\n".join(pages)

# Procesar el texto para extraer fechas, referencias y créditospip
data = []
lines = text.split('\n')
for line in lines:
    # Suponiendo que las líneas tienen el formato: "Fecha Referencia Descripción Débito Crédito"clear
    parts = line.split()
    if len(parts) >= 5:
        date = parts[0]
        print(parts[4])
        reference = parts[3]
        # Intentar convertir la última columna en un número (es el crédito)
        try:
            credit = float(parts[-1].replace('Q', '').replace(',', ''))
            data.append((date, reference, credit))
        except ValueError:
            continue

# Crear un DataFrame con los datos extraídos
df = pd.DataFrame(data, columns=['Fecha', 'Referencia', 'Crédito (+)'])

# Mostrar el DataFrame resultante
print(df.head())
"""