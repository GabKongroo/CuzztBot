import yt_dlp
import asyncio
import os
import uuid

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
    "outtmpl": f"{DOWNLOAD_DIR}/%(title).64s.%(ext)s",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "64",
    }]
}

async def extract_info(search, download=True):
    def _extract():
        try:
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(search, download=download)
                if 'entries' in info:
                    info = info['entries'][0]
                return {
                    'title': info.get('title', 'Sconosciuto'),
                    'filepath': ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
                }
        except Exception as e:
            print(f"[ERROR] Errore nell'estrazione dei dati: {e}")
            return None
    return await asyncio.to_thread(_extract)
