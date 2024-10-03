# Imagen de python
FROM python:3.12-slim


RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar archivos 
COPY . .
# Instalar requirements
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto
EXPOSE 8000

# Compando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]