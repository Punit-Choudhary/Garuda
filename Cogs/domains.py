import re
import discord
from discord import embeds

from discord.ext import commands
from discord.ext.commands.core import has_permissions

from Tools.utils import getConfig, updateConfig


class Domains(commands.Cog):
    """
    This class contain functions to manage white-listed
    and blacklisted domains.
    
    --> white-listed domains will be allowed even if anti-link
        is enabled.
    --> black-listed domains will not be allowed even if
        anti-link is disabled.
    """

    def __init__(self, bot):
        self.bot = bot

    def extract_links(self, message) -> list:
        regex=r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}'
        urls = re.findall(regex, message.lower())
        return urls
 

# ----------- Whitelisting commands ------------- #

    @commands.command(name="addwhite")
    @has_permissions(administrator = True)
    async def addwhite(self, ctx, *args):
        """
        Mark domain as white-listed.
        usage example: ~addwhite https://youtube.com
        """

        # get config file
        config = getConfig(ctx.guild.id)
        data = config['whiteListedDomains']
        data_blacklisted = config['blackListedDomains']

        message = " ".join([arg for arg in args])
        urls = self.extract_links(message)
        for url in urls:
            if url in data:
                addwhite_present_embed = discord.Embed(
                    title = "**Domain Already Present**",
                    description = f"🦅: Given domain `{url}` is already `white-listed`.\
                    \n**Tip:** You can find all `whitelisted` domains using `~getwhite` command.",
                    color = 0xFF0000    # Red
                )

                await ctx.channel.send(embed = addwhite_present_embed)
            elif url in data_blacklisted:
                illegal_operation_black = discord.Embed(
                    title = "**illegal operation assigned**",
                    description = f"🦅: Given domain `{url}` is currently `black-listed`.\
                    \n**Tip:** You can always remove a domain using `~removewhite <url>`, `~removeblack <url>`"\
                    "to remove `white-listed`, and `black-listed` domain respectively.",
                    color = 0xFF0000    # Red
                )

                await ctx.channel.send(embed = illegal_operation_black)
            else:
                data.append(url)
                addwhite_added_embed = discord.Embed(
                    title = "**Domain White-listed Successfully**",
                    description = f"🦅: Given domain `{url}` has been "\
                        "successfully `whitelisted` ✅",
                    color = 0x00FF00    # Green
                )

                updateConfig(ctx.guild.id, config)
                await ctx.channel.send(embed = addwhite_added_embed)
    

    @commands.command(name="removewhite")
    @has_permissions(administrator = True)
    async def removewhite(self, ctx, *args):
        """
        Remove given domain urls from whitelisted category
        usage example: ~removewhite https://youtube.com
        """

        # get config file
        config = getConfig(ctx.guild.id)
        data = config['whiteListedDomains']
        data_blacklisted = config['blackListedDomains']

        message = " ".join(arg for arg in args)
        urls = self.extract_links(message)

        for url in urls:
            if url in data:
                # remove url from list
                data.remove(url)

                removewhite_success_embed = discord.Embed(
                    title = "**Domain Removed Successfully**",
                    description = f"🦅: Successfully removed `{url}` from `white-listed` "\
                        "domains list.",
                    color = 0x00FF00    # Green
                )

                updateConfig(ctx.guild.id, config)
                await ctx.channel.send(embed = removewhite_success_embed)

            elif url in data_blacklisted:
                removewhite_blacklisted_embed = discord.Embed(
                    title = "**Domain Not Found**",
                    description = f"🦅: Given domain `{url}` is not `white-listed`."\
                        f"\nHowever it is `black-listed`, use `~removeblack {url}` to remove.",
                    color = 0xedbe13    # yellow
                )

                await ctx.channel.send(embed = removewhite_blacklisted_embed)
            
            else:
                removewhite_notfound_embed = discord.Embed(
                    title = "**Domain Not Found**",
                    description = f"🦅: Give domain `{url}` is neither `white-listed` nor "\
                        "`black-listed`",
                    color = 0xFF0000    # Red
                )

                await ctx.channel.send(embed = removewhite_notfound_embed)
    

    @commands.command(name="getwhite")
    async def getwhite(self, ctx):
        """
        Return all domains that are allowed by admins
        in the server.
        """

        # get config file
        config = getConfig(ctx.guild.id)
        data = config['whiteListedDomains']

        if data:
            domains = "\n".join(url for url in data)

            getwhite_domains_embed = discord.Embed(
                title = "**Allowed Domains ✅**",
                description = f"🦅: These are the domains which are allowed in **{ctx.guild.name}**:\n```{domains}```",
                color = 0xffffff
            )

            await ctx.channel.send(embed = getwhite_domains_embed)
        else:
            getwhite_notfound_embed = discord.Embed(
                title = "**Error 404**",
                description = f"🦅: Looks like **{ctx.guild.name}** don't have any white-listed domain.",
                color = 0xFF0000
            )

            await ctx.channel.send(embed = getwhite_notfound_embed)



