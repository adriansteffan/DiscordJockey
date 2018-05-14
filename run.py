import discord
from discord.ext import commands

from config.config import *
from musicbot.audiocontroller import AudioController
from musicbot.utils import guild_to_audiocontroller

"""
Backlog:

documentation:
    readme
    help

maybe:
    logging
    hide ffmpeg

"""

initial_extensions = ['musicbot.commands.music', 'musicbot.commands.general']
bot = commands.Bot(command_prefix="!", pm_help=True)

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            pass


@bot.event
async def on_ready():
    print('Starting the bot...')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=" Music, type !help "))

    for guild in bot.guilds:
        print(guild.name)
        await guild.me.edit(nick=DEFAULT_NICKNAME)
        try:
            await guild.voice_channels[0].connect()
        except:
            pass
        guild_to_audiocontroller[guild] = AudioController(bot, guild, DEFAULT_VOLUME)
    print('Startup complete!')


@bot.event
async def on_guild_join(guild):
    print(guild.name)
    guild_to_audiocontroller[guild] = AudioController(bot, guild, DEFAULT_VOLUME)
    try:
        await guild.voice_channels[0].connect()
    except:
        pass


bot.run(token, bot=True, reconnect=True)
