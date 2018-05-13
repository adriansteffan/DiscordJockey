from discord.ext import commands

from musicbot.utils import *


class Music:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='yt')
    async def _play_youtube(self, ctx, youtube_link):

        current_guild = get_guild(self.bot, ctx.message)

        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        audiocontroller = guild_to_audiocontroller[current_guild]
        await audiocontroller.add_song(youtube_link)

    @commands.command(name='pause')
    async def _pause(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            return
        current_guild.voice_client.pause()

    @commands.command(name='stop')
    async def _stop(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        await guild_to_audiocontroller[current_guild].stop_player()

    @commands.command(name='skip')
    async def _skip(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            return
        current_guild.voice_client.stop()

    @commands.command(name='prev')
    async def _prev(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        guild_to_audiocontroller[current_guild].prev_song()

    @commands.command(name='resume')
    async def _resume(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        current_guild.voice_client.resume()

    @commands.command(name='vol')
    async def _volume(self, ctx, volume):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return

        guild_to_audiocontroller[current_guild].volume = volume


def setup(bot):
    bot.add_cog(Music(bot))
