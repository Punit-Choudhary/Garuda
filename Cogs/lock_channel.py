import discord
from discord import channel

from discord.ext import commands
from discord.ext.commands import has_permissions


class LockChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="lock")
    @has_permissions(administrator = True)
    @commands.guild_only()
    async def lock(self, ctx):
        """
        🔒 Locks the channel
        """

        # change the channel name
        await ctx.channel.edit(name=f"🔒-{ctx.channel.name}")
        perms = ctx.channel.overwrites_for(ctx.guild.default_role)
        perms.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms)

        lock_success_embed = discord.Embed(
            title = f"**Successfully Locked {ctx.channel.name}**",
            color = 0x00FF00
        )

        await ctx.channel.send(embed = lock_success_embed)


# Setup
def setup(bot):
    bot.add_cog(LockChannelCog(bot))