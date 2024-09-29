import discord
from discord.ext import commands

# Api and keys
#OPENROUTER_API_KEY = "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"
#OPENROUTER_API_KEY = "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" #yoann
OPENROUTER_API_KEY = "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"
DISCORD_TOKEN = "MTI4Njk1MTU5ODk1ODA1MTM3MQ.GPzUcY.cxlEDrA0zdCTEGSaIbXK5nt9HDCGEgyUKqqL2Y"

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
