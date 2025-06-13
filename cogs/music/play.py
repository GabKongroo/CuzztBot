import asyncio
import discord
import urllib
from .queue import MusicQueue  
from .youtube_handler import extract_info

class Play:
    def __init__(self, client):
        self.client = client
        self.music_queue = MusicQueue() 

    async def play(self, ctx, *, search):
        self.music_queue.stop_flag = False  

        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            return await ctx.send("🎧 Devi essere in un canale vocale!")

        if not ctx.voice_client:
            await voice_channel.connect()

        loading_msg = await ctx.send("🔎 Caricamento in corso...")

        try:
            is_url = search.startswith("http://") or search.startswith("https://")

            if is_url and "list=" in search:
                parsed = urllib.parse.urlparse(search)
                query = urllib.parse.parse_qs(parsed.query)
                playlist_id = query.get("list", [None])[0]

                if not playlist_id:
                    await loading_msg.edit(content="❌ Nessun ID playlist trovato.")
                    return
                is_mix = playlist_id.startswith("RD")
                
                if is_mix:
                    await ctx.send("⚠️ Hai inserito una playlist Mix di YouTube.\n🎲 I contenuti potrebbero essere casuali.")
                    await loading_msg.edit(content="❌ Le playlist Mix non sono supportate al momento.")
                    return
                else:
                    await loading_msg.edit(content="❌ Le playlist non sono ancora supportate in questa versione.")
                    return
            else:
                query = f"ytsearch:{search}" if not is_url else search
                info = await extract_info(query)
                if not info or not info.get('filepath'):
                    await loading_msg.edit(content="❌ Nessun risultato valido trovato.")
                    return

                filepath = info['filepath']
                title = info.get('title', 'Sconosciuto')

                if self.music_queue.add(filepath, title):
                    print(f"[INFO] Aggiunto alla coda: {title}")

                await loading_msg.delete()

                if not ctx.voice_client.is_playing():
                    await self.play_next(ctx)

        except Exception as e:
            await loading_msg.edit(content=f"❌ Errore: {e}")
            print(f"[ERROR] Durante estrazione: {e}")
            return

    async def play_next(self, ctx):
        if self.music_queue.stop_flag:
            print("[STOP] La riproduzione è stata interrotta.")
            return

        next_song = self.music_queue.next()
        if next_song:
            filepath, title = next_song
            source = discord.FFmpegPCMAudio(filepath)

            def _after_play(e):
                if filepath and os.path.exists(filepath):
                    os.remove(filepath)
                    print(f"[INFO] File temporaneo rimosso: {filepath}")
                self.client.loop.create_task(self.play_next(ctx))

            ctx.voice_client.play(source, after=_after_play)

            print(f"[INFO] Ora in riproduzione: {title}")
            await ctx.send(f'🎶 In riproduzione: **{title}**')
        else:
            print("[INFO] La coda è vuota. Disconnetto.")
            if ctx.voice_client:
                await ctx.voice_client.disconnect()
            await ctx.send("📭 La coda è terminata, esco dal canale.")
