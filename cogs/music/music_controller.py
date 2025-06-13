from discord.ext import commands
from .play import Play

class MusicController(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.play_handler = Play(client)

    @commands.command(name='play')
    async def play(self, ctx, *, search):
        await self.play_handler.play(ctx, search=search)

    @commands.command(name='stop')
    async def stop(self, ctx):
        # Ferma la musica, svuota la coda e disconnette
        await self.play_handler.music_queue.stop(ctx)

    @commands.command(name='skip')
    async def skip(self, ctx):
        # Salta il brano corrente
        await self.play_handler.music_queue.skip(ctx)

    @commands.command(name='clear_queue')
    async def clear_queue(self, ctx):
        # Pulisce la coda
        await self.play_handler.music_queue.clear(ctx)

    @commands.command(name='queue')
    async def show_queue(self, ctx):
        # Mostra la coda
        await self.play_handler.music_queue.show_queue(ctx)

    @commands.command(name='raffaele')
    async def raffaele(self, ctx):
        # Mostra la vera identià di Raffaele
        await ctx.send("⚠️ Raffaele è gay! 😏")