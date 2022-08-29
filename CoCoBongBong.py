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

# access_token = os.environ['BOT_TOKEN']
bot.run('NzU4OTU5Njg2NDcyNTY0NzQ2.GnGF5j.L2yqZ3EJc6JTTHi_A56WVjHbbbH1HGuwmrzWS8')