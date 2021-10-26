import json
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions


class AntiSpamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="antispam")
    @has_permissions(administrator = True)
    async def antispam(self, ctx, antispam):

        if antispam == "true":
            # Edit config file
            with open("config.json") as file:
                data = json.load(file)
                data["antispam"] = True
                updated_data = json.dumps(data, indent=4, ensure_ascii=False, allow_nan=True)
            
            antispam_enable_embed = discord.Embed(
                title = "**ANTI-SPAM ENABLED**",
                description = "🦅: Anti-Spam Has Been Enabled 👁‍🗨",
                color = 0x2fa737    # Green Color
            )

            await ctx.channel.send(embed = antispam_enable_embed)

        else:
            # Edit config file
            with open("config.json") as config:
                data = json.load(config)
                data["antispam"] = False
                updated_data = json.dumps(data, indent=4, ensure_ascii=False, allow_nan=True)
            
            antispam_disable_embed = discord.Embed(
                title = "**ANTI-SPAM DISABLED**",
                description = "🦅: Anti-Spam Has Been Disabled ❌",
                color = 0xe00000    # Red Color
            )

            await ctx.channel.send(embed = antispam_disable_embed)
        
        # Updating Data in Config file
        with open("config.json") as file:
            file.write(updated_data)


# Setup Bot

def setup(bot):
    bot.add_cog(AntiSpamCog(bot))
