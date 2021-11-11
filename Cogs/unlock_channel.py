import discord
from discord import channel

from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.core import command


class UnlockChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="unlock")
    @has_permissions(administrator = True)
    @commands.guild_only()
    async def unlock(self, ctx):
        """
        🔓 unlock the locked channel
        """
        perms = ctx.channel.overwrites_for(ctx.guild.default_role)
        perms.send_messages = True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms)

        await ctx.channel.edit(name=ctx.channel.name.replace("🔒-", "", 1))

        unlock_successful_embed = discord.Embed(
            title = "🦅: 🔓 Channel Unlocked",
            color = 0x00FF00    # Green
        )

        await ctx.channel.send(embed = unlock_successful_embed)


# Setup
def setup(bot):
    bot.add_cog(UnlockChannelCog(bot))