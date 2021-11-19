import discord

from discord.ext import commands


class ModerationCog(commands.Cog, name="Moderation Commands"):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="kick", usage="<@member> [reason : optional]")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """
        Kick out a member from server
        """
        if ctx.author.id == member.id:
            kick_fun_embed = discord.Embed(
                title="**Are you OK bro??**",
                description=f"🦅: {ctx.author.mention}, Looks like you need to visit a psychiatrist\n\
                    Here is the [contact info](https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley)",
                color = 0x7716f5    # Purple
            )
            await ctx.channel.send(embed = kick_fun_embed)
            return

        try:
            kick_dm_embed = discord.Embed(
                title="**You Have Been Kicked Out**",
                description=f"🦅: You have been kicked out of the **{ctx.guild.name}\n**\
                    {'Because: ' + str(reason) if reason != None else ''}",
                color = 0xFF0000    # Red
            )

            await member.send(embed = kick_dm_embed)

            await member.kick(reason=reason)

            kick_embed = discord.Embed(
                title = f"**Kicked {member.display_name}**",
                color = 0x00FF00    # Green
            )
            kick_embed.add_field(name="Kicked Member 👢", value=member.display_name)
            kick_embed.add_field(name="Kicked By", value=ctx.author.mention)
            kick_embed.set_footer(text=f"Reason: {reason}")

            await ctx.send(embed = kick_embed)
        except Exception as e:
            print(e)


    @commands.command(name="ban", usage="<@member> [reason : optional]")
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """
        Ban a member from server
        """
        if ctx.author.id == member.id:
            ban_fun_embed = discord.Embed(
                title="**Are you OK bro??**",
                description=f"🦅: {ctx.author.mention}, Looks like you need to visit a psychiatrist\n\
                    Here is the [contact info](https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley)",
                color = 0x7716f5    # Purple
            )
            await ctx.channel.send(embed = ban_fun_embed)
            return

        try:
            ban_dm_embed = discord.Embed(
                title="**You Have Been Banned**",
                description=f"🦅: You have been Banned from **{ctx.guild.name}\n**\
                    {'Because: ' + str(reason) if reason != None else ''}",
                color = 0xFF0000    # Red
            )

            await member.send(embed = ban_dm_embed)

            await member.ban(reason=reason)

            ban_embed = discord.Embed(
                title = f"**Banned {member.display_name}**",
                color = 0x00FF00    # Green
            )
            ban_embed.add_field(name="Banned Member 🚫", value=member.display_name)
            ban_embed.add_field(name="Banned By", value=ctx.author.mention)
            ban_embed.set_footer(text=f"Reason: {reason}")
            ban_embed.set_thumbnail(url="https://media.tenor.co/videos/16d1dd77408db03a6c78210391957fc5/mp4")

            await ctx.send(embed = ban_embed)
        except Exception as e:
            print(e)
    

    @commands.command(name="clear", usage="<number of messages> | default 100")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=100):
        """
        Purge requested no. of messages from channel.
        """
        await ctx.channel.purge(limit=int(amount) + 1)

        clear_embed = discord.Embed(
            title="Message deleted!",
            description=f"🦅: I've purged {amount} messages | **{ctx.author.name}**",
            color=0x00FF00  # Green
        )

        await ctx.channel.send(embed=clear_embed, delete_after=10)
    


# Setup
def setup(bot):
    bot.add_cog(ModerationCog(bot))