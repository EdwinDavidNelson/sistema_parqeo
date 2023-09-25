# Usa una imagen base de Python
FROM python:latest

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
ADD requirements.txt requirements.txt

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Copia el contenido del directorio actual al directorio de trabajo
# Se copia el archivo app.py de mi directorio local al directorio root del contenedor
COPY main.py main.py

# Comando para ejecutar la aplicación cuando se ejecute el contenedor
CMD ["python", "app.py"]