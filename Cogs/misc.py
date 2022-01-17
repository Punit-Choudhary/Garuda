import discord

from discord.ext import commands


class MiscCommandsCog(commands.Cog, name="Misc Commands"):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="ping")
    async def ping(self, ctx):
        """return bot's latency"""
        latency = round(self.bot.latency * 1000, 2)
        if latency < 50:
            color_code = 0x03fc39   # green
        elif latency < 90:
            color_code = 0xfcc203   # yellow
        else:
            color_code = 0xfc0703   # red
        
        ping_reply = discord.Embed(
            title=":ping_pong:  pong!",
            description=f"{latency}ms",
            color=color_code
        )

        await ctx.send(embed=ping_reply)

# setup
def setup(bot):
    bot.add_cog(MiscCommandsCog(bot))