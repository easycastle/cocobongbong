import discord
import asyncio
from discord.ext.commands import Cog
from discord.commands import slash_command, Option

from etc.config import BotColor, BotVer

class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def help(self, ctx):
        """컬트봇의 사용 방법을 알려줍니다."""
        
        helpEmbed = discord.Embed(title='도움말', description='여기서 사용할 수 있는 명령어 모음입니다.', color=BotColor)
        helpEmbed.add_field(name='`/help`', value='코코봉봉의 사용 방법을 알려줍니다.', inline=True)
        helpEmbed.add_field(name='`/수강자명단`', value='교수님에게 배울 수강자 명단을 보여줍니다.', inline=True)
        helpEmbed.add_field(name='`/출석체크`', value='출석 체크를 진행합니다.', inline=True)
        helpEmbed.set_footer(text=BotVer)
        
        await ctx.respond(embed=helpEmbed)

def setup(bot):
    bot.add_cog(Help(bot))