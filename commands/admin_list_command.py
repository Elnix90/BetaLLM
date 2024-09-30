import os
from data.system_variables import *
from data.constants import *
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def admin_list(ctx):
    """Show the list of admin for the bot"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")

    message = "Here is the list of my admins:\n - **" + permanent_admin + "**\n"
    for admin in ADMINS_USERS_IDS:
        message += " - **" + str(ADMINS_USERS_IDS[admin]) + "**\n"
    
    await ctx.reply(message)
    logger.info(message)