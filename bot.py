import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from mcstatus import JavaServer
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
MC_ADDRESS = os.getenv("MC_ADDRESS")

if not all([DISCORD_TOKEN, CHANNEL_ID, MC_ADDRESS]):
    print("⚠️ 請確認 .env 檔案的 DISCORD_TOKEN、CHANNEL_ID、MC_ADDRESS 都有正確設定！")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def send_status():
    channel = bot.get_channel(int(CHANNEL_ID))
    if not channel:
        print(f"⚠️ 找不到頻道 ID {CHANNEL_ID}")
        return

    try:
        server = JavaServer.lookup(MC_ADDRESS)
        status = await asyncio.get_event_loop().run_in_executor(None, server.status)

        embed = discord.Embed(title="🟢 Minecraft Server Status", color=0x00ff00)
        embed.add_field(name="延遲", value=f"{status.latency:.1f} ms", inline=True)
        embed.add_field(name="人數", value=f"{status.players.online}/{status.players.max}", inline=True)
    except Exception as e:
        embed = discord.Embed(title="🔴 Minecraft Server Status", description=str(e), color=0xff0000)

    await channel.send(embed=embed)

@bot.event
async def on_ready():
    print(f"✅ Discord Bot 啟動成功！登入帳號：{bot.user}")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_status, "interval", minutes=5)
    scheduler.start()

@bot.command(name="status")
async def manual_status(ctx):
    try:
        server = JavaServer.lookup(MC_ADDRESS)
        status = server.status()

        embed = discord.Embed(title="🟢 Minecraft Server Status", color=0x00ff00)
        embed.add_field(name="延遲", value=f"{status.latency:.1f} ms", inline=True)
        embed.add_field(name="人數", value=f"{status.players.online}/{status.players.max}", inline=True)
    except Exception as e:
        embed = discord.Embed(title="🔴 Minecraft Server Status", description=str(e), color=0xff0000)

    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
