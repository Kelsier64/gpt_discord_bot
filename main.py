from dotenv import load_dotenv
import os
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
load_dotenv()
dc_token = os.getenv("DISCORD_BOT_TOKEN") 

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
cogs = ["gpt"]

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")

# 卸載指令檔案
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded {extension} done.")

# 重新載入程式檔案
@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded {extension} done.")

if __name__ == "__main__":
	for cog in cogs:
		bot.load_extension(f"cogs.{cog}")
	bot.run(dc_token)