from config.config import *

guild_to_audiocontroller = {}


def get_guild(bot, message):
    if not message.guild is None:
        return message.guild
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            if message.author in channel.members:
                return guild
    return None


async def send_message(ctx, message):
    await ctx.send("```\n" + message + "\n```")


async def connect_to_channel(guild, dest_channel_name, ctx, switch=False, default=True):
    for channel in guild.voice_channels:
        if str(channel.name).strip() == str(dest_channel_name).strip():
            if switch:
                try:
                    await guild.voice_client.disconnect()
                except:
                    await send_message(ctx, NOT_CONNECTED_MESSAGE)
            await channel.connect()
            return

    if default:
        try:
            await guild.voice_channels[0].connect()
        except:
            pass
    else:
        await send_message(ctx, CHANNEL_NOT_FOUND_MESSAGE + str(dest_channel_name))
