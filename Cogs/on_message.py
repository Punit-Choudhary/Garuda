import re
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

            if message.author.id != 742931080096776242:
                reply = discord.Embed(
                    title = "Garuda 🦅",
                    description = f"🦅: {choice(responses)}, Btw all commands are available at `~help`",
                    color = 0xFFFF00
                )
            else:
                latency = round(self.bot.latency * 1000, 2)
                reply = discord.Embed(
                    title = "Garuda 🦅",
                    description = f"🦅: I am active & doing my job,\nlatency: {latency}ms",
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
        
        # Anti-Link
        if config['antiLink']:
            def check_link(message) -> bool:
                regex=r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
                urls = re.findall(regex, message.content.lower())
                if urls:
                    return True
                else:
                    return False
            
            if check_link(message):
                # delete the message if that contains link
                await message.delete()
                
                links_delete_embed = discord.Embed(
                    title = "**No Links!**",
                    description = f"🦅: {message.author.mention}, you are not allowed to send links here!",
                    color = 0xFF0000    # Red
                )
                await message.channel.send(embed = links_delete_embed, delete_after=10)



# Setup bot
def setup(bot):
    bot.add_cog(OnMessageCog(bot))
