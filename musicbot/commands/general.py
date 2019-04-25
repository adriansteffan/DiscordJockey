from discord.ext import commands

from config import config
from musicbot import utils
from musicbot.audiocontroller import AudioController


class General(commands.Cog):
    """ A collection of the commands for moving the bot around in you server.

            Attributes:
                bot: The instance of the bot that is executing the commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='connect', description=config.HELP_CONNECT_LONG, help=config.HELP_CONNECT_SHORT)
    async def _connect(self, ctx, *, dest_channel_name: str):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return

        if utils.guild_to_audiocontroller[current_guild] is None:
            utils.guild_to_audiocontroller[current_guild] = AudioController(self.bot, current_guild,
                                                                            config.DEFAULT_VOLUME)
        await utils.connect_to_channel(current_guild, dest_channel_name, ctx, switch=False, default=True)

    @commands.command(name='disconnect', description=config.HELP_DISCONNECT_LONG, help=config.HELP_DISCONNECT_SHORT)
    async def _disconnect(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await current_guild.voice_client.disconnect()

    @commands.command(name='cc', aliases=["changechannel"], description=config.HELP_CC_LONG, help=config.HELP_CC_SHORT)
    async def _changechannel(self, ctx, *, dest_channel_name: str):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return

        await utils.connect_to_channel(current_guild, dest_channel_name, ctx, switch=True, default=False)

    @commands.command(name='addbot', description=config.HELP_ADDBOT_LONG, help=config.HELP_ADDBOT_SHORT)
    async def _addbot(self, ctx):
        await ctx.send(config.ADD_MESSAGE_1 + str(self.bot.user.id) + config.ADD_MESSAGE_2)


def setup(bot):
    bot.add_cog(General(bot))
