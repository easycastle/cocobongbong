import discord
import asyncio
from discord.ext.commands import Cog, has_permissions, has_role
from discord.commands import slash_command, Option
from discord.ui import Select, View
from discord.utils import get

from etc.config import BotColor, BotVer
from etc.db import *

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
        
def setup(bot):
    bot.add_cog(General(bot))