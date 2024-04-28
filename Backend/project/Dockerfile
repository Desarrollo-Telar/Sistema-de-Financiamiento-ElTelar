# Usa una imagen de Python como base
FROM python:3.9

# Establece la variable de entorno PYTHONUNBUFFERED para que Python no haga buffering de la salida
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Establece el directorio de trabajo en /code
WORKDIR /code

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt /code/

# Instala las dependencias definidas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del directorio actual al directorio de trabajo
COPY . /code/

# Expone el puerto 8000 para que se pueda acceder a la aplicación desde fuera del contenedor
EXPOSE 8000

# Define el comando que se ejecutará cuando se inicie el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
