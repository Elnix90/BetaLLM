import os
from data.constants import *
from data.keys import *
from data.system_variables import *
from functions.check_admin import is_admin
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def switch_api(ctx, n: int = None):
    """Change the AI API used to generate responses"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):  # Changed ctx to ctx.author.id
        global CURRENT_API

        if n is not None:
            if 0 <= n < len(OPENROUTER_API_KEYS):  # Changed condition for better readability
                CURRENT_API = n
                save_vars(curapi=CURRENT_API)
            else:
                await ctx.reply(f"Invalid API number. Please choose between 0 and {len(OPENROUTER_API_KEYS) - 1}.")
                logger.warning(f"Invalid API number {n} provided by {ctx.author.name}")
                return
        else:
            CURRENT_API = (CURRENT_API + 1) % len(OPENROUTER_API_KEYS)
        
        save_vars(curapi=CURRENT_API)  # Save the changes even when cycling through APIs
        await ctx.reply(f"My API is now {OPENROUTER_API_KEYS[CURRENT_API][:15]}...")
        logger.info(f"AI API switched to {OPENROUTER_API_KEYS[CURRENT_API][:15]}... by {ctx.author.name}")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        logger.warning(f"{ctx.author.name} does not have sufficient permissions to execute the switch_api command.")