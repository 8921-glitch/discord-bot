import os
import discord
from discord.ext import commands, tasks
import feedparser

# Discord Token（從 Render / Railway Environment Variables 讀取）
TOKEN = os.getenv("TOKEN")

# Discord 頻道 ID
CHANNEL_ID = 1505035336659763210

# 想監控的 Twitter/X 帳號 RSS
RSS_URL = "https://x.com/LimbusCompany_B"

# Discord Intents
intents = discord.Intents.default()
intents.message_content = True

# 建立 Bot
bot = commands.Bot(command_prefix="!", intents=intents)

# 記錄最後一篇推文
last_link = None


@bot.event
async def on_ready():
    print(f"已登入：{bot.user}")

    # 啟動背景任務
    check_twitter.start()


@tasks.loop(minutes=1)
async def check_twitter():
    global last_link

    try:
        # 讀取 RSS
        feed = feedparser.parse(RSS_URL)

        # 沒資料就跳過
        if not feed.entries:
            return

        # 最新推文
        latest = feed.entries[0]

        # 第一次啟動時不發舊訊息
        if last_link is None:
            last_link = latest.link
            return

        # 有新推文
        if latest.link != last_link:

            last_link = latest.link

            # 取得 Discord 頻道
            channel = bot.get_channel(CHANNEL_ID)

            # 找不到頻道
            if channel is None:
                print("找不到 Discord 頻道")
                return

            # 發送訊息
            await channel.send(
                f"🐦 新推文！\n\n{latest.title}\n{latest.link}"
            )

            print("已發送新推文")

    except Exception as e:
        print(f"錯誤：{e}")


# 啟動 Bot
keep_alive()

bot.run(TOKEN)