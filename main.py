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
from db_connection import DB_Connection

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
    scheduler.add_job(send_ai_news, CronTrigger(hour=1, minute=2,  timezone='Asia/Tokyo'))
    # await send_ai_news()


#setup channel for a command.
async def set_command_channel(interaction, command: str):
    connection = DB_Connection()
    conn = connection.db_connect()
    if conn is None:
        # message = "❌ Failed to connect to the database."
        return False

    try:
        cursor = conn.cursor()

        # Fetch the internal server ID
        fetch_server_sql = "SELECT id FROM server WHERE guild_id = %s;"
        cursor.execute(fetch_server_sql, (interaction.guild.id,))
        server_result = cursor.fetchone()

        if server_result is None:
            # message = "❌ This server is not registered in the database."
            return False #, message

        # Explanation of `server_id = server_result[0]`
        # `cursor.fetchone()` returns a tuple, like (12,) — the first item is the internal 'id'
        server_id = server_result[0]

        insert_sql = '''
            INSERT INTO channel (channel_id, name, command, activator, join_date, server_id)
            VALUES (%s, %s, %s, %s, NOW(), %s)
            ON CONFLICT (channel_id)
            DO UPDATE SET
                name = EXCLUDED.name,
                command = EXCLUDED.command,
                activator = EXCLUDED.activator,
                join_date = EXCLUDED.join_date,
                remove_date = NULL,
                server_id = EXCLUDED.server_id;
        '''

        cursor.execute(
            insert_sql,
            (
                interaction.channel.id,
                interaction.channel.name,
                command,
                interaction.user.id,
                server_id
            )
        )

        conn.commit()
        # message = f"✅ Channel registered for `{command}` command!"
        return True #, message

    except Exception as e:
        await interaction.response.send_message(f"❌ Database error: {e}")

    finally:
        cursor.close()
        conn.close()


# AI news channel setup.
@clients.tree.command(name="news", description="Get the latest AI news!")
async def set_news_channel(interaction):
    if interaction.response.is_done():
        # Already responded somehow (possible duplicate trigger)
        return

    try:
        await interaction.response.defer(thinking=True) 

        success = await set_command_channel(interaction, 'news')

        # Safe follow-up only
        if success:
            await interaction.followup.send("📡 Got it! You'll receive AI updates in this channel.")
            
        else:
            await interaction.followup.send(f"❌ Channel didn't setup! 😭")
            

    except Exception as e:
        # Just in case there's an unexpected failure
        if not interaction.response.is_done():
            await interaction.response.send_message(f"⚠️ Error: {e}", ephemeral=True)
        else:
            await interaction.followup.send(f"⚠️ Error: {e}", ephemeral=True)


# Send AI news to defined channels.
async def send_ai_news():
    connection = DB_Connection()
    conn = connection.db_connect()
    if conn is None:
        print("Connection Faild! 😵‍💫")

    try:
        cursor = conn.cursor()

        # Fetch the internal server ID
        fetch_channel_sql = "SELECT channel_id FROM channel WHERE command = 'news';"
        cursor.execute(fetch_channel_sql)
        channel_result = cursor.fetchone()

        if channel_result:
            channel_ids = channel_result[0]
            channels = (channel_ids,)

        conn.commit()
        
    except Exception as e:
        print("Database connection Error! 😔")
    finally:
        cursor.close()
        conn.close()

    print(channels)
    for channel_id in channels:
        channel = clients.get_channel(channel_id)
        print(f"I am looking for latest ai news and share on Channel {channel}")
        news_content = get_ai_news()
        await channel.send(f"📰 **AI Trend Report**\n{news_content}")


#on join server
@clients.event
async def on_guild_join(guild):
    connection = DB_Connection()
    conn = connection.db_connect()
    # cursor = conn.cursor()
    
    sql = """
    INSERT INTO server (guild_id, name, join_date)
    VALUES (%s, %s, NOW())
    ON CONFLICT (guild_id)
    DO UPDATE SET name = EXCLUDED.name;
    """
    cursor = conn.cursor()
    cursor.execute(sql, (guild.id, guild.name))
    conn.commit()
    cursor.close()
    conn.close()

# on leave the server.
@clients.event
async def on_guild_remove(guild):
    connection = DB_Connection()
    conn = connection.db_connect()
    # cursor = conn.cursor()
    
    sql = """
    delete from server
    WHERE guild_id = %s;
    """
    cursor = conn.cursor()
    cursor.execute(sql, (guild.id,))
    conn.commit()
    cursor.close()
    conn.close()


# Welcoming new members on Server.
welcome_channel_id = ''

# @clients.command(pass_context=True)
# async def welcome(ctx,channel:discord.TextChannel) -> str:
#     # channel = clients.get_channel(channel)
#     if channel:
#         # await channel.connect
#         await ctx.send(f"Welcome to {channel.mention}! The channel id is {channel.id}")
#         global welcome_channel_id
#         welcome_channel_id = channel.id
#         return channel.id
#     # else:
#     await ctx.send(f"Channel {channel} not found!")
#     return -1
@clients.tree.command(name="welcome", description="Welcomes a new member with joke!")
async def welcome(interaction) -> str:
    if interaction.response.is_done():
        # Already responded somehow (possible duplicate trigger)
        return

    try:
        await interaction.response.defer(thinking=True) 

        success = await set_command_channel(interaction, 'welcome')

        # Safe follow-up only
        if success:
            await interaction.followup.send(f"✅ Welcome channel setup complete!")
            
        else:
            await interaction.followup.send(f"❌ Channel didn't setup! 😭")
            

    except Exception as e:
        # Just in case there's an unexpected failure
        if not interaction.response.is_done():
            await interaction.response.send_message(f"⚠️ Error: {e}", ephemeral=True)
        else:
            await interaction.followup.send(f"⚠️ Error: {e}", ephemeral=True)

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
async def memberLeaves(ctx,channel:discord.TextChannel) -> str:
    # channel = clients.get_channel(channel)
    if channel:
        # await channel.connect
        await ctx.send(f"Configuration completed on {channel.mention}! When a member leaves, it'll appear here {channel.id}")
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
if __name__ == '__main__':
    clients.run(os.getenv('BOT_TOKEN'))

