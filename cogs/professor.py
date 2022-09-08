import discord
import asyncio
from discord.ext.commands import Cog, has_permissions, has_role
from discord.commands import slash_command, Option
from discord.ui import Button, Select, View
from discord.utils import get

from etc.config import BotColor, BotVer
from etc.db import get_subject

from datetime import datetime

class Professor(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='수강자명단')
    @has_role('교수님')
    async def check_students(self, ctx, student_role: Option(discord.Role, '조회할 학생', required=True)):    
        """교수님에게 배울 수강자 명단을 보여줍니다."""
        
        if student_role.name[-3:] != '수강자':
            await ctx.respond('올바른 역할이 아닙니다!')
            
        else:
            professor_roles = ctx.author.roles
            subject = student_role.name[0:-4]
            is_professor = False
            
            for role in professor_roles:
                if f'{subject} 교수님' == role.name:
                    students        = get(ctx.guild.roles, name=f'{student_role.name}').members
                    student_list    = ''
                    
                    student_list_embed = discord.Embed(title='수강자 리스트', description=f'{ctx.author.mention}님의 {subject} 과목 수강자 리스트입니다.', color=BotColor)
                    for student in students:
                        student_list += f'{student.mention} ({student.id})\n'
                    student_list_embed.add_field(name=f'{role.name}', value=student_list)
                    student_list_embed.set_footer(text=BotVer)
                    
                    await ctx.respond(embed=student_list_embed)
                    is_professor = True
                    break
            
            if not is_professor:    
                await ctx.respond(f'교수님은 {subject} 담당자가 아닙니다!')

    @slash_command(name='조회')
    @has_role('교수님')
    async def refer_student(self, ctx, student: Option(discord.Member, '조회할 학생', required=True)):
        """수강생의 정보를 조회합니다."""
        
        student_role    = map(lambda x: x.strip(' 수강자'), filter(lambda x: True if ' 수강자' in x else False, map(lambda x: x.name, student.roles)))
        professor_role  = map(lambda x: x.strip(' 교수님'), filter(lambda x: True if ' 교수님' in x else False, map(lambda x: x.name, ctx.author.roles)))

        if set(student_role) & set(professor_role) != set():
            refer_student_embed = discord.Embed(title='학생 조회', description=f'{student.mention}님의 정보입니다.', color=BotColor)
            refer_student_embed.add_field(name='이름', value=f'**{student.name}**', inline=False)
            refer_student_embed.add_field(name='학번', value=f'**{student.id}**', inline=False)
            refer_student_embed.set_footer(text=BotVer)
            
            await ctx.respond(embed=refer_student_embed)
            
        else:
            await ctx.respond('교수님이 가르치는 수강생이 아닙니다!')
        
    @slash_command(name='출석체크')
    @has_role('교수님')
    async def attendance_check(self, ctx):
        """출석 체크를 진행합니다."""
        
        if ctx.channel.name == '🙋출석체크':
            subject                 = ctx.channel.category.name
            channel_member_list     = set(ctx.author.voice.channel.members)
            professor_list          = list(channel_member_list & set(get(ctx.guild.roles, name=f'{subject} 교수님').members))
            student_list            = get(ctx.guild.roles, name=f'{subject} 수강자').members
            attended_member_list    = list(channel_member_list - set(professor_list))
            absent_member_list      = list(set(student_list) - set(attended_member_list))
            
            professor               = ''
            attended_member         = ''
            absent_member           = ''
            
            for member in professor_list:
                professor           += f'{member.mention}({member.id}) '
            for member in attended_member_list:
                attended_member     += f'{member.mention}({member.id}) '
            for member in absent_member_list:
                absent_member       += f'{member.mention}({member.id}) '
                
            if absent_member == '':
                absent_member       = '-'
            if attended_member == '':
                attended_member     = '-'
            
            attendance_check_embed = discord.Embed(title=f'{datetime.now().strftime("%Y-%m-%d")} 출석 체크', description=f'총원 {len(professor_list) + len(student_list)}명, 교수님 {len(professor_list)}명, 출석 {len(attended_member_list)}명, 결석 {len(absent_member_list)}명', color=BotColor)
            attendance_check_embed.add_field(name='교수님', value=professor, inline=False)
            attendance_check_embed.add_field(name='출석자', value=attended_member, inline=False)
            attendance_check_embed.add_field(name='결석자', value=absent_member, inline=False)
            attendance_check_embed.set_footer(text=BotVer)
            
            await ctx.respond(embed=attendance_check_embed)
            
        else:
            await ctx.respond('이곳은 출석체크를 하는 곳이 아닙니다!')
        
def setup(bot):
    bot.add_cog(Professor(bot))