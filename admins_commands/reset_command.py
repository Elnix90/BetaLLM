import os
from data.constants import *
from functions.check_admin import is_admin
from data.system_logs import get_file_path
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def reset(ctx):
    """Erase log file for the context channel to reset bot's memory"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):
        filename = get_file_path(ctx)
        try:
            if os.path.exists(filename):
                os.remove(filename)
                channel_type = 'DM' if isinstance(ctx.channel, discord.DMChannel) else 'channel'
                await ctx.reply(f"The logs for the {channel_type} ID {ctx.channel.id} have been reset!")
                logger.info(f"The logs for the {channel_type} ID {ctx.channel.id} have been reset")
            else:
                channel_type = 'DM' if isinstance(ctx.channel, discord.DMChannel) else 'channel'
                await ctx.reply(f"No log file found for this {channel_type}.")
                logger.info(f"No log file found for this {channel_type}")
        except Exception as e:
            await ctx.reply(f"An error occurred while resetting the logs: {e}")
            logger.error(f"An error occurred while resetting the logs: {e}")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        logger.warning(f"{ctx.author.name} does not have sufficient permissions to execute the command.")
