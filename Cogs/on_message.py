from dis import dis
from pydoc import describe
import re
import logging
import discord
from random import choice
from discord.ext import commands
from rich.logging import RichHandler

from Tools.utils import getConfig, get_prefix
from datetime import datetime


# setting up logging
FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%x]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


class OnMessageCog(commands.Cog):
    """
    Contain on_message function to watch messages
    """
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_message(self, message):

        # Don't reply/watch messages from bots
        if message.author.bot:
            return
                

        # Check for mention
        if self.bot.user.mentioned_in(message):
            responses = ["what's up?", "what happend kid?", "Hello 👋", "I am watching 👁‍🗨", "How are you doing?", "Feeling safe?", "Everything OK?"]

            reply = discord.Embed(
                title = "Garuda 🦅",
                description = f"🦅: {choice(responses)}, Btw all commands are available at `{await get_prefix(self.bot, message)}help`",
                color = 0xFFFF00
            )

            await message.channel.send(embed = reply)

        # Don't watch Admin's messages        
        if message.author.guild_permissions.administrator:
            return


        # Config
        config = getConfig(message.guild.id)

        # Anti-Spam
        if config["antiSpam"]:
            def check(message):
                return (message.author == message.author and (datetime.utcnow() - message.created_at).seconds < 15)
        
            if len(list(filter(lambda x: check(x), self.bot.cached_messages))) >= 8 and len(list(filter(lambda x: check(x), self.bot.cached_messages))) < 12:
                spam_warn_embed = discord.Embed(
                    title = f"STOP SPAMMING {message.author}",
                    description = "🦅: Stop Spamming Kiddo! 👁",
                    color = 0xFF0000    # Red
                )

                await message.channel.send(embed = spam_warn_embed)
            elif len(list(filter(lambda x: check(x), self.bot.cached_messages))) >= 10:
                spam_kick_embed_dm = discord.Embed(
                    title = "**You Have Been Kicked 👢**",
                    description = f"🦅: You have been kicked out of the {message.author.guild.name} Server\nReason: Spamming",
                    color = 0xFF0000    # Red
                )
                # send kick notification in User's DM
                await message.author.send(embed = spam_kick_embed_dm)
                # kick the user
                try:
                    await message.author.kick()
                except Exception as e:
                    if isinstance(e, discord.errors.Forbidden):
                        log.warn(f"Kick permission not available!\nGuild: {message.guild}, Author: {message.author.name}, Message: {message.content}")
                        kick_forbidden_embed = discord.Embed(
                            title="Missing Permissions :pleading_face:",
                            description=f"Hey Admins, I don't have permissions to kick the spammer, {message.author.name} :cry:",
                            color=0xFFC0CB
                        )

                        await message.channel.send(embed=kick_forbidden_embed)

                spam_kick_embed = discord.Embed(
                 title = "**User Has Been Kicked 👢**",
                 description = f"🦅: {message.author.mention} has been kicked out,\nReason: Spamming",
                 color = 0x00FF00   # Green
                )
                await message.channel.send(embed = spam_kick_embed)
        
        # Anti-Link
        def extract_urls(message) -> bool:
            regex=r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}'
            urls = re.findall(regex, message.content.lower())
            if urls:
                return urls
            else:
                return []

        if config['antiLink']:
            """
            If anti-link is enabled, allow White-Listed Domains Only!
            Delete the message if any of the url in message is not White-listed.
            """

            whitelisted = config['whiteListedDomains']
            urls = extract_urls(message)

            if urls:
                """
                Check if all links are white-listed
                """

                for url in urls:
                    if url not in whitelisted:
                        await message.delete()
                        await message.channel.send(
                            embed = discord.Embed(
                                title = "**❌ Not Allowed ❌**",
                                description = f"🦅: Hey kiddo {message.author.mention}, Only white-listed links are \
                                    allowed in **{message.guild.name}**\n**Tip:**\
                                    Use `~getwhite` or `~getblack` to view `White-Listed` and \
                                    `Black-Listed` domains.",
                                color = 0xFF0000
                            ), 
                        delete_after = 20
                        )
                        return
        else:
            """
            Delete message containing Blacklisted link
            """
            blacklisted = config['blackListedDomains']
            urls = extract_urls(message)

            if urls:
                for url in urls:
                    if url in blacklisted:
                        await message.delete()
                        await message.channel.send(
                            embed = discord.Embed(
                                title = "**❌ Not Allowed ❌",
                                description = f"🦅: Hey kiddo {message.author.mention}, The link \
                                    you just sent was Black-Listed, don't repeat that again!\n \
                                    **Tip:** Use `~getwhite` or `~getblack` to view `White-Listed` and \
                                    `Black-Listed` domains.",
                                color = 0xFF0000
                            ),
                        delete_after = 20
                        )
                        return




# Setup bot
def setup(bot):
    bot.add_cog(OnMessageCog(bot))
