FROM python:3.10-slim

# Crear y establecer directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY . /app

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto (opcional, según tu app)
EXPOSE 5000

# Comando para iniciar tu app (ajusta si usas otro archivo o framework)
CMD ["gunicorn", "app:app"]
