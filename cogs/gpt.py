import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import requests
import base64
from datetime import datetime
import pytz
from dotenv import load_dotenv
from openai import AzureOpenAI
import os

load_dotenv()
API_KEY = os.getenv("AZURE_OPENAI_API_KEY") 
RESOURCE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
deployment_name = "gpt4o"

client = AzureOpenAI(
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version = "2024-09-01-preview",
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)
def str_request(messages, max_tokens):
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.2
        )
        return response.choices[0].message.content
    except:
        return "error"

class Gpt(commands.Cog):
    guilds = [1270418744434491413,1156116900321960017,1292494291926777896]

    def __init__(self,bot):
        self.bot = bot
        self.gpt_state = True
        self.history = []
    @nextcord.slash_command(name="activate",description="activate the gpt",guild_ids=guilds)
    async def activate(self,interaction:Interaction):
        self.gpt_state = True
        await interaction.response.send_message("gpt is now activated")

    @nextcord.slash_command(name="deactivate",description="deactivate the gpt",guild_ids=guilds)
    async def deactivate(self,interaction:Interaction):
        self.gpt_state = False
        await interaction.response.send_message("gpt is now deactivated")
    
    @nextcord.slash_command(name="read",description="read message history",guild_ids=guilds)
    async def read(self,interaction:Interaction,limit:int):
        channel = interaction.channel
        self.history.clear()
        async for msg in channel.history(limit=limit):
            self.history.append(f"{msg.author}: {msg.content}")
        await interaction.response.send_message(f"read {limit} messages done")
        
    @nextcord.slash_command(name="clear",description="clear message history",guild_ids=guilds)
    async def clear(self,interaction:Interaction):
        self.history.clear()
        await interaction.response.send_message("cleared messages done")
    
    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        timestamp = message.created_at
        gmt_plus_8 = pytz.timezone('Asia/Taipei')
        timestamp = timestamp.astimezone(gmt_plus_8)
        time = f"{timestamp.date()}/{timestamp.hour}:{timestamp.minute}:{timestamp.second}"

        if message.author == self.bot.user or not self.gpt_state:
            return
        else:
            if message.attachments:
                if message.attachments[0].content_type.startswith("image"):
                    response = requests.get(message.attachments[0].url)
                    img = base64.b64encode(response.content).decode('utf-8')

                    msgs = [{"role": "user","content": [{"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{img}"}}]},
                            {"role": "user", "content": f"{message.author}: {message.content}"}]
                    self.history.append(f"{message.author}: {message.content}")
            else:
                msgs = [{"role": "system", "content": f"以下是對話歷史記錄:{self.history}"},{"role": "user", "content": f"以下是最新訊息： time:{time} author:{message.author} message:{message.content}"}]
                self.history.append(f"time:{time} author:{message.author} message:{message.content}")
            msgs.append({"role": "system", "content":"請回覆最新訊息"})
            reply = str_request(msgs, 500)
            self.history.append(f"me: {reply}")

            await message.channel.send(reply)
            

def setup(bot):
    bot.add_cog(Gpt(bot))
