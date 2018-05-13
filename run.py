import discord
from discord.ext import commands
import youtube_dl
import asyncio
from collections import deque


"""
Backlog:

core:
    Playlist fucntionality + change name back
    on guild join event

music integration:
    spotify
    Song info

cleanup:
    split files
    hide ffmpeg

documentation:
    readme
    help


"""

token = "NDQ0ODA4NjMyNzA2NjYyNDAw.DdhXTw.TgIgkWS6qsdeNSECFqsj1Zo8vCM"
DEFAULT_NICKNAME = "{DiscordJockey}"
NO_GUILD_MESSAGE = 'Warining: Please join a voice channel or enter the command in guild chat'
NOT_CONNECTED_MESSAGE = "Error: Bot not connected to any voice channel"
CHANNEL_NOT_FOUND_MESSAGE = "Error: Could not find channel "


class AudioController:
    
    def __init__(self,guild,volume):
        self._volume = volume
        self.playlist = Playlist()
        self.current_songinfo = None
        self.guild = guild

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        try:
            self.guild.voice_client.source.volume = float(value)/100.0
        except:
            pass

    def next_song(self):
        pass

    def add_song(self):
       pass

    async def play_youtube(self,youtube_link):

        ##fix it
        try:
            downloader = youtube_dl.YoutubeDL({'format': 'bestaudio','title':True})
            extracted_info = downloader.extract_info(youtube_link, download=False)
        except:
            downloader = youtube_dl.YoutubeDL({})
            extracted_info = downloader.extract_info(youtube_link, download=False)
    
        new_nick = ("[" +extracted_info.get('title').split("(")[0])[0:29]+ "]"
        await self.guild.me.edit(nick=new_nick)
    
        self.guild.voice_client.play(discord.FFmpegPCMAudio(extracted_info['url']), after = self.next_song())
        self.guild.voice_client.source = discord.PCMVolumeTransformer(self.guild.voice_client.source)
        self.guild.voice_client.source.volume = float(self.volume)/100.0

    
class Playlist:

    MAX_HISTORY_LENGTH = 10
    
    def __init__(self):
        self.playque = deque()
        self.playhistory = deque()
    




bot = commands.Bot(command_prefix="!",pm_help=True)


guild_to_audiocontroller = {}

# gets the guild from a message
def get_guild(message):
    if not message.guild is None:
        return message.guild
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            if message.author in channel.members:
                return guild
    return None

async def send_message(ctx,message):
    await ctx.send("```\n"+message+"\n```")

async def connect_to_channel(guild,dest_channel_name,ctx,switch = False,default = True):
    for channel in guild.voice_channels:
        if str(channel.name).strip() == str(dest_channel_name).strip():
            if switch:
                try:
                    await guild.voice_client.disconnect()
                except:
                    await send_message(ctx,NOT_CONNECTED_MESSAGE)
            await channel.connect()
            return

    if default:      
        try:
            await guild.voice_channels[0].connect()
        except:
            pass
    else:
        await send_message(ctx,CHANNEL_NOT_FOUND_MESSAGE +str(dest_channel_name))

        

@bot.event
async def on_ready():
    
    print('Starting the bot...')
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(name=" Music, type !help "))
    
    for guild in bot.guilds:
        print(guild.name)
        await guild.me.edit(nick=DEFAULT_NICKNAME)
        try:
            await guild.voice_channels[0].connect()
        except:
            pass
        guild_to_audiocontroller[guild] = AudioController(guild,10)
    print('Startup complete!')

@bot.event
async def on_guild_join(guild):
    pass
    

    
@bot.command(name='connect')
async def _connect(ctx ,*args):
    current_guild = get_guild(ctx.message)
    
    if current_guild is None:
        await send_message(ctx,NO_GUILD_MESSAGE)
        return
    
    dest_channel_name = " ".join(args)
    await connect_to_channel(current_guild,dest_channel_name,ctx,switch = False,default = True)
    

@bot.command(name='disconnect')
async def _disconnect(ctx):
    current_guild = get_guild(ctx.message)
    
    if current_guild is None:
        await send_message(ctx,NO_GUILD_MESSAGE)
        return
    await current_guild.voice_client.disconnect()

@bot.command(name='cc',aliases=["changechannel"])
async def _connect(ctx ,*args):
    current_guild = get_guild(ctx.message)
    
    if current_guild is None:
        await send_message(ctx,NO_GUILD_MESSAGE)
        return
    
    dest_channel_name = " ".join(args)
    await connect_to_channel(current_guild,dest_channel_name,ctx,switch = True,default = False)

@bot.command(name='yt')
async def _play_youtube(ctx,youtube_link):

    current_guild = get_guild(ctx.message)
    
    if current_guild is None:
        await send_message(ctx,NO_GUILD_MESSAGE)
        return
    audiocontroller = guild_to_audiocontroller[current_guild]
    await audiocontroller.play_youtube(youtube_link)


@bot.command(name='pause')
async def _pause(ctx):
    current_guild = get_guild(ctx.message)
    if current_guild is None:
        await send_message(ctx,NO_GUILD_MESSAGE)
        return
    current_guild.voice_client.pause()

@bot.command(name='stop')
async def _stop(ctx):
    current_guild = get_guild(ctx.message)
    if current_guild is None:
        await send_message(ctx,NO_GUILD_MESSAGE)
        return
    current_guild.voice_client.stop()
    
@bot.command(name='skip')
async def _skip(ctx):
    await ctx.send('Coming Soon')

@bot.command(name='prev')
async def _prev(ctx):
    await ctx.send('Coming Soon')
    
@bot.command(name='resume')
async def _resume(ctx):
    current_guild = get_guild(ctx.message)
    if current_guild is None:
        await send_message(ctx,NO_GUILD_MESSAGE)
        return
    current_guild.voice_client.resume()

@bot.command(name='vol')
async def _volume(ctx,volume):
    current_guild = get_guild(ctx.message)
    if current_guild is None:
        await send_message(ctx,NO_GUILD_MESSAGE)
        return

    guild_to_audiocontroller[current_guild].volume = volume
    
    
bot.run(token)
