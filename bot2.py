import os
import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread

# ===== Webserver für Render =====
app = Flask('')

@app.route('/')
def home():
    return "Bot ist online!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# ===== Discord Bot =====
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} ist online!")
    await bot.change_presence(activity=discord.Game(name="Überwacht deinen Server"))
    try:
        await bot.tree.sync()
        print("Slash Commands synchronisiert!")
    except Exception as e:
        print(e)

# Beispiel Slash Command Kick
@bot.tree.command(name="kick", description="Kickt ein Mitglied")
@app_commands.describe(member="Mitglied", reason="Grund")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if interaction.user.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member} gekickt!")
    else:
        await interaction.response.send_message("Keine Berechtigung!", ephemeral=True)

# ========= REAKTIONSROLLEN =========

ROLE_MESSAGE_ID = 0  # HIER KOMMT GLEICH DIE NACHRICHTEN-ID REIN
ROLE_NAME = "Mitglied"  # Muss exakt wie die Rolle heißen
ROLE_EMOJI = "✅"

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != ROLE_MESSAGE_ID:
        return

    guild = bot.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    member = guild.get_member(payload.user_id)

    if member is None or member.bot:
        return

    if str(payload.emoji) == ROLE_EMOJI:
        await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != ROLE_MESSAGE_ID: 1443304975110377532
        return

    guild = bot.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    member = guild.get_member(payload.user_id)

    if member is None or member.bot:
        return

    if str(payload.emoji) == ROLE_EMOJI:
        await member.remove_roles(role)

@bot.tree.command(name="welcome", description="Begrüßt ein neues Mitglied")
@app_commands.describe(member="Das neue Mitglied")
async def welcome(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(
        f"👋 Willkommen auf dem Server, {member.mention}!"
    )


@bot.tree.command(name="hilfe", description="Zeigt alle Bot-Befehle an")
async def hilfe(interaction: discord.Interaction):
    text = (
        "🤖 **Bot-Hilfe – Alle Befehle:**\n\n"
        "🔧 **Moderation:**\n"
        "/kick @User [Grund] – Kickt ein Mitglied\n"
        "/ban @User [Grund] – Bannt ein Mitglied\n\n"
        "👋 **Begrüßung:**\n"
        "/welcome @User – Begrüßt ein neues Mitglied manuell\n\n"
        "🎭 **Rollen:**\n"
        "Reagiere mit ✅ auf die Rollen-Nachricht, um die Rolle zu bekommen\n\n"
        "✅ **Status:**\n"
        "Der Bot zeigt dauerhaft: *Überwacht deinen Server*"
        "ban und kick command  
    )

    await interaction.response.send_message(text, ephemeral=True)



























# Bot starten
import os
bot.run(os.getenv("DISCORD_TOKEN"))

