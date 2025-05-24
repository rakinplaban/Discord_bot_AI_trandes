import discord
from discord.ext import commands
import apikey
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import feedparser
import requests
from bs4 import BeautifulSoup as bfsoup
import os
from dotenv import load_dotenv
import json

load_dotenv()


# Set up intents
intents = discord.Intents.default()  # Default intents
intents.messages = True  # Explicitly enable message-related events (optional, depends on your use case)
intents.message_content = True  # Allows your bot to read message content
intents.members = True  # Allows your bot to access member-related events (optional, depends on your use case)

clients = commands.Bot(command_prefix = '/',intents=intents)

scheduler = AsyncIOScheduler()


def get_ai_news():
    seen_titles = set()
    news_items = []

    def add_entry(title, link, source_emoji):
        if title not in seen_titles:
            seen_titles.add(title)
            news_items.append(f"{source_emoji} **{title}**\n🔗 {link}")

    # --- MarkTechPost AI ---
    try:
        feed = feedparser.parse("https://www.marktechpost.com/category/artificial-intelligence/feed/")
        for entry in feed.entries[:3]:
            title = entry.title
            link = entry.link
            add_entry(title, link, "🧠")
            # news_items.append(f"🧠 **{title}**\n🔗 {link}")
    except Exception as e:
        news_items.append(f"⚠️ MarkTechPost error: {e}")


    # --- arXiv AI ---
    try:
        feed = feedparser.parse("http://export.arxiv.org/rss/cs.AI")
        for entry in feed.entries[:3]:
            title = entry.title
            link = entry.link
            # news_items.append(f"📚 **{title}**\n🔗 {link}")
            add_entry(title, link, "📚")
    except Exception as e:
        news_items.append(f"⚠️ arXiv error: {e}")

    # --- Hugging Face Blog (no feed, fallback to scrape or skip) ---
    try:
        res = requests.get("https://huggingface.co/blog")
        soup = bfsoup(res.text, "html.parser")
        posts = soup.select("a[href^='/blog/']")[:2]
        for a in posts:
            title = a.text.strip()
            link = "https://huggingface.co" + a["href"]
            if title:
                add_entry(title, link, "🤗")
                # news_items.append(f"🤗 **{title}**\n🔗 {link}")
    except Exception as e:
        news_items.append(f"⚠️ HuggingFace error: {e}")

    return "\n\n".join(news_items) if news_items else "No fresh AI news today."


@clients.event
async def on_ready():
    print(f"Logged in as {clients.user}")
    try:
        synced = await clients.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print("Command sync failed:", e)
    scheduler.start()
    scheduler.add_job(send_ai_news, CronTrigger(hour=0, minute=0,  timezone='Asia/Tokyo'))
    # await send_ai_news()


CHANNEL_FILE = "channels.json"

# Load saved channels
def load_channels():
    try:
        with open(CHANNEL_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Save channels
def save_channels(data):
    with open(CHANNEL_FILE, "w") as f:
        json.dump(data, f)

channels = load_channels()

@clients.command()
async def set_news_channel(ctx):
    user_id = str(ctx.author.id)
    channel_id = ctx.channel.id
    channels[user_id] = channel_id
    save_channels(channels)
    await ctx.send(f"📡 Got it! You'll receive AI updates in this channel.")

async def send_ai_news():

    for usr_id, channel_id in channels.items():
        channel = clients.get_channel(channel_id)
        print(f"I am looking for latest ai news and share on Channel {channel}")
        news_content = get_ai_news()
        await channel.send(f"📰 **AI Trend Report**\n{news_content}")


# Welcoming new members on Server.
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


good_bye = ''

@clients.command(pass_context=True)
async def welcome(ctx,channel:discord.TextChannel) -> str:
    # channel = clients.get_channel(channel)
    if channel:
        # await channel.connect
        await ctx.send(f"Welcome to {channel.mention}! The channel id is {channel.id}")
        global good_bye
        good_bye = channel.id
        return channel.id
    # else:
    await ctx.send(f"Channel {channel} not found!")
    return -1


@clients.event
async def on_member_remove(member):
    apikey.fetch_joke
    global good_bye
    channel = clients.get_channel(good_bye)  # Replace with your channel ID
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
