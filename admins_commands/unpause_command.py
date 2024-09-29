import os
from data.constants import *
from functions.check_admin import is_admin
from data.system_logs import *
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def unpause(ctx):
    """Unpause the bot if it's paused in the current channel"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):
        data = load_logs(ctx)
        PAUSE_BOT = data["PAUSE"]

        if PAUSE_BOT:
            PAUSE_BOT = 0
            save_logs(ctx, pause=PAUSE_BOT)
            
            await ctx.reply("Bot pause has been manually cancelled in this channel.")
            logger.info(f"Bot pause has been manually cancelled in channel {ctx.channel.id}")
        else:
            await ctx.reply("The bot isn't paused in this channel.")
            logger.info(f"Attempted to unpause bot in channel {ctx.channel.id}, but it wasn't paused")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        logger.warning(f"{ctx.author.name} does not have sufficient permissions to execute the unpause command.")