# ------------- BlackListing Commands -------------- #

    @commands.command(name="addblack")
    @has_permissions(administrator = True)
    async def addblack(self, ctx, *args):
        """
        Mark domain as white-listed.
        usage example: ~addblack https://youtube.com
        """

        # get config file
        config = getConfig(ctx.guild.id)
        data = config['blackListedDomains']
        data_whitelisted = config['whiteListedDomains']


        message = " ".join([arg for arg in args])
        urls = self.extract_links(message)
        for url in urls:
            if url in data:
                addblack_present_embed = discord.Embed(
                    title = "**Domain Already Present**",
                    description = f"🦅: Given domain `{url}` is already `black-listed`.\
                    \n**Tip:** You can find all `black-listed` domains using `~getblack` command.",
                    color = 0xFF0000    # Red
                )

                await ctx.channel.send(embed = addblack_present_embed)
            elif url in data_whitelisted:
                illegal_operation_black = discord.Embed(
                    title = "**illegal operation assigned**",
                    description = f"🦅: Given domain `{url}` is currently `white-listed`.\
                    \n**Tip:** You can always remove a domain using `~removewhite <url>`, `~removeblack <url>` "\
                    "to remove `white-listed`, and `black-listed` domain respectively.",
                    color = 0xFF0000    # Red
                )

                await ctx.channel.send(embed = illegal_operation_black)
            else:
                data.append(url)
                addblack_added_embed = discord.Embed(
                    title = "**Domain Black-listed Successfully**",
                    description = f"🦅: Given domain `{url}` has been "\
                        "successfully `blacklisted` ✅",
                    color = 0x00FF00
                )

                updateConfig(ctx.guild.id, config)
                await ctx.channel.send(embed = addblack_added_embed)


    @commands.command(name="removeblack")
    @has_permissions(administrator = True)
    async def removeblack(self, ctx, *args):
        """
        Remove given domain urls from whitelisted category
        usage example: ~removeblack https://youtube.com
        """

        # get config file
        config = getConfig(ctx.guild.id)
        data = config['blackListedDomains']
        data_whitelisted = config['whiteListedDomains']

        message = " ".join(arg for arg in args)
        urls = self.extract_links(message)

        for url in urls:
            if url in data:
                # remove url from list
                data.remove(url)

                removeblack_success_embed = discord.Embed(
                    title = "**Domain Removed Successfully**",
                    description = f"🦅: Successfully removed `{url}` from `black-listed` "\
                        "domains list.",
                    color = 0x00FF00    # Green
                )

                updateConfig(ctx.guild.id, config)
                await ctx.channel.send(embed = removeblack_success_embed)

            elif url in data_whitelisted:
                removeblack_whitelisted_embed = discord.Embed(
                    title = "**Domain Not Found**",
                    description = f"🦅: Given domain `{url}` is not `black-listed`."\
                        f"\nHowever it is `white-listed`, use `~removewhite {url}` to remove.",
                    color = 0xedbe13    # yellow
                )

                await ctx.channel.send(embed = removeblack_whitelisted_embed)
            
            else:
                removeblack_notfound_embed = discord.Embed(
                    title = "**Domain Not Found**",
                    description = f"🦅: Give domain `{url}` is neither `black-listed` nor "\
                        "`white-listed`",
                    color = 0xFF0000    # Red
                )

                await ctx.channel.send(embed = removeblack_notfound_embed)


    @commands.command(name="getblack")
    async def getblack(self, ctx):
        """
        Return all domains that are not allowed by admins
        in the server.
        """

        # get config file
        config = getConfig(ctx.guild.id)
        data = config['blackListedDomains']

        if data:
            domains = "\n".join(url for url in data)

            getblack_domains_embed = discord.Embed(
                title = "**Black Listed Domains ❌**",
                description = f"🦅: These are the domains which are not allowed in **{ctx.guild.name}**:\n ```{domains}```",
                color = 0x000000
            )

            await ctx.channel.send(embed = getblack_domains_embed)
        else:
            getblack_notfound_embed = discord.Embed(
                title = "**Error 404**",
                description = f"🦅: Looks like **{ctx.guild.name}** don't have any black-listed domain.",
                color = 0xFF0000
            )

            await ctx.channel.send(embed = getblack_notfound_embed)


# Setup
def setup(bot):
    bot.add_cog(Domains(bot))