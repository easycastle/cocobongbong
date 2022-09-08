import discord
import asyncio
from discord.utils import get

from etc.config import BotColor, BotVer

basic_permission = discord.Permissions(
    view_channel                = True, 
    create_instant_invite       = True, 
    change_nickname             = True, 
    send_messages               = True, 
    send_messages_in_threads    = True, 
    create_public_threads       = True, 
    create_private_threads      = True, 
    embed_links                 = True, 
    attach_files                = True, 
    add_reactions               = True, 
    external_emojis             = True, 
    external_stickers           = True, 
    mention_everyone            = True, 
    read_message_history        = True, 
    use_application_commands    = True, 
    connect                     = True, 
    speak                       = True, 
    stream                      = True, 
    # use_embedded_activities = True,       todo: 활동 사용하기 권한 확인
    use_voice_activation        = True,
)

professor_overwrite = discord.PermissionOverwrite(
    view_channel                = True, 
    manage_channels             = True, 
    create_instant_invite       = True, 
    send_messages               = True, 
    send_messages_in_threads    = True, 
    create_public_threads       = True, 
    create_private_threads      = True, 
    embed_links                 = True, 
    attach_files                = True, 
    manage_messages             = True, 
    connect                     = True, 
    speak                       = True, 
    stream                      = True, 
    # use_embedded_activities = True,       todo: 활동 사용하기 권한 확인
    use_voice_activation        = True, 
    priority_speaker            = True, 
    mute_members                = True, 
    deafen_members              = True, 
    move_members                = True, 
    manage_events               = True, 
)

student_overwrite = discord.PermissionOverwrite(
    view_channel                = True, 
    create_instant_invite       = True, 
    send_messages               = True, 
    send_messages_in_threads    = True, 
    embed_links                 = True, 
    attach_files                = True, 
    connect                     = True, 
    speak                       = True, 
    stream                      = True, 
    # use_embedded_activities = True,       todo: 활동 사용하기 권한 확인
    use_voice_activation        = True, 
)

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