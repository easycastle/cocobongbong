import discord
import asyncio
from discord.ext import tasks
from discord.ext.commands import Cog, has_role, has_permissions
from discord.commands import slash_command, Option
from discord.ui import Button, Select, View
from discord.utils import get

from etc.config import *
from etc.session_option import *

from datetime import datetime
import notion_database

import os

intents = discord.Intents.default()
intents.members = True
intents.typing = True
bot = discord.Bot(intents=intents)

if __name__ == '__main__':
    for extension in EXTENSIONS:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('cannot be loaded {}\n{}'.format(extension, e))

@bot.event
async def on_ready():
    print('빌드 완료')
    print('봇 : 코코봉봉')
    print('=============')
    
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f'/help 치면 사용법 설명'))
    
@bot.event
async def on_member_update(before, after):
    before_roles = before.roles
    after_roles = after.roles
    
    if len(before_roles) != len(after_roles):
        guild = bot.get_guild(1012586500006875139)
        
        if len(list(filter(lambda x: True if '교수님' in x else False, map(lambda x: x.name, after_roles)))) == 1: await after.remove_roles(get(guild.roles, name='교수님'))
        elif len(list(filter(lambda x: True if '수강자' in x else False, map(lambda x: x.name, after_roles)))) == 1: await after.remove_roles(get(guild.roles, name='수강생'))

        category = list(set(after_roles) - set(before_roles))[0].name[-3:] if len(after_roles) > len(before_roles) else list(set(before_roles) - set(after_roles))[0].name[-3:]
        await update_log_channel(guild, category)

access_token = os.environ['BOT_TOKEN']
bot.run(access_token)