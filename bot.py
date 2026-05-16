import os
import discord
from discord.ext import commands, tasks
import feedparser

TOKEN = os.getenv("TOKEN")

CHANNEL_ID = 1505035336659763210

RSS_URL = "https://nitter.net/OpenAI/rss"

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

last_link = ""

@bot.event
async def on_ready():
    print(f"已登入：{bot.user}")
    check_twitter.start()

@tasks.loop(minutes=1)
async def check_twitter():
    global last_link

    feed = feedparser.parse(RSS_URL)

    if feed.entries:

        latest = feed.entries[0]

        if latest.link != last_link:

            last_link = latest.link

            channel = bot.get_channel(CHANNEL_ID)

            await channel.send(
                f"新推文！\n{latest.title}\n{latest.link}"
            )

bot.run(TOKEN)