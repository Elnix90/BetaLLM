import os
from data.system_variables import *
from data.constants import *
from functions.check_admin import is_admin
from data.system_logs import *
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def set_history(ctx, value: int = 5):
    """Set the HISTORY value for the logs in the channel."""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):
        data = load_logs(ctx)

        value = max(1, min(30, value))

        # data["MAX_HISTORY"] = value
        save_logs(ctx, maxhistory=value)  # Save the updated data

        await ctx.reply(f"HISTORY has been set to {value} for this channel.")
        logger.info(f"HISTORY has been set to {value} for this channel.")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        logger.warning(f"{ctx.author.name} does not have sufficient permissions to execute the command.")
