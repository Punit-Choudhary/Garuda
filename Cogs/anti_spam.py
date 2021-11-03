import json
import discord

from discord.ext import commands
from discord.ext.commands.core import has_permissions

from Tools.utils import getConfig, updateConfig


class AntiSpamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="antispam")
    @has_permissions(administrator = True)
    async def antispam(self, ctx, antispam):
        # get config of particular guild
        data = getConfig(ctx.guild.id)
        # data = json.load(config)

        if antispam == "true":
            data['antiSpam'] = True
           
            antispam_enable_embed = discord.Embed(
                title = "**ANTI-SPAM ENABLED**",
                description = "🦅: Anti-Spam Has Been Enabled 👁‍🗨",
                color = 0x00FF00    # Green Color
            )

            updateConfig(ctx.guild.id, data)
            await ctx.channel.send(embed = antispam_enable_embed)

        elif antispam == "false":
            data['antiSpam'] = False

            antispam_disable_embed = discord.Embed(
                title = "**ANTI-SPAM DISABLED**",
                description = "🦅: Anti-Spam Has Been Disabled ❌",
                color = 0xFF0000    # Red Color
            )

            updateConfig(ctx.guild.id, data)
            await ctx.channel.send(embed = antispam_disable_embed)
        else:
            antispam_wrong_input_embed = discord.Embed(
                title = "**illegal Input Provided**",
                description = f"🦅: illegal Input Provided.\nLegal values: `true`, `false`\nCurrently Anti-Spam is `{'Enabled' if data['antiSpam'] else 'Disabled'}`",
                color = 0xFFA500    # Orange
            )

            await ctx.channel.send(embed = antispam_wrong_input_embed)

# Setup Bot

def setup(bot):
    bot.add_cog(AntiSpamCog(bot))
