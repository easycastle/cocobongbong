import discord
import asyncio
from discord.ext.commands import Cog, has_permissions, has_role
from discord.commands import slash_command, Option
from discord.ui import Button, Select, View
from discord.utils import get

from etc.config import BotColor, BotVer
from etc.db import check_subject

class Student(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @slash_command(name='출결확인')
    @has_role('수강자')
    async def confirm_attendance(self, ctx, subject: Option(str, '과목', choices=check_subject(), required=True)):
        """출결 상황을 보여줍니다."""
        
        student         = ctx.author
        student_role    = map(lambda x: x.name, student.roles)
        
        if subject in student_role:
            await student.send('개발 중입니다')        # todo: 수강 관리 기능 개발
            await ctx.respond(f'{subject} 과목의 출결 상황을 dm으로 보냈습니다.')

        else:
            await ctx.respond(f'{student.mention}님은 {subject} 과목의 수강자가 아닙니다!')
        
def setup(bot):
    bot.add_cog(Student(bot))