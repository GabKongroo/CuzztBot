import yt_dlp
import asyncio

YDL_OPTIONS = {
    "format": "bestaudio[ext=m4a]/bestaudio/best",
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
    "source_address": "0.0.0.0",
    "outtmpl": "-",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "64",  # audio a 64 kbps
    }]
}


FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -loglevel panic',
    # Non specificare path assoluto, lascia ffmpeg nel PATH di sistema
    'executable': 'ffmpeg'
}



async def extract_info(search):
    def _extract():
        try:
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                print(f"[DEBUG] Estraendo informazioni per: {search}")
                return ydl.extract_info(search, download=False)
        except Exception as e:
            print(f"[ERROR] Errore nell'estrazione dei dati: {e}")
            return None
    return await asyncio.to_thread(_extract)

