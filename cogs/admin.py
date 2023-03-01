import discord
import asyncio
from discord.ext.commands import Cog, has_role, has_permissions
from discord.commands import slash_command, Option
from discord.ui import Select, View
from discord.utils import get

from etc.config import BotColor, BotVer
from etc.db import *
from etc.create import create_subject
from etc.session_option import basic_permission, head_student_overwrite, student_overwrite
from etc.log_translation import translateLog

import requests, json

logList = None      # log 10개씩 하나로 담은 리스트
embedPage = None    # 임베드 페이지 (0에서 시작)

class Admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='개설', guild_ids=[1012586500006875139])
    @has_role('관리자')
    async def open_session(self, ctx, new_subject: Option(str, '스터디명', required=True), head_student: Option(discord.Member, '스터디 대표생', required=True), color: Option(str, '역할 색상', required=True)):
        """원하는 주제의 스터디를 개설합니다."""
        
        if ' ' in new_subject:
            await ctx.respond('스터디명에 공백은 넣을 수 없습니다!')
        else:
            await ctx.defer()
            
            subject_head_student_role = await ctx.guild.create_role(name=f'{new_subject} <{head_student.name}> 대표생', permissions=basic_permission, color=int(f'0x{color}', 16))
            subject_assistant_role = await ctx.guild.create_role(name=f'{new_subject} <{head_student.name}> 도우미', permissions=basic_permission, color=int(f'0x{color}', 16))
            subject_student_role = await ctx.guild.create_role(name=f'{new_subject} <{head_student.name}> 수강생', permissions=basic_permission, color=int(f'0x{color}', 16))
            
            assistant_position = get(ctx.guild.roles, name='도우미').position
            await subject_head_student_role.edit(position=assistant_position+1)
            student_position = get(ctx.guild.roles, name='수강생').position
            await subject_assistant_role.edit(position=student_position+1)
            
            category = await ctx.guild.create_category(name=f'{new_subject} <{head_student.name}>', position=len(ctx.guild.categories))
            await category.set_permissions(get(ctx.guild.roles, name='@everyone'), view_channel=False, connect=False)
            await category.set_permissions(subject_head_student_role, overwrite=head_student_overwrite)
            await category.set_permissions(subject_student_role, overwrite=student_overwrite)
            
            announcement = await category.create_text_channel('📢공지')
            studying = await category.create_text_channel('📝공부방')
            archive = await category.create_text_channel('📂자료실')
            question = await category.create_text_channel('❓질문')
            attendance = await category.create_text_channel('🙋출석체크')
            assignment = await category.create_text_channel('🎃과제-정답')
            classroom = await category.create_voice_channel('🏫스터디실')
            
            await announcement.edit(sync_permissions=True)
            await studying.edit(sync_permissions=True)
            await archive.edit(sync_permissions=True)
            await question.edit(sync_permissions=True)
            await attendance.edit(sync_permissions=True)
            await assignment.edit(sync_permissions=True)
            await classroom.edit(sync_permissions=True)
            
            head_student_role = get(ctx.guild.roles, name='대표생')
            await head_student.add_roles(head_student_role, subject_head_student_role)
            
            create_subject(f'{new_subject} <{head_student.name}>', str(head_student.id))
            # new_subject_data = {
            #     "parent": {"database_id": database_id['subject']},
            #     "properties": {
            #         "과목": {
            #             "title": [
            #                 {
            #                     "text": {
            #                         "content": f'{new_subject} <{head_student.name}>'
            #                     }
            #                 }
            #             ]
            #         }, 
            #         "대표생": {
            #             "rich_text": [
            #                 {
            #                     "text": {
            #                         "content": str(head_student.id)
            #                     }
            #                 }
            #             ]
            #         }
            #     }
            # }
            # res = requests.post('https://api.notion.com/v1/pages', headers=headers, data=json.dumps(new_subject_data))
            # print(res.text)
            
            await ctx.respond(f'{new_subject} <{head_student.name}> 과목이 개설되었습니다.')
        
    @slash_command(name='폐강')
    @has_role('관리자')
    async def close_session(self, ctx, session: Option(discord.Role, '스터디 대표생 역할', required=True), head_student: Option(discord.Member, '대표생 이름', required=True)):
        """해당 스터디를 폐강합니다."""
        
        if not '대표생' in session.name:
            ctx.respond('알맞은 역할이 아닙니다!')
        elif not session.name in map(lambda x: x.name, head_student.roles):
            await ctx.respond('폐강할 스터디의 담당 대표생이 아닙니다!')
        else:
            await ctx.defer()
            
            for name in ['대표생', '도우미', '수강생']:
                role = get(ctx.guild.roles, name=f'{session.name[:-3]}{name}')
                await role.delete()
                
            if len(list(filter(lambda x: x.name[-3:] == '대표생', head_student.roles))) == 1:
                await head_student.remove_roles(get(ctx.guild.roles, name='대표생'))
            
            category = get(ctx.guild.categories, name=f'{session.name[:-4]}')
            for channel in category.channels:
                await channel.delete()
            await category.delete()
            
            for page in get_db(database_id['subject']):
                if page['properties']['과목']['title'][0]['text']['content'] == session.name[:-4]:
                    block_id = page['id']
            requests.delete(f'https://api.notion.com/v1/blocks/{block_id}', headers=headers)
                
            await ctx.respond('해당 스터디를 폐강하였습니다.')

    @slash_command()
    @has_permissions(administrator=True)
    async def kick(self, ctx, kicked_user: Option(discord.Member, '추방할 유저', required=True), reason: Option(str, '추방하는 이유', required=False, default=None)):
        """문제가 있는 사람들을 추방합니다."""
        
        await ctx.respond(embed=discord.Embed(title='강퇴', description=kicked_user.mention + '님을 추방합니다', color=BotColor))
        await kicked_user.kick(reason=reason)

    @slash_command()
    @has_permissions(administrator=True)
    async def ban(self, ctx, banned_user: Option(discord.Member, '차단할 유저', required=True), reason: Option(str, '차단하는 이유', required=False, default=None)):
        """마음에 들지 않은 사람들을 차단합니다."""
        
        await ctx.respond(embed=discord.Embed(title='강퇴', description=banned_user.mention + '님을 추방합니다', color=BotColor))
        await banned_user.ban(reason=reason)

    @slash_command()
    @has_permissions(administrator=True)
    async def mute_chat(self, ctx, muted_user: Option(discord.Member, '뮤트할 유저', required=True), mute_mode: Option(str, '뮤트 모드', choices=['현재 채널 뮤트', '서버 전체 뮤트'], required=False, default=None)):
        """채팅이 시끄러운 사람들을 조용히 만듭니다."""
        
        if mute_mode == None:
            muteEmbed = discord.Embed(title='채팅 뮤트', description='명령어 뒤에 뮤트 모드를 적어주세요', color=BotColor)
            muteEmbed.add_field(name='`1.` 현재 채널 뮤트', value='이 채널에서만 뮤트시킵니다', inline=False)
            muteEmbed.add_field(name='`2.` 서버 전체 뮤트', value='서버 전체에서 뮤트시킵니다', inline=False)

            await ctx.respond(embed=muteEmbed)

        else:
            sinner = discord.PermissionOverwrite()
            sinner.send_messages = False
            sinner.send_messages_in_threads = False
            sinner.create_public_threads = False
            sinner.create_private_threads = False
            sinner.embed_links = False
            sinner.attach_files = False
            sinner.add_reactions = False
            sinner.use_external_emojis = False
            sinner.use_external_stickers = False
            sinner.mention_everyone = False
            sinner.manage_messages = False
            sinner.manage_threads = False
            sinner.read_message_history = False
            sinner.send_tts_messages = False
            sinner.use_application_commands = False
            sinner.manage_channels = False
            sinner.manage_permissions = False
            sinner.manage_webhooks = False
            sinner.create_instant_invite = False

            if mute_mode == '현재 채널 뮤트':
                await ctx.channel.set_permissions(muted_user, overwrite=sinner)
                await ctx.respond(embed=discord.Embed(title='현재 채널 뮤트', description=f'뮤트 대상 : {muted_user.mention}\n뮤트 채널 : {ctx.channel.mention}\n`뮤트했습니다`', color=BotColor))

            elif mute_mode == '서버 전체 뮤트':
                for sinnerChannel in ctx.guild.text_channels:
                    if muted_user in sinnerChannel.members:
                        await sinnerChannel.set_permissions(muted_user, overwrite=sinner)

                await page.clear_reactions()
                await page.edit(embed=discord.Embed(title='서버 전체 뮤트', description=f'뮤트 대상 : {muted_user.mention}\n`뮤트했습니다`', color=BotColor))

    @slash_command()
    @has_permissions(administrator=True)
    async def unmute_chat(self, ctx, unmuted_user: Option(discord.Member, '언뮤트할 유저', required=True), mute_mode: Option(str, '언뮤트 모드', choices=['현재 채널 언뮤트', '서버 전체 언뮤트'], required=False, default=None)):
        """채팅이 조용해진 사람들을 말할 수 있게 해줍니다."""
        
        if mute_mode == None:
            unmuteEmbed = discord.Embed(title='채팅 언뮤트', description= '명령어 뒤에 언뮤트 모드를 적어주세요', color=BotColor)
            unmuteEmbed.add_field(name='`1.` 현재 채널 언뮤트', value='이 채널에서만 언뮤트시킵니다', inline=False)
            unmuteEmbed.add_field(name='`2.` 서버 전체 언뮤트', value='서버 전체에서 언뮤트시킵니다', inline=False)

            await ctx.respond(embed=unmuteEmbed)

        else:
            if mute_mode == '현재 채널 언뮤트':
                await ctx.channel.set_permissions(unmuted_user, overwrite=None)
                await ctx.respond(embed=discord.Embed(title='현재 채널 언뮤트', description=f'언뮤트 대상 : {unmuted_user.mention}\n언뮤트 채널 : {ctx.channel.mention}\n`언뮤트했습니다`', color=BotColor))

            elif mute_mode == '서버 전체 언뮤트':
                for sinnerChannel in ctx.guild.text_channels:
                    if unmuted_user in sinnerChannel.members:
                        await sinnerChannel.set_permissions(unmuted_user, overwrite=None)

                await page.clear_reactions()
                await page.edit(embed=discord.Embed(title='서버 전체 언뮤트', description=f'언뮤트 대상 : {unmuted_user.mention}\n`언뮤트했습니다`', color=BotColor))

    @slash_command()
    @has_permissions(administrator=True)
    async def clear(self, ctx, amount: Option(int, '삭제할 개수', required=False, default=None), name: Option(discord.TextChannel, '채널 이름', required=False, default=None)):
        """많은 메세지를 한번에 삭제합니다."""
        
        if amount == None:
            await ctx.channel.purge(limit=10)
        else:
            await ctx.channel.purge(limit=amount)

        await ctx.delete()
        
def setup(bot):
    bot.add_cog(Admin(bot))