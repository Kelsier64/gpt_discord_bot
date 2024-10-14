from dotenv import load_dotenv
import os
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from flask import Flask
import asyncio

load_dotenv()
dc_token = os.getenv("DISCORD_BOT_TOKEN")

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")

cogs = ["gpt"]

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded {extension} done.")

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded {extension} done.")

async def run_discord_bot():
    for cog in cogs:
        bot.load_extension(f"cogs.{cog}")
    await bot.start(dc_token)

def run_flask_app():
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, run_flask_app)  # Run Flask in a background thread
    loop.run_until_complete(run_discord_bot())  # Run the Discord bot
