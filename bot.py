import asyncio
import toml
import discord
from discord.ext import commands
from discord import app_commands


# Load the configuration from TOML file
config = toml.load("/data/config.toml")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()
    print("Commands synced successfully.")

    # Set activity based on TOML configuration
    status_message = config["discord_settings"].get("status_message", "playing: Default Game")
    activity_parts = status_message.split(": ", 1)
    if len(activity_parts) != 2:
        print(f"Invalid status_message format: {status_message}")
        return

    activity_type, name = activity_parts
    activity_type = activity_type.lower()  # Convert to lowercase for comparison
    activity_types = {
        "playing": discord.ActivityType.playing,
        "streaming": discord.ActivityType.streaming,
        "listening": discord.ActivityType.listening,
        "watching": discord.ActivityType.watching,
    }

    if activity_type == "custom":
        activity = discord.CustomActivity(name=name)
    else:
        activity_type_enum = activity_types.get(activity_type, discord.ActivityType.playing)
        activity = discord.Activity(type=activity_type_enum, name=name)
    
    await bot.change_presence(activity=activity)

@bot.tree.command(name="setactivity", description="Change the bot's activity status")
@app_commands.describe(activity_type="Type of activity: playing, streaming, listening, watching, custom", name="Name of the activity")
async def set_activity(interaction: discord.Interaction, activity_type: str, name: str):
    allowed_user_ids = config["discord_settings"].get("admin_ids", [])
    if interaction.user.id not in allowed_user_ids:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    activity_types = {
        "playing": discord.ActivityType.playing,
        "streaming": discord.ActivityType.streaming,
        "listening": discord.ActivityType.listening,
        "watching": discord.ActivityType.watching,
        "custom": None  # Special case for custom activity
    }

    if activity_type == "custom":
        activity = discord.CustomActivity(name=name)
    else:
        activity_type_enum = activity_types.get(activity_type.lower(), discord.ActivityType.playing)
        activity = discord.Activity(type=activity_type_enum, name=name)

    await bot.change_presence(activity=activity)

    # Save the activity status to the configuration file
    config["discord_settings"]["status_message"] = f"{activity_type}: {name}"
    with open("config.toml", "w") as f:
        toml.dump(config, f)

    await interaction.response.send_message(f"Activity updated to {activity_type} '{name}'.", ephemeral=True)

async def main():
    await bot.start(config["discord_settings"]["bot_token"])

asyncio.run(main())
