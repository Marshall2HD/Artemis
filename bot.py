import asyncio
import os
import discord
from discord.ext import commands
from discord import app_commands

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_activity = None
        self.current_status = discord.Status.online

    async def set_activity(self, activity_type: str, name: str):
        activity_types = {
            "playing": discord.ActivityType.playing,
            "streaming": discord.ActivityType.streaming,
            "listening": discord.ActivityType.listening,
            "watching": discord.ActivityType.watching,
            "custom": None
        }
        activity_type_enum = activity_types.get(activity_type.lower(), discord.ActivityType.playing)

        if activity_type_enum is None:
            self.current_activity = discord.CustomActivity(name=name)
        else:
            self.current_activity = discord.Activity(type=activity_type_enum, name=name)

        await self.change_presence(activity=self.current_activity, status=self.current_status)

    async def set_status(self, status: str):
        status_types = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd
        }
        status_value = status.lower()
        if status_value not in status_types:
            raise ValueError(f"Invalid status: {status}. Please use online, idle, or dnd.")

        self.current_status = status_types[status_value]
        await self.change_presence(activity=self.current_activity, status=self.current_status)

# Load configuration from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_ACTIVITY_TYPE = os.getenv("BOT_ACTIVITY_TYPE", "playing").lower()
BOT_ACTIVITY = os.getenv("BOT_ACTIVITY", "with the settings")
STATUS_IND = os.getenv("STATUS_IND", "online").lower()

# Admin IDs from environment variables (comma-separated)
ADMIN_IDS = {int(id) for id in os.getenv("ADMIN_IDS", "").split(',') if id.isdigit()}

intents = discord.Intents.default()
intents.message_content = True
bot = MyBot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()
    print("Commands synced successfully.")
    await bot.set_activity(BOT_ACTIVITY_TYPE, BOT_ACTIVITY)
    await bot.set_status(STATUS_IND)

@bot.tree.command(name="setactivity", description="Change the bot's activity status")
@app_commands.describe(activity_type="Type of activity: playing, streaming, listening, watching, custom", name="Name of the activity")
async def set_activity(interaction: discord.Interaction, activity_type: str, name: str):
    if interaction.user.id not in ADMIN_IDS:
        return await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

    try:
        await bot.set_activity(activity_type, name)
        await interaction.response.send_message(f"Activity updated to {activity_type} '{name}'.", ephemeral=True)
    except ValueError as e:
        await interaction.response.send_message(str(e), ephemeral=True)

@bot.tree.command(name="setstatus", description="Change the bot's status")
@app_commands.describe(status="Status to set: online, idle, dnd")
async def set_status(interaction: discord.Interaction, status: str):
    if interaction.user.id not in ADMIN_IDS:
        return await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

    try:
        await bot.set_status(status)
        await interaction.response.send_message(f"Status updated to {status}.", ephemeral=True)
    except ValueError as e:
        await interaction.response.send_message(str(e), ephemeral=True)

@bot.tree.command(name="createwebhook", description="Create a WebHook")
@app_commands.describe(name="The name of the webhook")
async def createwebhook(interaction: discord.Interaction, name: str):
    if interaction.user.id not in ADMIN_IDS:
        return await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

    if not interaction.guild.me.guild_permissions.manage_webhooks:
        return await interaction.response.send_message('The MANAGE_WEBHOOKS permission is required to create a webhook.', ephemeral=True)

    try:
        webhook = await interaction.channel.create_webhook(name=name)
        await interaction.response.send_message(f'Webhook created! {webhook.url}', ephemeral=True)
    except Exception as e:
        print(f'Error creating webhook: {e}')
        await interaction.response.send_message('There was an error creating the webhook.', ephemeral=True)

async def main():
    await bot.start(BOT_TOKEN)

asyncio.run(main())
