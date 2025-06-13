# Usa un'immagine base leggera ma compatibile
FROM python:3.12-slim

# Installa dipendenze di sistema necessarie
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libopus0 \
    libopus-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea la cartella dell'app
WORKDIR /app

# Copia i file del progetto
COPY . .

# Installa le dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando per avviare il bot
CMD ["python", "main.py"]
