import asyncio
import toml
import discord
from discord.ext import commands
from discord import app_commands

# Load the configuration from TOML file
config_path = "/data/config.toml"
config = toml.load(config_path)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Global variables to store the current status and activity
current_activity = None
current_status = None

async def update_presence():
    global current_activity, current_status

    # Load activity and status from TOML configuration
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
        new_activity = discord.CustomActivity(name=name)
    else:
        activity_type_enum = activity_types.get(activity_type, discord.ActivityType.playing)
        new_activity = discord.Activity(type=activity_type_enum, name=name)

    status_type = config["discord_settings"].get("status_ind", "online").lower()
    status_types = {
        "online": discord.Status.online,
        "idle": discord.Status.idle,
        "dnd": discord.Status.dnd,
    }
    new_status = status_types.get(status_type, discord.Status.online)

    # Check if the current status and activity need to be updated
    if current_activity != new_activity or current_status != new_status:
        await bot.change_presence(activity=new_activity, status=new_status)
        current_activity = new_activity
        current_status = new_status

async def presence_checker():
    while True:
        await update_presence()
        await asyncio.sleep(30)  # Adjust the check interval as needed

@bot.event
async def on_ready():
    global current_activity, current_status
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()
    print("Commands synced successfully.")

    # Initialize the current activity and status based on config
    await update_presence()

    # Start the presence checker task
    bot.loop.create_task(presence_checker())

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
        new_activity = discord.CustomActivity(name=name)
    else:
        activity_type_enum = activity_types.get(activity_type.lower(), discord.ActivityType.playing)
        new_activity = discord.Activity(type=activity_type_enum, name=name)

    # Save the activity status to the configuration file
    config["discord_settings"]["status_message"] = f"{activity_type}: {name}"
    with open(config_path, "w") as f:
        toml.dump(config, f)

    # Set activity without changing the status
    await bot.change_presence(activity=new_activity, status=current_status)
    current_activity = new_activity

    await interaction.response.send_message(f"Activity updated to {activity_type} '{name}'.", ephemeral=True)

@bot.tree.command(name="setstatus", description="Change the bot's status")
@app_commands.describe(status="Status to set: online, idle, dnd")
async def set_status(interaction: discord.Interaction, status: str):
    allowed_user_ids = config["discord_settings"].get("admin_ids", [])
    if interaction.user.id not in allowed_user_ids:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    status_types = {
        "online": discord.Status.online,
        "idle": discord.Status.idle,
        "dnd": discord.Status.dnd,
    }

    status_value = status.lower()
    if status_value not in status_types:
        await interaction.response.send_message(f"Invalid status: {status}. Please use online, idle, or dnd.", ephemeral=True)
        return

    # Save the status to the configuration file
    config["discord_settings"]["status_ind"] = status_value
    with open(config_path, "w") as f:
        toml.dump(config, f)

    # Set status without changing the activity
    await bot.change_presence(activity=current_activity, status=status_types[status_value])
    current_status = status_types[status_value]

    await interaction.response.send_message(f"Status updated to {status}.", ephemeral=True)

async def main():
    global current_activity, current_status
    # Initialize activity and status based on config
    await update_presence()
    await bot.start(config["discord_settings"]["bot_token"])

asyncio.run(main())
