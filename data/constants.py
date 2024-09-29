import discord
from discord.ext import commands

# Free models list
free_models_list = [
    "meta-llama/llama-3.1-8b-instruct:free",
    "meta-llama/llama-3.2-11b-vision-instruct:free",
    "nousresearch/hermes-3-llama-3.1-405b:free",
    "google/gemini-flash-1.5-exp",
    "google/gemini-flash-8b-1.5-exp"

]

# Messages
NO_PERMISSION_DENY_MESSAGE = "Vous n'avez pas l'autorisation d'exécuter cette commande."




# Role react on Minecraft/wlch
ACCEPT_EMOJI = "✅"
REFUSE_EMOJI = "❌"
GUILD_ID = 1286313400447668369
MESSAGE_ID = 1286947250949591070
ROLE_NAME = "Membre"
ROLE_ID = 1286315681536675957


# Permanent admin users id:
permanent_admin = 1154096065411297402


# Discord Intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix="%", intents=intents)
