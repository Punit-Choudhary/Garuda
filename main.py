import os
import logging
import discord

from dotenv import load_dotenv
from discord.ext import commands
from pretty_help import PrettyHelp
from rich.logging import RichHandler

from Tools.utils import get_prefix


# getting environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")
OWNER = os.getenv("OWNER")


# setting up logging
FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%x]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

# Setting up Discord Intents
intents = discord.Intents.default()
intents.members = True
intents.presences = True


bot = commands.Bot(
    
    command_prefix = get_prefix,
    intents = intents,
    case_insensitivity = True,
    strip_after_prefix = True,
    owner_id = OWNER,
    help_command=PrettyHelp()
)


# Loading Cogs
for cog in os.listdir("Cogs"):
    if cog.startswith("__pycache__"):
        log.info("Skipping __pycache__ folder")
    else:
        try:
            bot.load_extension(f"Cogs.{cog[:-3]}")
            log.info(f"Loaded {cog[:-3]} ✅")
        except Exception as e:
            log.fatal(f"Failed to load {cog[:-3]}, error: {e}")


@bot.event
async def on_ready():
    log.info(f"{bot.user} 🦅 is active now 😎")
    await bot.change_presence(
        activity = discord.Activity(
            type = discord.ActivityType.watching,
            name = "You 👁"
        )
    )


# Running the Bot
bot.run(TOKEN)
