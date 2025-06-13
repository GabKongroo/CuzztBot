import discord

class MusicQueue:
    def __init__(self):
        self.queue = []
        self.stop_flag = False
        self.processed_urls = set()

    def add(self, path, title):
        if not self.stop_flag and path not in [item[0] for item in self.queue]:
            self.queue.append((path, title))
            return True
        return False


    def next(self):
        return self.queue.pop(0) if self.queue else None

    async def stop(self, ctx):
        self.stop_flag = True  
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()  
            print("[INFO] Disconnesso manualmente e coda svuotata.")
            await ctx.send("🛑 Disconnesso e coda svuotata!")
            self.queue.clear()
            self.processed_urls.clear()
        else:
            await ctx.send("⚠️ Non sono in un canale vocale.")

    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            print("[INFO] Brano saltato.")
            await ctx.send("⏭️ Brano saltato!")
        else:
            await ctx.send("⚠️ Nessun brano in riproduzione.")

    async def clear(self, ctx):
        self.queue.clear()
        self.processed_urls.clear()
        await ctx.send("🗑️ La coda è stata svuotata!")

    async def show_queue(self, ctx):
        if not self.queue:
            await ctx.send("📭 La coda è vuota!")
            return
        description = ""
        for i, (_, title) in enumerate(self.queue, start=1):
            description += f"{i}. {title}\n"
        embed = discord.Embed(title="🎶 Coda attuale", description=description, color=0x1DB954)
        await ctx.send(embed=embed)
