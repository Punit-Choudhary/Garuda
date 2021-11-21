import discord

from discord.ext import commands
from discord.ext.commands import MissingPermissions, MissingRequiredArgument
from discord.ext.commands import CommandNotFound, CommandOnCooldown, BotMissingPermissions

from Tools.utils import get_prefix


class ErrorEventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            prefix = await get_prefix(self.bot, ctx)
            command_not_found_embed = discord.Embed(
                title = "WDYM?",
                description = f"🦅: There is no such command.\n\
                    Type `{prefix}help` to view all available commands.",
                color = 0xFF0000    # Red
            )

            await ctx.send(embed=command_not_found_embed, delete_after=20)

        elif isinstance(error, MissingRequiredArgument):
            prefix = await get_prefix(self.bot, ctx)
            missing_arg_embed = discord.Embed(
                title = "Missing Required Argument!",
                description = f"🦅: Correct implementation of the command is:\n\
                    `{prefix}{ctx.command.name} {ctx.command.usage}`.\n\
                    Hint: Type `{prefix}command_name` to view help.",
                color = 0xFF0000    # Red
            )

            await ctx.send(embed = missing_arg_embed, delete_after=20)

        elif isinstance(error, MissingPermissions):
            missing = ", ".join(error.missing_perms)
            missing_perms_embed = discord.Embed(
                title = "❕Missing Permissions❕",
                description = f"🦅: {ctx.author.mention}, you need {missing} permission(s) to command me.\n\
                    My eyes are on YOU! 👁",
                color = 0x6e2bff    # Purple
            )

            await ctx.send(embed=missing_perms_embed)

        elif isinstance(error, BotMissingPermissions):
            missing = ", ".join(error.missing_perms)
            missing_perms_embed = discord.Embed(
                title = "🆘 Missing Permissions 😢",
                description = f"🦅: {ctx.author.mention}, I need {missing} permission(s) to execute this command\n\
                    Please, reach out Admin of the **{ctx.guild.name} Server** with this issue.",
                color = 0xdb1682    # Pink
            )

            await ctx.send(embed=missing_perms_embed)


# Setup
def setup(bot):
    bot.add_cog(ErrorEventsCog(bot))