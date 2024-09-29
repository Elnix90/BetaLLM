import os
from data.system_variables import *
from data.constants import *
from functions.check_admin import is_admin
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def remove_admin(ctx, user: discord.User):
    """Remove mentioned admin from the admin users list"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):
        user_id = user.id
        if user_id in ADMINS_USERS_IDS:
            ADMINS_USERS_IDS.remove(user_id)
            save_vars(admin=ADMINS_USERS_IDS)

            await ctx.reply(f"User {user.mention} has been removed as an admin by {ctx.author.mention}")
            logger.info(f"User {user.mention} has been removed as an admin by {ctx.author.mention}")

        else:
            await ctx.reply(f"{user.mention} is not an admin.")
            logger.info(f"{user.mention} is not an admin.")

    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        logger.warning(f"{ctx.author.name} does not have sufficient permissions to execute the command.")
