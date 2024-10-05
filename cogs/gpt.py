import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import openai_api
import requests
import base64
class Gpt(commands.Cog):
    gpt_state = True
    history = []

    def __init__(self,bot):
        self.bot = bot

    @nextcord.slash_command(name="activate",description="activate the gpt")
    async def activate(self,interaction:Interaction):
        self.gpt_state = True
        await interaction.response.send_message("gpt is now activated")

    @nextcord.slash_command(name="deactivate",description="deactivate the gpt")
    async def deactivate(self,interaction:Interaction):
        self.gpt_state = False
        await interaction.response.send_message("gpt is now deactivated")
    
    @nextcord.slash_command(name="read",description="read message history")
    async def read(self,interaction:Interaction,limit:int):
        channel = interaction.channel
        self.history.clear()
        async for msg in channel.history(limit=limit):
            self.history.append(f"{msg.author}: {msg.content}")
        await interaction.response.send_message(f"read {limit} messages done")
        
    @nextcord.slash_command(name="clear",description="clear message history")
    async def clear(self,interaction:Interaction):
        self.history.clear()
        await interaction.response.send_message("cleared messages done")
    
    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
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
                msgs = [{"role": "system", "content": f"以下是對話歷史記錄:{self.history} 請根據歷史記錄回答user"},{"role": "user", "content": f"{message.author}: {message.content}"}]
                self.history.append(f"{message.author}: {message.content}")

            reply = openai_api.str_request(msgs, 500)
            self.history.append(f"me: {reply}")

            await message.channel.send(reply)
            

def setup(bot):
    bot.add_cog(Gpt(bot))
