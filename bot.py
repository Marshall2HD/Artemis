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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()
    print("Commands synced successfully.")

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
        activity = discord.CustomActivity(name=name)
    else:
        activity_type_enum = activity_types.get(activity_type, discord.ActivityType.playing)
        activity = discord.Activity(type=activity_type_enum, name=name)

    status_type = config["discord_settings"].get("status_ind", "online").lower()
    status_types = {
        "online": discord.Status.online,
        "idle": discord.Status.idle,
        "dnd": discord.Status.dnd,
    }
    status = status_types.get(status_type, discord.Status.online)

    await bot.change_presence(activity=activity, status=status)

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

    # Save the activity status to the configuration file
    config["discord_settings"]["status_message"] = f"{activity_type}: {name}"
    with open(config_path, "w") as f:
        toml.dump(config, f)

    # Set activity without changing the status
    current_status = config["discord_settings"].get("status_ind", "online").lower()
    status_types = {
        "online": discord.Status.online,
        "idle": discord.Status.idle,
        "dnd": discord.Status.dnd,
    }
    status = status_types.get(current_status, discord.Status.online)

    await bot.change_presence(activity=activity, status=status)

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
    current_activity = config["discord_settings"].get("status_message", "playing: Default Game")
    activity_parts = current_activity.split(": ", 1)
    if len(activity_parts) != 2:
        activity = None
    else:
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

    await bot.change_presence(activity=activity, status=status_types[status_value])

    await interaction.response.send_message(f"Status updated to {status}.", ephemeral=True)

@bot.tree.command(name="createwebhook", description="Create a WebHook")
@app_commands.describe(name="The name of the webhook")
async def createwebhook(interaction: discord.Interaction, name: str):
    allowed_user_ids = config["discord_settings"].get("admin_ids", [])
    if interaction.user.id not in allowed_user_ids:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    # Check if the bot has permission to manage webhooks
    if not interaction.guild.me.guild_permissions.manage_webhooks:
        await interaction.response.send_message('The MANAGE_WEBHOOKS permission is required to create a webhook.', ephemeral=True)
        return

    try:
        # Create the webhook
        webhook = await interaction.channel.create_webhook(
            name=name,
            avatar=None
        )

        await interaction.response.send_message(f'Webhook created! {webhook.url}', ephemeral=True)
    except Exception as e:
        print(f'Error creating webhook: {e}')
        await interaction.response.send_message('There was an error creating the webhook.', ephemeral=True)

async def main():
    await bot.start(config["discord_settings"]["bot_token"])

asyncio.run(main())
