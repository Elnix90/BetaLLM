import os
from data.constants import *
from data.system_variables import *
from functions.check_admin import is_admin
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def switch_model(ctx, n: int = None):
    """Change the AI model used to generate responses"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):
        global CURRENT_MODEL

        if n is not None:
            if 0 <= n < len(free_models_list):
                CURRENT_MODEL = n
                save_vars(curmo=CURRENT_MODEL)
            else:
                await ctx.reply(f"Invalid model number. Please choose between 0 and {len(free_models_list) - 1}.")
                logger.warning(f"Invalid model number {n} provided by {ctx.author.name}")
                return
        else:
            CURRENT_MODEL = (CURRENT_MODEL + 1) % len(free_models_list)
        
        save_vars(curmo=CURRENT_MODEL)
        await ctx.reply(f"My model is now {free_models_list[CURRENT_MODEL]}.")
        logger.info(f"AI model switched to {free_models_list[CURRENT_MODEL]} by {ctx.author.name}")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        logger.warning(f"{ctx.author.name} does not have sufficient permissions to execute the switch_model command.")
