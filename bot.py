import os
import discord
from discord.ext import commands
import asyncio
from cogs.music import music_controller  
from dotenv import load_dotenv

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
