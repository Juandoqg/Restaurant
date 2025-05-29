# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Evita prompts durante instalación de paquetes
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea y activa un entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Expone el puerto por donde servirá la app
EXPOSE 8000

# Comando de inicio
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "mysite.asgi:application"]
