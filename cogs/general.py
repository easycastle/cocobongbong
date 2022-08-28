import discord
import asyncio
from discord.ext.commands import Cog, has_permissions, has_role
from discord.commands import slash_command, Option
from discord.ui import Button, Select, View
from discord.utils import get

from config import BotColor, BotVer

class General(Cog):
    def __init__(self, bot):
        self.bot = bot
        
def setup(bot):
    bot.add_cog(General(bot))