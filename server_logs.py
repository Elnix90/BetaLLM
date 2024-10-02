from data.constants import *
from send_large_mesage import *
import os

from init_logger import setup_logger
logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

async def log_to_server(ctx, user_message, bot_response):
    # Get or create logging channel
    server_logs_channel_id = SERVER_LOGS_ID  # This should be defined in constants.py
    server_logs_channel = bot.get_channel(server_logs_channel_id)

    if not server_logs_channel:
        logger.error("Logging channel not found!")
        return

    # Create a unique channel name based on context
    if isinstance(ctx.channel, discord.DMChannel):
        channel_name = f"DM du {ctx.author.name} (ID : {ctx.author.id})"
    else:
        channel_name = f"{ctx.channel.name}({ctx.guild.name})"

    # Check if a specific logging channel exists; create if not
    existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    if not existing_channel:
        existing_channel = await ctx.guild.create_text_channel(channel_name)

    # Send formatted messages to logging channel
    await send_large_message(existing_channel, f"*User Request:*\n{user_message}\n*Bot Response:*")
    await send_large_message(existing_channel, f"{bot_response}")
