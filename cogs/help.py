import discord
import asyncio
from discord.ext.commands import Cog
from discord.commands import slash_command, Option

from etc.config import BotColor, BotVer

class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def help(self, ctx, category: Option(str, '명령어 카테고리', choices=['일반', '교수님', '수강자'], required=False, default=None)):
        """코코봉봉의 사용 방법을 알려줍니다."""
        
        if category == None:
            embed = discord.Embed(title='도움말', description='아래의 명령어들을 이용해 도움말을 볼 수 있습니다.', color=CoCoColor)
            embed.add_field(name=f'`/help`', value='명령어들의 종류를 크게 구분해서 보여줍니다.', inline=True)
            embed.add_field(name=f'`/help 일반`', value='일반적으로 사용 가능한 명령어 모음입니다.', inline=True)
            embed.add_field(name=f'`/help 교수님`', value='교수님들이 사용 가능한 명령어 모음입니다.', inline=True)
            embed.add_field(name=f'`/help 수강자`', value='학생들이 사용 가능한 명령어입니다.', inline=True)
        
        elif category == '일반':
            help_embed = discord.Embed(title='도움말', description='일반적으로 사용 가능한 명령어 모음입니다.', color=BotColor)
            help_embed.add_field(name='`/학번`', value='자신의 학번(디스코드 id)를 알려줍니다.', inline=True)
            help_embed.add_field(name='`/교수소개 <과목>`', value='과목별 교수님의 한 줄 소개를 보여줍니다.', inline=True)
            help_embed.add_field(name='`/수강신청 <과목>`', value='수강신청을 도와줍니다.', inline=True)
        
        elif category == '교수님':
            help_embed = discord.Embed(title='도움말', description='교수님들이 사용 가능한 명령어 모음입니다.', color=BotColor)
            help_embed.add_field(name='`/수강자명단 <과목>`', value='교수님에게 배울 수강자 명단을 보여줍니다.', inline=True)
            help_embed.add_field(name='`/조회 <조회할 학생>`', value='수강생의 정보를 조회합니다.', inline=True)
            help_embed.add_field(name='`/출석체크`', value='출석 체크를 진행합니다.', inline=True)

        elif category == '수강자':
            help_embed = discord.Embed(title='도움말', description='학생들이 사용 가능한 명령어입니다.', color=BotColor)
            help_embed.add_field(name='`/출결확인 <과목>`', value='출결 상황을 보여줍니다.', inline=True)
        
        help_embed.set_footer(text=BotVer)
            
        await ctx.respond(embed=help_embed)

def setup(bot):
    bot.add_cog(Help(bot))