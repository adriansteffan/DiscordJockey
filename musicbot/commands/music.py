from discord.ext import commands

from musicbot.utils import *


class Music:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='yt')
    async def _play_youtube(self, ctx, *, track: str):
        print(track)
        current_guild = get_guild(self.bot, ctx.message)

        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        audiocontroller = guild_to_audiocontroller[current_guild]

        if track.isspace() or not track:
            return
        await audiocontroller.add_song(track)

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
        await guild_to_audiocontroller[current_guild].prev_song()

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

    @commands.command(name='spotify')
    async def _spotify(self, ctx,  *, nick_name=None):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return

        spotify_member = None
        if not nick_name or nick_name.isspace():
            spotify_member = ctx.message.author

        else:
            for channel in current_guild.voice_channels:
                for member in channel.members:
                    if member.nick == nick_name or (member.nick is None and member.name == nick_name):
                        spotify_member = member

        if spotify_member is None:
            return
        if spotify_member.activity.name != "Spotify":
            return
        song = spotify_member.activity.title + " " + spotify_member.activity.artist

        await guild_to_audiocontroller[current_guild].add_song(song)

    @commands.command(name='songinfo')
    async def _songinfo(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        song_info = guild_to_audiocontroller[current_guild].current_songinfo

def setup(bot):
    bot.add_cog(Music(bot))
