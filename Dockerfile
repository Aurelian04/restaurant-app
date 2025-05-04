# Imagine de bază
FROM python:3.12-slim

# Setează directorul de lucru
WORKDIR /app

# Instalează dependințele de sistem pentru psycopg2 și Pillow
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiază fișierul requirements și instalează pachetele Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiază tot codul aplicației
COPY . .

# Expune portul aplicației
EXPOSE 8000

# Comandă default: pornește aplicația Django cu Gunicorn
CMD ["gunicorn", "restaurant_app.wsgi:application", "--bind", "0.0.0.0:8000"]
