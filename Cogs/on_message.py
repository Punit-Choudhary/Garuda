import discord
from random import choice
from discord.ext import commands

from Tools.utils import getConfig
from datetime import datetime


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
                description = f"🦅: {choice(responses)}, Btw all commands are available at `~help`",
                color = 0xFFFF00
            )
            await message.channel.send(embed = reply)
        

        # Config
        config = getConfig(message.guild.id)

        # Anti-Spam
        if config["antiSpam"]:
            def check(message):
                return (message.author == message.author and (datetime.utcnow() - message.created_at).seconds < 15)
        
            if len(list(filter(lambda x: check(x), self.bot.cached_messages))) >= 5 and len(list(filter(lambda x: check(x), self.bot.cached_messages))) < 9:
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
                await message.author.kick()

                spam_kick_embed = discord.Embed(
                 title = "**User Has Been Kicked 👢**",
                 description = f"🦅: {message.author.mention} has been kicked out,\nReason: Spamming",
                 color = 0x00FF00   # Green
                )
                await message.channel.send(embed = spam_kick_embed)


# Setup bot
def setup(bot):
    bot.add_cog(OnMessageCog(bot))
