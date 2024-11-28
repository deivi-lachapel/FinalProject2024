# Usa una imagen base de Python
FROM python:3.11-slim

# Instala las dependencias del sistema necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requisitos e instala las dependencias de Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de tu aplicación
COPY . .

# Ejecuta collectstatic después de copiar el código de la aplicación
RUN python manage.py collectstatic --noinput
RUN ls -la staticfiles/rest_framework


# Establece el comando por defecto para ejecutar tu aplicación
CMD ["gunicorn", "AppDevTFG2024:app", "--bind", "0.0.0.0:8000"]
