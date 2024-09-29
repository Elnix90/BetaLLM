import os
from data.constants import *
from functions.check_admin import is_admin
from data.system_logs import *
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def toggle_history(ctx):
    """Toggle message history for the channel"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):
        data = load_logs(ctx)
        HISTORY = data["HISTORY"]
        HISTORY = not HISTORY
        save_logs(ctx, history=HISTORY)

        status = "ENABLED" if HISTORY else "DISABLED"
        await ctx.reply(f"History **{status}**")
        logger.info(f"History {status} for channel {ctx.channel.id}")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        logger.warning(f"{ctx.author.name} does not have sufficient permissions to execute the command.")