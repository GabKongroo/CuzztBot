FROM python:3.12-slim

# Installa le librerie di sistema, compresa libopus0
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libopus0 \
    libopus-dev \
    libffi-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copia tutti i file del progetto
COPY . .

# Installa le dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Assicura che libopus sia caricabile
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu

# Avvia il bot
CMD ["python", "main.py"]
