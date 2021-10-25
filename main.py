import os
from random import choice
import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("TOKEN")

# Setting up Discord Intents
intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(
    command_prefix = ">",
    intents = intents,
    case_insensitivity = True,
    strip_after_prefix = True
)


@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        response = ["what's up?", "what happend kid?", "Hello 👋", "I am watching 👁‍🗨", "How are you doing?", "Feeling safe?", "Everything OK?"]
        await message.channel.send(f"🦅: {choice(response)}, Btw all commands are available at `>help`")


@bot.event
async def on_ready():
    print(f"{bot.user} 🦅 is active now ✅")
    await bot.change_presence(
        activity = discord.Activity(
            type = discord.ActivityType.watching,
            name = "You 👁‍🗨"
        )
    )


# Running the Bot
bot.run(TOKEN)
