import discord
import asyncio
from discord.ext import tasks
from discord.ext.commands import Cog, has_permissions, has_role
from discord.commands import slash_command, Option
from discord.ui import Button, Select, View
from discord.utils import get

from etc.config import BotColor, BotVer
from etc.session_option import SUBJECT, STUDENT_LIST_CHANNEL

class Student(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_study_members.start()
        
    @tasks.loop(hours=1.0)
    async def check_study_members(self):
        
        server                  = self.bot.get_guild(1012586500006875139)
        checklist               = dict(zip(STUDENT_LIST_CHANNEL, SUBJECT)).items()
        
        for item in checklist:
            study_list          = server.get_channel(item[0])
            professors          = get(server.roles, name=f'{item[1]} 교수님').members
            students            = get(server.roles, name=f'{item[1]} 수강자').members
            professor_list      = ''
            student_list        = ''
            
            check_embed = discord.Embed(title=f'📋{item[1]} 스터디원', color=BotColor)
            for professor in professors:
                professor_list  += f'{professor.name} ({professor.id})\n'
            check_embed.add_field(name='교수님', value=professor_list if professor_list != '' else '-', inline=False)
            for student in students:
                student_list    += f'{student.name} ({student.id})\n'
            check_embed.add_field(name='수강자', value=student_list if student_list != '' else '-', inline=False)
            check_embed.set_footer(text=BotVer)
            
            await study_list.purge()           
            await study_list.send(embed=check_embed)
        
    @slash_command(name='출결확인')
    @has_role('수강자')
    async def confirm_attendance(self, ctx, subject: Option(str, '과목', choices=SUBJECT, required=True)):
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