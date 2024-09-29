import os
import asyncio
from data.constants import *
from functions.check_admin import is_admin
from data.system_logs import *
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def pause(ctx, duration: int = None):
    """Pause the bot in the context channel for 'duration' seconds or indefinitely if no duration is specified"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):
        data = load_logs(ctx)
        PAUSE_BOT = data["PAUSE"]

        if not PAUSE_BOT:
            PAUSE_BOT = True
            save_logs(ctx, pause=PAUSE_BOT)

            if duration:
                await ctx.reply(f"Bot will be paused for {duration} seconds in this channel.")
                logger.info(f"Bot will be paused for {duration} seconds in this channel.")

                await asyncio.sleep(duration)

                PAUSE_BOT = False
                save_logs(ctx, pause=PAUSE_BOT)

                await ctx.send("Bot is now active again in this channel!")
                logger.info("Bot is now active again in this channel!")

            else:
                await ctx.reply("Bot has been paused indefinitely in this channel.")
                logger.info("Bot has been paused indefinitely in this channel.")
        else:
            await ctx.reply("The bot is already paused in this channel.")
            logger.info("The bot is already paused in this channel.")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        logger.warning(f"{ctx.author.name} does not have sufficient permissions to execute the command.")
