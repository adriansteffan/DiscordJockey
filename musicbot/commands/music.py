from discord.ext import commands

from musicbot.utils import *


class Music:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='yt', description = HELP_YT_LONG, help = HELP_YT_SHORT)
    async def _play_youtube(self, ctx, *, track: str):
        print(track)
        current_guild = get_guild(self.bot, ctx.message)

        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        audiocontroller = guild_to_audiocontroller[current_guild]

        if track.isspace() or not track:
            return
        await audiocontroller.add_youtube(track)

    @commands.command(name='pause', description = HELP_PAUSE_LONG, help = HELP_PAUSE_SHORT)
    async def _pause(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            return
        current_guild.voice_client.pause()

    @commands.command(name='stop', description = HELP_STOP_LONG, help = HELP_STOP_SHORT)
    async def _stop(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        await guild_to_audiocontroller[current_guild].stop_player()

    @commands.command(name='skip', description = HELP_SKIP_LONG, help = HELP_SKIP_SHORT)
    async def _skip(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            return
        current_guild.voice_client.stop()

    @commands.command(name='prev', description = HELP_PREV_LONG, help = HELP_PREV_SHORT)
    async def _prev(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        await guild_to_audiocontroller[current_guild].prev_song()

    @commands.command(name='resume', description = HELP_RESUME_LONG, help = HELP_RESUME_SHORT)
    async def _resume(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        current_guild.voice_client.resume()

    @commands.command(name='vol', aliases = ["volume"], description = HELP_VOL_LONG, help = HELP_VOL_SHORT)
    async def _volume(self, ctx, volume):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return

        guild_to_audiocontroller[current_guild].volume = volume

    @commands.command(name='spotify', description = HELP_SPOTIFY_LONG, help = HELP_SPOTIFY_SHORT)
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

    @commands.command(name='songinfo', description = HELP_SONGINFO_LONG, help = HELP_SONGINFO_SHORT)
    async def _songinfo(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        songinfo = guild_to_audiocontroller[current_guild].current_songinfo
        if songinfo is None:
            return
        await ctx.message.author.send(songinfo.output)

    @commands.command(name='history', description = HELP_HISTORY_LONG, help = HELP_HISTORY_SHORT)
    async def _history(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)
        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        await send_message(ctx,guild_to_audiocontroller[current_guild].track_history())

def setup(bot):
    bot.add_cog(Music(bot))
