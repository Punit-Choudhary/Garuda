import discord

from discord.ext import commands


class Help(commands.Cog, name="help"):
    
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="help")
    async def help(self, ctx):
        pass
