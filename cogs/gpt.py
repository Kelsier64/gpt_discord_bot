import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import openai_api
import requests
import base64
class Gpt(commands.Cog):
    gpt_state = True
    def __init__(self,bot):
        self.bot = bot
    @nextcord.slash_command(name="activate",description="activate the gpt",guild_ids=[1270418744434491413,1156116900321960017])
    async def activate(self,interaction:Interaction):
        self.gpt_state = True
        await interaction.response.send_message("gpt is now activated")

    @nextcord.slash_command(name="deactivate",description="deactivate the gpt",guild_ids=[1270418744434491413,1156116900321960017])
    async def deactivate(self,interaction:Interaction):
        self.gpt_state = False
        await interaction.response.send_message("gpt is now deactivated")

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
                            {"role": "user", "content": message.content}]
            else:
                msgs = [{"role": "user", "content": message.content}]
            reply = openai_api.str_request(msgs, 500)
            await message.channel.send(reply)

def setup(bot):
    bot.add_cog(Gpt(bot))
