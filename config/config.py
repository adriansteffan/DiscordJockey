token: str = "NDQ0ODA4NjMyNzA2NjYyNDAw.DdhXTw.TgIgkWS6qsdeNSECFqsj1Zo8vCM"
DEFAULT_NICKNAME = "{DiscordJockey}"

NO_GUILD_MESSAGE = 'Warining: Please join a voice channel or enter the command in guild chat'
NOT_CONNECTED_MESSAGE = "Error: Bot not connected to any voice channel"
CHANNEL_NOT_FOUND_MESSAGE = "Error: Could not find channel "

ADD_MESSAGE_1 = "```To add this bot to your own Server, click the following link:```\n <https://discordapp.com/oauth2/authorize?client_id="
ADD_MESSAGE_2 = "&scope=bot>"

INVALID_INVITE_MESSAGE = "Error: Invalid invitation link"

INFO_HISTORY_TITLE = "Songs Played:"

DEFAULT_VOLUME = 7

MAX_HISTORY_LENGTH = 10
MAX_TRACKNAME_HISTORY_LENGTH = 15

SONGINFO_UPLOADER = "Uploader: "
SONGINFO_DURATION = "Duration: "
SONGINFO_SECONDS = "s"
SONGINFO_LIKES = "Likes: "
SONGINFO_DISLIKES = "Dislikes: "

HELP_ADDBOT_SHORT = "Add Bot to another server"
HELP_ADDBOT_LONG = "Gives you the link for adding this bot to another server of yours."
HELP_CC_SHORT = "Change voicechannel"
HELP_CC_LONG = "Switches the bot to another voicechannel."
HELP_CONNECT_SHORT = "Connect bot to voicechannel"
HELP_CONNECT_LONG = ""
HELP_DISCONNECT_SHORT = "Connect bot from voicechannel"
HELP_DISCONNECT_LONG = ""

HELP_HISTORY_SHORT = "Show history of songs"
HELP_HISTORY_LONG = "Shows the " + str(MAX_TRACKNAME_HISTORY_LENGTH) + " last played songs."
HELP_PAUSE_SHORT = "Pause Music"
HELP_PAUSE_LONG = "Pauses the AudioPlayer. Playback can be continued with the resume command."
HELP_PREV_SHORT = "Go back one Song"
HELP_PREV_LONG = "Plays the previous song again."
HELP_RESUME_SHORT = "Resume Music"
HELP_RESUME_LONG = "Resumes the AudioPlayer."
HELP_SKIP_SHORT = "Skip a song"
HELP_SKIP_LONG = "Skips the currently playing song and goes to the next item in the queue."
HELP_SONGINFO_SHORT = "Info about current Song"
HELP_SONGINFO_LONG = "Shows details about the song currently being played and posts a link to the song."
HELP_SPOTIFY_SHORT = "Play song from Spotify"
HELP_SPOTIFY_LONG = ("Gives you an easy way to share a song from Spotify via the bot.\n\n"
                     "!!!Spotify needs to be linked to your Discord account for this to work.!!!\n"
                     "The command takes the song that is being played by your Spotify client and plays it on the bot via Youtube.\n"
                     "You can target another users client by specifying his nickname as an argument.\n\n"
                     "The song needs to be playing for the command to launch, so you need to listen for the first few seconds of the song while the bot loads it up.\n"
                     "If the player is already playing, the command adds the song to the playingqueue.\n\n"
                     "(The bot is not 100% accurate and plays slightly different versions of the songs every now and then.)")
HELP_STOP_SHORT = "Stop Music"
HELP_STOP_LONG = "Stops the AudioPlayer and clears the songqueue"
HELP_VOL_SHORT = "Change volume %"
HELP_VOL_LONG = "Changes the volume of the AudioPlayer. Argument specifies the % to which the volume should be set."
HELP_YT_SHORT = "Play song from Youtube"
HELP_YT_LONG = ("Plays the audio of a Youtube video. Argument can either be:\n"
                "  - A link to the video (https://ww...)\n"
                "  - The title of a video (Rick Astley - Never Gonna Give You Up)\n" 
                "  - Keywords for a search(lofi hip-hop) -> the bot plays the first result)\n"
                "  - A link to a playlist -> the bot will play the songs one after another\n"
                "If the player is already playing, the command adds the song to the playingqueue")
