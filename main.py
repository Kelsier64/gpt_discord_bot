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

client = commands.Bot(command_prefix='$', intents=intents)

@client.event
async def on_ready():
    print("bot is ready")

if __name__ == "__main__":
	cogs = []
	for cog in cogs:
		client.load_extension(f"cogs.{cog}")

	client.run(dc_token)