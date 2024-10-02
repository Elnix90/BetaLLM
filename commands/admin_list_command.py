import os
from data.system_variables import *
from data.constants import *
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def admin_list(ctx):
    """Display the list of administrators for the bot"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")

    message = "Here is the list of my administrators:\n"
    
    # Add permanent admin
    permanent_admin_user = await bot.fetch_user(permanent_admin)
    message += f"- **{permanent_admin_user.name}** (ID: {permanent_admin})\n"
    
    # Add other admins
    for admin_id in ADMINS_USERS_IDS:
        try:
            admin_user = await bot.fetch_user(admin_id)
            message += f"- **{admin_user.name}** (ID: {admin_id})\n"
        except Exception as e:
            logger.error(f"Error fetching user with ID {admin_id}: {str(e)}")
            message += f"- Unknown User (ID: {admin_id})\n"
    
    await ctx.reply(message)
    logger.info(message)
