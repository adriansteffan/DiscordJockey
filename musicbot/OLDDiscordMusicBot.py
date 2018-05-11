import discord
import asyncio
import youtube_dl
from pathlib import Path
import urllib.request
import shutil
import datetime
import collections
from bs4 import BeautifulSoup as bs
import socket
import sys
import random
import praw
import reddit_config
from pynput.keyboard import Key,Listener
import os


with open('Misc/meme_blacklist_fr.txt') as f:
    blacklist = f.read().splitlines()
                
with open('Misc/fr_config.txt') as f:
    config = f.read().splitlines()

serverID = config[0].split(':')[1]
textID = config[1].split(':')[1]
voiceID = config[2].split(':')[1]
token = config[3].split(':')[1]

general_volume = 0.10
general_meme_volume = 0.4
join_meme_active = True

client = discord.Client()
discord.opus.load_opus('opus/libopus-0')

memelist = collections.deque()
playlist = collections.deque()
prev_songs = collections.deque()

i=0 # bugfix for coroutine in next_song
j=0

r = praw.Reddit(username = reddit_config.username,
                password = reddit_config.password,
                client_id = reddit_config.client_id,
                client_secret = reddit_config.client_secret,
                user_agent = "Meme DJ")

async def find_dank_meme(reddit_login):
    submissions = []
    for meme in reddit_login.subreddit("dankmemes").hot(limit=30):
        submissions.append(meme)
    meme_number = random.randrange(3,30)
    print(submissions[meme_number].url)
    await client.send_message(client.get_channel(textID),submissions[meme_number].url)

def create_memelist():
    xmemelist = collections.deque()
    with open('Misc/memes.txt') as f:
        
        memelist_raw = f.read().splitlines()
    random.shuffle(memelist_raw)
    for meme in memelist_raw:
                if meme.startswith('!') and meme not in blacklist:
                    xmemelist.append(meme)
    return xmemelist
                    
async def play_yt(link):
    global player
    
    try:
        if not player.is_playing():
            if len(playlist) == 0:
                playlist.append(link)
            try:
                player = await client.voice_client_in(client.get_server(serverID)).create_ytdl_player(playlist[0],ytdl_options={'noplaylist' : True},after=next_song)
                print('\n')
                player.volume = general_volume
                player.start()
                prev_songs.append(playlist[0])
                playlist.popleft()
            except:
                print('youtbe Error...')
                playlist.popleft()
                player.stop()
        else:
            playlist.append(link)
        
    except NameError:
        playlist.append(link)
        try:
            player = await client.voice_client_in(client.get_server(serverID)).create_ytdl_player(playlist[0],ytdl_options={'noplaylist' : True},after=next_song)
            print('\n')
            player.volume = general_volume
            player.start()
        except:
            print('youtbe Error...')
            playlist.popleft()
        try:
            prev_songs.append(playlist[0])
            playlist.popleft()
        except IndexError:
            pass

        
def next_song():
    try:
        coro = play_yt(playlist[0])
        fut[i] = asyncio.run_coroutine_threadsafe(coro, client.loop)
        try:
            fut[i].result()
            i = i+1
        except:
            pass
    except IndexError:
        pass

async def play_clip(clip):
    global player
    player = client.voice_client_in(client.get_server(serverID)).create_ffmpeg_player(clip,after=next_meme)
    player.volume = general_meme_volume
    print(general_meme_volume)
    player.start()
    if len(memelist) != 0:
        memelist.popleft()
    
async def play_meme(command):
    global player
    memename = command.strip('!')
    meme = 'MusicFiles/Clips/'+memename+'.mp3'
    if Path(meme).is_file(): 
        try:
            if not player.is_playing():
                await play_clip(meme)

        # If there is no player, create one
        except NameError:
            await play_clip(meme)

