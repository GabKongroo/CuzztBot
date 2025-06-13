import asyncio
import discord
import urllib
import yt_dlp
from yt_dlp import YoutubeDL
from .queue import MusicQueue  
from .youtube_handler import *



class Play:
    def __init__(self, client):
        self.client = client
        self.music_queue = MusicQueue() 
        self.extract_info = extract_info
        

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
                    # Playlist Mix
                    playlist_url = search  # Usa direttamente l'URL passato nel comando
                    await ctx.send("⚠️ Hai inserito una playlist Mix di YouTube.\n🎲 I contenuti potrebbero essere casuali.")

                    flat_options = YDL_OPTIONS.copy()
                    flat_options.update({
                        'extract_flat': True,
                        'quiet': False,
                        'playlistend': 30
                    })

                    def _extract_mix_flat():
                        with yt_dlp.YoutubeDL(flat_options) as ydl:
                            return ydl.extract_info(playlist_url, download=False)

                    mix_info = await asyncio.to_thread(_extract_mix_flat)

                    if not mix_info or 'entries' not in mix_info:
                        await loading_msg.edit(content="❌ Errore nel caricamento della playlist mix.")
                        return

                    playlist_entries = mix_info['entries'][:30]
                    await loading_msg.edit(content=f"📃 Mix trovato con {len(playlist_entries)} brani. Avvio...")

                    for index, entry in enumerate(playlist_entries):
                        if self.music_queue.stop_flag:
                            print("[STOP] Interruzione richiesta. Blocco il caricamento Mix.")
                            break

                        video_id = entry.get('id')
                        if not video_id:
                            continue

                        video_url = f"https://www.youtube.com/watch?v={video_id}"
                        video_info = await self.extract_info(video_url)
                        if not video_info:
                            continue

                        audio_url = video_info['url']
                        video_title = video_info.get('title', 'Sconosciuto')

                        # Aggiungi il controllo per evitare di aggiungere brani se il flag stop è attivo
                        if self.music_queue.stop_flag:
                            print("[STOP] Interruzione richiesta. Non aggiungo alla coda.")
                            break

                        if audio_url not in self.music_queue.processed_urls:
                            self.music_queue.queue.append((audio_url, video_title))
                            self.music_queue.processed_urls.add(audio_url)
                            print(f"[INFO] Aggiunto alla coda: {video_title}")

                        if index == 0 and not ctx.voice_client.is_playing():
                            await self.play_next(ctx)
                    return

                else:
                    # Playlist normale
                    playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"

                    flat_options = YDL_OPTIONS.copy()
                    flat_options['extract_flat'] = True
                    flat_options['quiet'] = True

                    def _extract_flat():
                        with yt_dlp.YoutubeDL(flat_options) as ydl:
                            return ydl.extract_info(playlist_url, download=False)

                    flat_info = await asyncio.to_thread(_extract_flat)

                    if not flat_info or 'entries' not in flat_info:
                        await loading_msg.edit(content="❌ Errore nel caricamento della playlist.")
                        return

                    playlist_entries = flat_info['entries']
                    await loading_msg.edit(content=f"📃 Playlist trovata con {len(playlist_entries)} brani. Avvio...")

                    for index, entry in enumerate(playlist_entries):
                        if self.music_queue.stop_flag:
                            print("[STOP] Interruzione richiesta. Blocco il caricamento Playlist.")
                            break

                        video_id = entry.get('id')
                        video_url_full = f"https://www.youtube.com/watch?v={video_id}"
                        video_info = await self.extract_info(video_url_full)

                        if not video_info:
                            continue

                        audio_url = video_info['url']
                        video_title = video_info.get('title', 'Sconosciuto')

                        # Aggiungi il controllo per evitare di aggiungere brani se il flag stop è attivo
                        if self.music_queue.stop_flag:
                            print("[STOP] Interruzione richiesta. Non aggiungo alla coda.")
                            break

                        if audio_url not in self.music_queue.processed_urls:
                            self.music_queue.queue.append((audio_url, video_title))
                            self.music_queue.processed_urls.add(audio_url)
                            print(f"[INFO] Aggiunto alla coda: {video_title}")

                        if index == 0 and not ctx.voice_client.is_playing():
                            await self.play_next(ctx)
            else:
                # Ricerca testuale
                query = f"ytsearch:{search}"
                info = await self.extract_info(query)
                if not info or 'entries' not in info:
                    await loading_msg.edit(content="❌ Nessun risultato trovato.")
                    return

                first_entry = info['entries'][0]
                audio_url = first_entry['url']
                video_title = first_entry.get('title', 'Sconosciuto')

                if self.music_queue.add(audio_url, video_title):  # Usa la funzione add della MusicQueue
                    print(f"[INFO] Aggiunto alla coda: {video_title}")

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
            url, title = next_song
            source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(
                source,
                after=lambda e: self.client.loop.create_task(self.play_next(ctx))
            )
            print(f"[INFO] Ora in riproduzione: {title}")
            await ctx.send(f'🎶 In riproduzione: **{title}**')
        else:
            print("[INFO] La coda è vuota. Disconnetto.")
            if ctx.voice_client:
                await ctx.voice_client.disconnect()
            await ctx.send("📭 La coda è terminata, esco dal canale.")
