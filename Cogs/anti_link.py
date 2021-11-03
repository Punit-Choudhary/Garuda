import json
import discord

from discord.ext import commands
from discord.ext.commands.core import has_permissions

from Tools.utils import getConfig, updateConfig


class AntiLinkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="antilink")
    @has_permissions(administrator = True)
    async def antilink(self, ctx, antilink):
        # get config file of guild
        data = getConfig(ctx.guild.id)

        if antilink == "true":
            data['antiLink'] = True

            antilink_enable_embed = discord.Embed(
                title = "**ANTI-LINK ENABLED**",
                description = "🦅: Anti-Link Has Been Enabled 👁‍🗨",
                color = 0x00FF00    # Green
            )

            updateConfig(ctx.guild.id, data)
            await ctx.channel.send(embed = antilink_enable_embed)
        elif antilink == "false":
            data['antiLink'] = False

            antilink_disable_embed = discord.Embed(
                title = "**ANTI-LINK DISABLED**",
                description = "🦅: Anti-Link Has Been Disabled ❌",
                color = 0xFF0000    # Red
            )

            updateConfig(ctx.guild.id, data)
            await ctx.channel.send(embed = antilink_disable_embed)
        else:
            antilink_wrong_input_embed = discord.Embed(
                title = "**illegal Input Provided**",
                description = f"🦅: illegal Input Provided.\nLegal values: `true`, `false`\nCurrently Anti-Link is `{'Enabled' if data['antiLink'] else 'Disabled'}`",
                color = 0xFFA500    # Orange
            )

            await ctx.channel.send(embed = antilink_wrong_input_embed)

# Setup Bot
def setup(bot):
    bot.add_cog(AntiLinkCog(bot))