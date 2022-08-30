import discord
import asyncio
from discord.utils import get

from etc.config import BotColor, BotVer

SUBJECT = ['C', 'Python', 'JS/TS', 'FrontEnd', 'BackEnd', 'JAVA']

PROFESSOR_INTRODUCTION = {
    364226674893651969: '@11.11_dh',                            # 덕환
    942042864823717898: '여 친 조 아',                          # 밀라봉봉
    550660367488122881: '병윤이는 늘 밥을 해줬어',              # 병윤
    411066423025336320: '신찬규 그는 신이야',                   # 신찬규
    798223945600991265: '목잘남',                               # 이현서(경북대)
    439817891240607746: '서울 한복판에 내버려진 건에 대하여',   # 코코조용
}

async def update_log_channel(guild, category):
    member_list_channel = get(guild.channels, name=f'📋{category}')
    position = member_list_channel.position
    new_channel = await member_list_channel.clone()
    await member_list_channel.delete()
    await new_channel.edit(position=position)
        
    for subject in SUBJECT:
            members = get(guild.roles, name=f'{subject} {category}').members
            member_list = ''
            for member in members:
                member_list += f'{member.mention} ({member.id})\n'
                
            member_list_embed = discord.Embed(title=subject, description=member_list, color=BotColor)
            member_list_embed.set_footer(text=BotVer)
            
            await new_channel.send(embed=member_list_embed)