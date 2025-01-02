import discord
from discord.ext import commands
import apikey
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


# Set up intents
intents = discord.Intents.default()  # Default intents
intents.messages = True  # Explicitly enable message-related events (optional, depends on your use case)
intents.message_content = True  # Allows your bot to read message content
intents.members = True  # Allows your bot to access member-related events (optional, depends on your use case)

clients = commands.Bot(command_prefix = '/',intents=intents)


@clients.event
async def on_ready():
    print("Bot is ready")
    print("-------------")

@clients.command()
async def hello(ctx):
    await ctx.send("Hello, I'm here.")

welcome_channel_id = ''

@clients.command(pass_context=True)
async def welcome(ctx,channel:discord.TextChannel) -> str:
    # channel = clients.get_channel(channel)
    if channel:
        # await channel.connect
        await ctx.send(f"Welcome to {channel.mention}! The channel id is {channel.id}")
        global welcome_channel_id
        welcome_channel_id = channel.id
        return channel.id
    # else:
    await ctx.send(f"Channel {channel} not found!")
    return -1

# welcome_channel_id = welcome(clients, discord.TextChannel)

@clients.event
async def on_member_join(member):
    apikey.fetch_joke
    global welcome_channel_id
    channel = clients.get_channel(welcome_channel_id)  # Replace with your channel ID
    await channel.send(f"Welcome to the server, {member.mention}! Glad to see you here 🥰.")
    await channel.send(f"**{apikey.fetch_joke()}**")
    await channel.send(f"{member.mention}, did you like the joke?")


@clients.event
async def on_member_remove(member):
    channel = clients.get_channel(1313159077844619274)  # Replace with your channel ID
    await channel.send(f"{member.mention} has left or been removed!")

@clients.command(pass_context=True)
async def joinVoiceChat(ctx,channel:discord.VoiceChannel):
    # voice_channel = clients.get_channel(channel)
    if channel:
        await channel.connect()
        await ctx.send(f"Joined {channel}")

    else:
        await ctx.send("Voice channel not found!")


@clients.command()
async def leaveVoiceChat(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel.")


# def activate_bot():
clients.run(os.getenv('BOT_TOKEN'))
