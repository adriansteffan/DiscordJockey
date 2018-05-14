from discord.ext import commands

from musicbot.audiocontroller import AudioController
from musicbot.utils import *


class General:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='connect', description = HELP_CONNECT_LONG, help = HELP_CONNECT_SHORT)
    async def _connect(self, ctx, *, dest_channel_name: str):
        current_guild = get_guild(self.bot, ctx.message)

        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return

        if guild_to_audiocontroller[current_guild] is None:
            guild_to_audiocontroller[current_guild] = AudioController(self.bot, current_guild, DEFAULT_VOLUME)
        await connect_to_channel(current_guild, dest_channel_name, ctx, switch=False, default=True)

    @commands.command(name='disconnect', description = HELP_DISCONNECT_LONG, help = HELP_DISCONNECT_SHORT)
    async def _disconnect(self, ctx):
        current_guild = get_guild(self.bot, ctx.message)

        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return
        await current_guild.voice_client.disconnect()

    @commands.command(name='cc', aliases=["changechannel"], description = HELP_CC_LONG, help = HELP_CC_SHORT)
    async def _changechannel(self, ctx, *, dest_channel_name: str):
        current_guild = get_guild(self.bot, ctx.message)

        if current_guild is None:
            await send_message(ctx, NO_GUILD_MESSAGE)
            return

        await connect_to_channel(current_guild, dest_channel_name, ctx, switch=True, default=False)

    @commands.command(name='addbot', description = HELP_ADDBOT_LONG, help = HELP_ADDBOT_SHORT)
    async def _addbot(self, ctx):
        await ctx.send(ADD_MESSAGE_1+str(self.bot.user.id)+ADD_MESSAGE_2)


def setup(bot):
    bot.add_cog(General(bot))
