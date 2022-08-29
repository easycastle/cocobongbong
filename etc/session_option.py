import discord
import asyncio
from discord.utils import get

from etc.config import BotColor, BotVer

SUBJECT = ['C', 'Python', 'JS/TS', 'FrontEnd', 'BackEnd', 'JAVA']
PROFESSOR_ROLE = ['C 교수님', 'Python 교수님', 'JS/TS 교수님', 'FrontEnd 교수님', 'BackEnd 교수님', 'JAVA 교수님']
STUDENT_ROLE = ['C 수강자', 'Python 수강자', 'JS/TS 수강자', 'FrontEnd 수강자', 'BackEnd 수강자', 'JAVA 수강자']

STUDENT_ROLE_ID = [
    1012912699170111498,        # C 수강자
    1012912588159471736,        # Python 수강자
    1012912798222790746,        # JS/TS 수강자
    1012912917215195226,        # FrontEnd 수강자
    1012913006662926386,        # BackEnd 수강자
    1013052558962589706,        # JAVA 수강자
    ]

PROFESSOR_ROLE_ID = [
    1012603328716345394,        # C 교수님
    1012603866853945385,        # Python 교수님
    1012603950366720020,        # JS/TS 교수님
    1012615075464491008,        # FrontEnd 교수님
    1012615146390179880,        # BackEnd 교수님
    1013052471477805148,        # JAVA 교수님
    ]

PROFESSOR_INTRODUCTION = {
    364226674893651969: '@11.11_dh',                            # 덕환
    942042864823717898: '여 친 조 아',                          # 밀라봉봉
    550660367488122881: '병윤이는 늘 밥을 해줬어',              # 병윤
    411066423025336320: '신찬규 그는 신이야',                   # 신찬규
    798223945600991265: '목잘남',                               # 이현서(경북대)
    439817891240607746: '서울 한복판에 내버려진 건에 대하여',   # 코코조용
}

STUDENT_LIST_CHANNEL = [
    1013610233303670836, 
    1013610555736608821, 
    1013610544349052948, 
    1013610531002790029, 
    1013610519959195708, 
    1013610498756988928, 
    ]

async def update_log_channel(ctx, job):
    member_list_channel = get(ctx.guild.channels, name=f'📋{job}')
    position = member_list_channel.position
    new_channel = await member_list_channel.clone()
    await member_list_channel.delete()
    await new_channel.edit(position=position)
        
    for subject in SUBJECT:
            members = get(ctx.guild.roles, name=f'{subject} {job}').members
            member_list = ''
            for member in members:
                member_list += f'{member.mention} ({member.id})\n'
                
            member_list_embed = discord.Embed(title=subject, description=member_list, color=BotColor)
            member_list_embed.set_footer(text=BotVer)
            
            await new_channel.send(embed=member_list_embed)