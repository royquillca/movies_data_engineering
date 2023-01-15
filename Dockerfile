FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo requirements.txt y ejecutar pip install
COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install  -r requirements.txt

# Copiar el resto de los archivos del proyecto
COPY . .

# Establecer la variable e entorno
ENV PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 8000

# Ejecutar el comando
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