def next_meme():
    try:
        print(memelist[0])
        coro = play_meme(memelist[0])
        fut[j] = asyncio.run_coroutine_threadsafe(coro, client.loop)
        try:
            fut[j].result()
            j = j+1
        except:
            pass
    except IndexError:
        pass

async def random_meme():
    random = create_memelist()[0]
    await play_meme(random)

async def autodj(genre,author):
    pass
    
    
async def player_interaction(interaction,author):
        try:
            
            if interaction == 'stop':
                    playlist.clear()
                    memelist.clear()
                    print(general_meme_volume)
                    
            if player.is_playing():
                if interaction == 'pause':
                    player.pause()
                elif interaction == 'skip' or interaction == 'stop':
                    player.stop()
                elif interaction == 'prev':
                    try:
                        playlist.appendleft(prev_songs.pop())
                        playlist.appendleft(prev_songs.pop())
                        player.stop()
                    except:
                        pass
            else:

                if interaction == 'resume':
                    player.resume()
    
                elif interaction == 'skip' or interaction == 'stop':
                    
                    # Fixing a laggy noise of the ffmpeg player when stopping
                    volume_holder = player.volume
                    player.volume = 0
                    player.resume()
                    player.stop()
                    player.volume = volume_holder
                    print(general_meme_volume)
                    
                elif interaction == 'prev':
                    try:
                        playlist.appendleft(prev_songs.pop())
                        player.stop()
                    except:
                        pass
                    
                
                    
        except NameError:
            await client.send_message(author,'Error: There is no player playing at the moment')


async def my_background_task():
    open('hotkeymeme.txt', 'w').close()
    await client.wait_until_ready()
    while not client.is_closed:
        await asyncio.sleep(0.25)
        if os.stat('hotkeymeme.txt').st_size > 0:
            f = open('hotkeymeme.txt','r')
            newmeme = f.read().splitlines()[0]
            f.close()
            await play_meme(newmeme)
            open('hotkeymeme.txt', 'w').close()
            
        
    
@client.event
async def on_ready():
    global voice
    print('\n')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print('Opus Loaded: ' + str(discord.opus.is_loaded())+'\n')
    await client.join_voice_channel(client.get_channel(voiceID))
    await client.change_status(discord.Game(name='!commands'))
    print('\n')
    
    

@client.event
async def on_voice_state_update(before, after):
    if before.voice.voice_channel is None and after.voice.voice_channel is not None and after != client.user.id:
        if join_meme_active:
            await random_meme()
    
