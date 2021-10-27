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
    command_prefix = "~",
    intents = intents,
    case_insensitivity = True,
    strip_after_prefix = True
)


# Loading Cogs
for cog in os.listdir("Cogs"):
    if cog.startswith("__pycache__"):
        print("Skipping __pycache__ folder")
    else:
        try:
            bot.load_extension(f"Cogs.{cog[:-3]}")
            print(f"Loaded {cog[:-3]} ✅")
        except Exception as e:
            print(f"Failed to load {cog[:-3]}, error: {e}")


@bot.event
async def on_ready():
    print(f"{bot.user} 🦅 is active now 😎")
    await bot.change_presence(
        activity = discord.Activity(
            type = discord.ActivityType.watching,
            name = "You 👁‍🗨"
        )
    )


# Running the Bot
bot.run(TOKEN)
