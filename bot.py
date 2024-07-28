import asyncio, os, toml, discord
from discord.ext import commands
from discord import app_commands

def load_config():
    # Try to load environment variables
    bot_token = os.getenv("DISCORD_BOT_TOKEN")
    status_message = os.getenv("DISCORD_STATUS_MESSAGE", "playing: Default Game")
    admin_ids = os.getenv("DISCORD_ADMIN_IDS", "").split(",")
    if admin_ids:
        admin_ids = list(map(int, admin_ids))
    
    # Fallback to loading from config.toml if environment variables are not set
    if not bot_token or not status_message:
        config = toml.load("config.toml")
        bot_token = bot_token or config["discord_settings"].get("bot_token")
        status_message = status_message or config["discord_settings"].get("status_message", "playing: Default Game")
        admin_ids = admin_ids or list(map(int, config["discord_settings"].get("admin_ids", [])))
    
    return bot_token, status_message, admin_ids

bot_token, status_message, admin_ids = load_config()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()
    print("Commands synced successfully.")

    # Set activity based on configuration
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
    if interaction.user.id not in admin_ids:
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

    # Update the status message environment variable
    os.environ["DISCORD_STATUS_MESSAGE"] = f"{activity_type}: {name}"
    await interaction.response.send_message(f"Activity updated to {activity_type} '{name}'.", ephemeral=True)

async def main():
    await bot.start(bot_token)

asyncio.run(main())
