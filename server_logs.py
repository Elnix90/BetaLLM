from data.constants import *
from send_large_mesage import *
from datetime import datetime
import os

from init_logger import setup_logger
logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

async def log_to_server(ctx, user_message, bot_response):
    server_logs_guild_id = SERVER_LOGS_ID  # ID du serveur de logs

    # Obtenir le serveur de logs
    logs_guild = bot.get_guild(server_logs_guild_id)
    if not logs_guild:
        logger.error("Logging guild not found!")
        return

    # Créer un nom unique pour le canal de logs
    if isinstance(ctx.channel, discord.DMChannel):
        channel_name = f"DM-{ctx.author.name}-{ctx.author.id}"
    else:
        channel_name = f"{ctx.channel.name}-{ctx.guild.name}"

    # Nettoyer le nom du canal pour respecter les règles de Discord
    channel_name = ''.join(c for c in channel_name if c.isalnum() or c in ['-', '_']).lower()
    channel_name = channel_name[:100]  # Limiter à 100 caractères

    # Chercher ou créer le canal de logs
    log_channel = discord.utils.get(logs_guild.text_channels, name=channel_name)
    if not log_channel:
        log_channel = await logs_guild.create_text_channel(channel_name)
        logger.info(f"Created new log channel: {channel_name}")

    # timestamp
    ts = f"<t:{int(datetime.now().timestamp())}:F>"

    # Envoyer les messages de logs
    await send_large_message(log_channel, f"**User Request: {ts}**\n{user_message}\n**Bot Response:  {ts}**",False)
    await send_large_message(log_channel, f"{bot_response}",False)

    logger.info(f"Logged message in channel: {channel_name}")
