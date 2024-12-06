import discord
from discord.ext import commands
import requests 

# Set up intents
intents = discord.Intents.default()  # Default intents
intents.messages = True  # Explicitly enable message-related events (optional, depends on your use case)
intents.message_content = True  # Allows your bot to read message content
intents.members = True  # Allows your bot to access member-related events (optional, depends on your use case)

clients = commands.Bot(command_prefix = '!',intents=intents)

@clients.event
async def on_ready():
    print("Bot is ready")
    print("-------------")

@clients.command()
async def hello(ctx):
    await ctx.send("Hello, I'm here.")


@clients.event
async def on_member_join(member):
    channel = clients.get_channel(1313061297880829974)  # Replace with your channel ID
    await channel.send(f"Welcome to the server, {member.mention}! Glad to see you here 🥰")


@clients.event
async def on_member_remove(member):
    channel = clients.get_channel(1313159077844619274)  # Replace with your channel ID
    await channel.send(f"{member.mention} has left or been removed!")


clients.run('BOT_Token')