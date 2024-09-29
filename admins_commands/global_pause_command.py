import os
import asyncio
from data.constants import *
from functions.check_admin import is_admin
from data.system_variables import *
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def global_pause(ctx, duration: int = None):
    """Pause the bot globally for 'duration' seconds or indefinitely if no duration is specified"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")
    
    global GLOBAL_PAUSE

    if is_admin(ctx.author.id):
        if not GLOBAL_PAUSE:
            GLOBAL_PAUSE = 1
            save_vars(glopa=GLOBAL_PAUSE)

            if duration:
                await ctx.reply(f"Bot will be paused for {duration} seconds.")
                logger.info(f"Bot will be paused for {duration} seconds.")

                await asyncio.sleep(duration)

                GLOBAL_PAUSE = 0
                save_vars(glopa=GLOBAL_PAUSE)

                await ctx.send("Bot is now active again!")
                logger.info("Bot is now active again!")

            else:
                await ctx.reply("Bot has been paused indefinitely.")
                logger.info("Bot has been paused indefinitely.")
        else:
            await ctx.reply("The bot is already paused.")
            logger.info("The bot is already paused.")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        logger.warning(f"{ctx.author.name} does not have sufficient permissions to execute the command.")