import discord
from discord.ext import commands
import youtube_dl
import asyncio


with open('config/config.txt') as f:
    config = f.read().splitlines()
    
serverID = config[0].split(':')[1]
textID = config[1].split(':')[1]
voiceID = config[2].split(':')[1]
token = config[3].split(':')[1]


bot = commands.Bot(command_prefix="!")
no_guild_message = 'Please join a voice channel or enter the command in guild chat'

# gets the guild from a message
def get_guild(message):
    if not message.guild is None:
        return message.guild
    for guild in bot.guilds:
        for channel in guild.channels:
            if channel.category != None and (channel.category.name == "Voice Channels" or channel.category.name == "Sprach-Kanäle") and message.author in channel.members:
                return guild
    return None

@bot.event
async def on_ready():
    
    print('Starting the bot...')
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(name=" Music, type !commands "))
    await bot.get_channel(int(voiceID)).connect()
    await bot.get_channel(444809976435965965).connect()
    for guild in bot.guilds:
        print(guild.voice_client)
        print(guild.name)
    print('Startup complete!')
    

@bot.command(name='commands')
async def _commands(ctx):
    await ctx.send('Coming Soon')

@bot.command(name='connect')
async def _connect(ctx):
    await ctx.send('Coming Soon')

@bot.command(name='disconnect')
async def _disconnect(ctx):
    await ctx.send('Coming Soon')
    

@bot.command(name='yt')
async def _play_youtube(ctx,youtube_link):

    current_guild = get_guild(ctx.message)
    
    if current_guild is None:
        await ctx.send(no_guild_message)
        return
    
    downloader = youtube_dl.YoutubeDL({'format': 'bestaudio','title':True})
    extracted_info = downloader.extract_info(youtube_link, download=False)
    new_nick = ("[" +extracted_info.get('title').split("(")[0])[0:29]+"]"
    await current_guild.me.edit(nick=new_nick)
    current_guild.voice_client.play(discord.FFmpegPCMAudio(extracted_info['url']), after=None)
    current_guild.voice_client.source = discord.PCMVolumeTransformer(current_guild.voice_client.source)


@bot.command(name='pause')
async def _pause(ctx):
    current_guild = get_guild(ctx.message)
    if current_guild is None:
        await ctx.send(no_guild_message)
        return
    current_guild.voice_client.pause()

@bot.command(name='stop')
async def _stop(ctx):
    current_guild = get_guild(ctx.message)
    if current_guild is None:
        await ctx.send(no_guild_message)
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
        await ctx.send(no_guild_message)
        return
    current_guild.voice_client.resume()

@bot.command(name='vol')
async def _volume(ctx,volume):
    current_guild = get_guild(ctx.message)
    if current_guild is None:
        await ctx.send(no_guild_message)
        return
    
    current_guild.voice_client.source.volume = float(volume)/100.0
    

@bot.command(name='clipvolume')
async def _clipvolume(ctx):
    await ctx.send('Coming Soon')

@bot.command(name='uploadinfo')
async def _uploadinfo(ctx):
    await ctx.send('Coming Soon')

@bot.command(name='upload')
async def _upload(ctx):
    await ctx.send('Coming Soon')

###Clip functionality
###Playlist fucntionality + change name back
### Change Voice Channel
###config file
### hide ffmpeg
### spotify 
    
bot.run(token)
