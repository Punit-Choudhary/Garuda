import discord

from discord.ext import commands
from Tools.utils import getConfig, updateConfig, get_prefix
from discord.ext.commands import has_permissions


class Prefix(commands.Cog):
    """Change command prefix of Garuda."""
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="prefix", usage="<new-prefix>")
    @has_permissions(administrator = True)
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def prefix(self, ctx, *args):
        """Change command prefix of Garuda."""
        if len(args) > 0:
            new_prefix = args[0]
            data = getConfig(ctx.guild.id)
            data["prefix"] = new_prefix
            updateConfig(ctx.guild.id, data)

            prefix_update_embed = discord.Embed(
                title = "**Prefix Updated**",
                description = f"🦅: Now you can command me using `{new_prefix}` prefix.",
                color = 0x00FF00    # Green
            )

            await ctx.channel.send(embed = prefix_update_embed)
        else:
            prefix_help_embed = discord.Embed(
                title = "**Set Prefix Usage**",
                description = f"🦅: example: `{await get_prefix(self.bot, ctx)}prefix ?`\nReplace `?` with your prefix.",
                color = 0xFF0000    # Red
            )

            await ctx.channel.send(embed = prefix_help_embed)



# Setup
def setup(bot):
    bot.add_cog(Prefix(bot))