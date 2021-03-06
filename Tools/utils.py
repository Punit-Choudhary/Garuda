import json

def getConfig(guildID, ctx=None):
    """Open Config file of Guild"""

    with open("config.json", 'r') as file:
        data = json.load(file)
    
    if str(guildID) not in data["guilds"]:
        # Create configuration for new guild
        defaultConfig = {
            "name": f"{ctx.guild.name}",
            "prefix": "~",
            "antiSpam": True,
            "antiLink": True,
            "whiteListedDomains": [],
            "blackListedDomains": []
        }

        updateConfig(guildID, defaultConfig)
        return getConfig(guildID)
    else:
        return data["guilds"][str(guildID)]


def updateConfig(guildID, data):
    with open("config.json", 'r') as file:
        config = json.load(file)
    
    config["guilds"][str(guildID)] = data
    updated_data = json.dumps(config, indent=4, ensure_ascii=False)

    with open("config.json", 'w') as file:
        file.write(updated_data)


async def get_prefix(bot, message) -> str:
    if not message.guild:
        return "~"
    else:
        data = getConfig(message.guild.id, ctx=message)
        return data["prefix"]