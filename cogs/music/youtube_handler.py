import yt_dlp
import asyncio

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioquality': 1,
    'outtmpl': 'downloads/%(id)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'quiet': True,
    'logtostderr': False,
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -loglevel panic'
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

