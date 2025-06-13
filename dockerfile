FROM python:3.12-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia tutti i file del progetto
COPY . /app

# Crea e attiva virtualenv, installa dipendenze
RUN python -m venv /opt/venv && \
    /bin/bash -c "source /opt/venv/bin/activate && pip install -r requirements.txt"

# Aggiungi la virtualenv al PATH
ENV PATH="/opt/venv/bin:$PATH"

# Comando di avvio semplice
CMD ["python", "bot.py"]
