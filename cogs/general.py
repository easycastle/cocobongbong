import discord
import asyncio
from discord.ext.commands import Cog, has_permissions, has_role
from discord.commands import slash_command, Option
from discord.ui import Select, View
from discord.utils import get

from etc.db import *
from etc.config import BotColor
from etc.config import BotVer

import requests, json

class General(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @slash_command(name='학번')
    async def my_id(self, ctx):
        """자신의 학번(디스코드 id)를 알려줍니다."""

        my_id_embed = discord.Embed(title='학번', description=f'{ctx.author.mention}님의 학번은 **{ctx.author.id}**입니다.', color=BotColor)
        my_id_embed.set_footer(text=BotVer)
        
        await ctx.respond(embed=my_id_embed)
        
    @slash_command(name='강의정보')
    async def session_info(self, ctx):
        """강의 정보를 알려줍니다."""
        
        session_info = get_session_info()
        
        session_info_embed = discord.Embed(title='강의 정보', description='강의 정보를 알려줍니다.', color=BotColor)
        session_info_embed.set_footer(text=BotVer)
        
        for session in session_info:
            session_info_embed.add_field(
                name=f'{session[0]} - {session[1]}', 
                value=f'''
                강의 기간 : {session[3]} ~ {session[4]}
                강의 시간 : {session[5]}
                강의 장소 : {session[6]}
                정원 : {session[7]}''',
                inline=True)
            
        await ctx.respond(embed=session_info_embed)

    @slash_command(name='스터디신청', guild_ids=[1012586500006875139])
    async def register(self, ctx):
        """스터디 신청을 도와줍니다."""
        
        if ctx.channel.name == '🃏신청':
            view = View()
            
            subject = Select(
                placeholder='신청할 과목을 선택하세요.', 
                options=[
                    discord.SelectOption(label=session, description=session.split()[1]) for session in get_subject()
                ]
            )
            
            async def subject_callback(interaction):
                student_role = get(ctx.guild.roles, name='수강생')
                subject_role = get(ctx.guild.roles, name=f'{subject.values[0]} 수강생')
                
                await ctx.author.add_roles(student_role, subject_role)
                
                subject.disabled = True
                subject.placeholder = f'{subject.values[0]} 과목 스터디를 신청하였습니다.'
                
                await interaction.response.edit_message(view=view)
            
            subject.callback = subject_callback
        
            view.add_item(subject)
            await ctx.respond(view=view)
            
        else:
            await ctx.delete()

    @slash_command()
    async def help(self, ctx, category: Option(str, '명령어 카테고리', choices=['어드민', '일반', '대표생', '수강생'], required=False, default=None)):
        """코코봉봉의 사용 방법을 알려줍니다."""
        
        if category == None:
            help_embed = discord.Embed(title='도움말', description='아래의 명령어들을 이용해 도움말을 볼 수 있습니다.', color=BotColor)
            help_embed.add_field(name=f'`/help`', value='명령어들의 종류를 크게 구분해서 보여줍니다.', inline=True)
            help_embed.add_field(name=f'`/help 어드민`', value='관리자만 사용 가능한 명령어 모음입니다.', inline=True)
            help_embed.add_field(name=f'`/help 일반`', value='일반적으로 사용 가능한 명령어 모음입니다.', inline=True)
            help_embed.add_field(name=f'`/help 대표생`', value='대표생들이 사용 가능한 명령어 모음입니다.', inline=True)
            help_embed.add_field(name=f'`/help 수강생`', value='학생들이 사용 가능한 명령어입니다.', inline=True)
        
        elif category == '어드민':
            help_embed = discord.Embed(title='관리자 명령어', description='관리자만 사용 가능한 명령어 모음입니다.', color=BotColor)
            help_embed.add_field(name=f'`/개설 <스터디명> <스터디 대표생> <역할 색상>`', value='원하는 주제의 스터디를 개설합니다.', inline=True)
            help_embed.add_field(name=f'`/폐강 <스터디 대표생 역할> <대표생 이름>`', value='해당 스터디를 폐강합니다.', inline=True)
            help_embed.add_field(name=f'`/kick <추방할 유저>`', value='문제가 있는 사람들을 추방합니다.', inline=True)
            help_embed.add_field(name=f'`/ban <차단할 유저>`', value='마음에 들지 않은 사람들을 차단합니다.', inline=True)
            help_embed.add_field(name=f'`/chat_mute <뮤트할 유저>`', value='채팅이 시끄러운 사람들을 조용히 만듭니다.', inline=True)
            help_embed.add_field(name=f'`/chat_unmute <언뮤트할 유저>`', value='채팅이 조용해진 사람들을 말할 수 있게 해줍니다.', inline=True)
            help_embed.add_field(name=f'`/voice_mute <뮤트할 유저>`', value='소리가 시끄러운 사람들을 조용히 만듭니다.', inline=True)
            help_embed.add_field(name=f'`/voice_unmute <언뮤트할 유저>`', value='소리가 조용해진 사람들을 말할 수 있게 해줍니다.', inline=True)
            help_embed.add_field(name=f'`/clear`', value='많은 메세지를 한번에 삭제합니다.', inline=True)
            help_embed.add_field(name=f'`/log`', value='이 서버의 감사 로그를 보여줍니다.', inline=True)
            
        elif category == '일반':
            help_embed = discord.Embed(title='도움말', description='모든 스터디원이 사용 가능한 명령어 모음입니다.', color=BotColor)
            help_embed.add_field(name='`/학번`', value='자신의 학번(디스코드 id)를 알려줍니다.', inline=True)
            help_embed.add_field(name='`/스터디신청`', value='스터디 신청을 도와줍니다.', inline=True)
        
        elif category == '대표생':
            help_embed = discord.Embed(title='도움말', description='대표생들이 사용 가능한 명령어 모음입니다.', color=BotColor)
            help_embed.add_field(name='`/수강생명단 <조회할 수강생 역할>`', value='스터디의 수강생 명단을 보여줍니다.', inline=True)
            help_embed.add_field(name='`/조회 <조회할 학생>`', value='수강생의 정보를 조회합니다.', inline=True)
            help_embed.add_field(name='`/도우미임용`', value='스터디를 도와줄 도우미를 납치합니다.', inline=True)
            help_embed.add_field(name='`/출석체크`', value='출석 체크를 진행합니다.', inline=True)

        elif category == '수강생':
            help_embed = discord.Embed(title='도움말', description='학생들이 사용 가능한 명령어입니다.', color=BotColor)
            help_embed.add_field(name='`/출결확인 <과목>`', value='출결 상황을 보여줍니다.(개발 중)', inline=True)
        
        help_embed.set_footer(text=BotVer)
        
        await ctx.respond(embed=help_embed)
        
def setup(bot):
    bot.add_cog(General(bot))
