# Usa un'immagine base Python ufficiale
FROM python:3.13-slim

# Aggiorna apt e installa ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Crea la cartella dell'app
WORKDIR /app

# Copia requirements.txt e installa dipendenze
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice
COPY . .

# Comando per lanciare il bot
CMD ["python", "bot.py"]
