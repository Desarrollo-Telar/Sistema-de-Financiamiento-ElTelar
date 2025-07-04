# Usa una imagen de Python como base
FROM python:3.12.8

# Establece las variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Establece el directorio de trabajo en /code
WORKDIR /code

# Instala las dependencias
COPY requirements.txt /code/
RUN python -m pip install -r requirements.txt

# Copia el contenido del directorio actual al directorio de trabajo
COPY . /code/
