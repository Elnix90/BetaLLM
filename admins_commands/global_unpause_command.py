import os
from data.constants import *
from functions.check_admin import is_admin
from data.system_variables import *
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def global_unpause(ctx):
    """Unpause the bot globally if it's currently paused"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")
    
    global GLOBAL_PAUSE

    if is_admin(ctx.author.id):
        if GLOBAL_PAUSE:
            GLOBAL_PAUSE = 0
            save_vars(glopa=GLOBAL_PAUSE)
            
            await ctx.reply("Bot pause has been manually cancelled.")
            logger.info("Bot pause has been manually cancelled.")

        else:
            await ctx.reply("The bot isn't paused.")
            logger.info("The bot isn't paused.")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        logger.warning(f"{ctx.author.name} does not have sufficient permissions to execute the command.")
