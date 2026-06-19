import discord
from discord.ext import commands
from discord import app_commands
import os
import json

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

SETTINGS_FILE = "settings.json"

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

settings = load_settings()

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.tree.command(
    name="channel",
    description="Set the logs channel"
)
async def channel(
    interaction: discord.Interaction,
    channel: discord.TextChannel
):
    settings[str(interaction.guild.id)] = {
        "channel_id": channel.id
    }

    save_settings(settings)

    await interaction.response.send_message(
        f"Logs channel set to {channel.mention}"
    )

@bot.tree.command(
    name="test",
    description="Send a test log"
)
async def test(interaction: discord.Interaction):

    guild = str(interaction.guild.id)

    if guild not in settings:
        await interaction.response.send_message(
            "No channel configured."
        )
        return

    channel_id = settings[guild]["channel_id"]

    log_channel = bot.get_channel(channel_id)

    await log_channel.send(
        "🟢 Test VRChat Log"
    )

    await interaction.response.send_message(
        "Test log sent."
    )

bot.run(TOKEN)
