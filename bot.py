import os
import discord
from discord.ext import commands
import asyncio
from cogs.music import music_controller  
from dotenv import load_dotenv
import subprocess, logging
import ctypes.util
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

try:
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
    logging.info("FFmpeg trovato: " + result.stdout.splitlines()[0])
except Exception as e:
    logging.error("FFmpeg NON trovato o non funziona: " + str(e))

print("[DEBUG] Ricerca libopus:", ctypes.util.find_library('opus'))

if not discord.opus.is_loaded():
    try:
        discord.opus.load_opus('libopus.so.0')  # Versione più comune
        print("[INFO] Opus caricato correttamente.")
    except Exception as e:
        print(f"[ERROR] Impossibile caricare Opus: {e}")




# Carica variabili d'ambiente da .env (solo in locale)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = commands.Bot(command_prefix='.', intents=intents)

async def main():
    async with client:
        await client.add_cog(music_controller.MusicController(client))  

        token = os.getenv("DISCORD_TOKEN")
        if not token:
            print("❌ ERRORE: DISCORD_TOKEN non trovato nelle variabili d'ambiente.")
            return
        await client.start(token)

asyncio.run(main())