@client.event
async def on_message(message):
    global general_meme_volume
    global general_volume
    global memelist
    global join_meme_active
    global r
    author = message.author
    now = datetime.datetime.now()
    
    if message.channel == client.get_channel(textID) or message.channel.is_private:
        
        # Logging command and time/date
        
        if str(author) != 'Musicus Botus 1.0#3974' and message.content.startswith('!'):
            f = open('Logs/'+str(now.day)+'-'+str(now.month)+'-'+str(now.year)+'.txt','a')
            f.write('\n('+ str(now.hour)+':'+str(now.minute)+':'+str(now.second)+') '+str(author)+' - '+message.content)
            f.close()
            print('('+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+') '+str(author)+' - '+message.content)
            
        if message.content.lower().startswith('!commands'):
            await client.send_typing(author)
            await client.send_message(author,open('Misc/commands.txt').read())
            
        elif message.content.lower().startswith('!memes'):############
            await client.send_typing(author)
            await client.send_message(author,open('Misc/memes.txt').read())
            
        elif message.content.lower().startswith('!log'):
            await client.send_typing(author)
            date = message.content.replace('!log ','')
            path = 'Logs/'+date+'.txt'
            if Path(path).is_file():
                await client.send_message(author,open(path).read())
            else:
                await client.send_message(author,'Error: no such log found')
                
        elif message.content.lower().startswith('!connect'):
            await client.join_voice_channel(client.get_channel(voiceID))
        elif message.content.lower().startswith('!disconnect'):
            if client.is_voice_connected(client.get_server(serverID)):
                await client.voice_client_in(client.get_server(serverID)).disconnect()
                
        elif message.content.lower().startswith('!yt'):
            link = message.content.strip('!yt ')

            if not 'playlist?list=' in link:
                await play_yt(link)
                
            else:
                r = urllib.request.urlopen(link)
                content =  r.read().decode(r.headers.get_content_charset())

                soup = bs(content,'html.parser')
                res = soup.find_all('a',{'class':'pl-video-title-link'})

                for l in res:
                    
                    watchlink = l.get("href")
                    watchlink = watchlink.split('&')[0]
                    playlist.append('https://www.youtube.com'+watchlink)
                await play_yt(playlist[0])


        elif message.content.lower().startswith('!*'):
            memelist = create_memelist()
            memelist.appendleft("!memecountdown")
            await play_meme(memelist[0])
            
        elif message.content.lower().startswith('!random'):
            await random_meme()
            
        elif message.content.lower().startswith('!postmeme'):
            await find_dank_meme(r)

        elif message.content.lower().startswith('autodj'):
            pass
            await autodj(message.content.lower().strip('!autodj '),author)
            
        elif message.content.lower().startswith('!joinmeme'):
            argument = message.content.lower().strip('!joinmeme ')
            if argument.lower() == 'on':
                join_meme_active = True
            elif argument.lower() == 'off':
                join_meme_active = False
            else:
                join_meme_active = not join_meme_active

            await client.send_message(author,'Meme on join: ' + str(join_meme_active))
            
        elif message.content.lower().startswith('!pause'):
            await player_interaction('pause',author)
                
        elif message.content.lower().startswith('!stop'):
            await player_interaction('stop',author)
            
        elif message.content.lower().startswith('!skip'):
            await player_interaction('skip',author)

        elif message.content.lower().startswith('!prev'):
            await player_interaction('prev',author)
                
        elif message.content.lower().startswith('!play') or message.content.startswith('!resume'):
            await player_interaction('resume',author)
            
        elif message.content.lower().startswith('!volume') or message.content.lower().startswith('!vol'):

            if float(message.content.strip('!volume ')) > 130:
                general_volume = 1.30
            else:
                general_volume = float(message.content.strip('!volume '))/100
            try:
                player.volume = general_volume
            except:
                pass
        elif message.content.lower().startswith('!memevolume') or message.content.lower().startswith('!memevol'):

            if float(message.content.strip('!volume ')) > 130:
                general_meme_volume = 1.30
            else:
                general_meme_volume = float(message.content.strip('!memevolume '))/100
            try:
                player.volume = general_meme_volume
            except:
                pass
            

        # Handling the upload of new memes by users
        
        elif message.content.lower().startswith('!uploadinfo'):
            await client.send_message(author,'To upload a meme, send it to the bot and add - !upload *name* - as a comment. You can access the new meme as usual')
            
        elif message.content.lower().startswith('!upload'):
            
            if message.attachments[0]['filename'].endswith('.mp3') or message.attachments[0]['filename'].endswith('.mp4') or message.attachments[0]['filename'].endswith('.wav'):
                name =  message.content.replace('!upload ','')
                location = 'MusicFiles/Clips/'+name+'.mp3'
                locationtext = 'Misc/memes.txt'
                    
                if not Path(location).is_file():    
                    r = urllib.request.Request(message.attachments[0]['url'])
                    r.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
                    url = urllib.request.urlopen(r)
                    output = open(location,'wb')
                    output.write(url.read())
                    output.close()
                    textfile = open(locationtext,'a')
                    textfile.write('\n!'+ name)
                    textfile.close()
                        
                else:
                    await client.send_message(author,'Error: already a file with that name')
            else:
                await client.send_message(author,'Error: file must be .mp3,.mp4 or .wav')
 
                
        elif message.content.startswith('!'):
            await play_meme(message.content)



client.loop.create_task(my_background_task())
client.run(token)

