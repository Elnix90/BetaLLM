import os
from data.constants import *
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, user: discord.Member, *, nickname: str = None):
    """Change nickname of mentioned user to given string, or reset to original nickname if no string is provided"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")
    
    name = user.display_name
    try:
        await user.edit(nick=nickname)
        if nickname:
            await ctx.reply(f"{name}'s nickname has been changed to {nickname}.")
            logger.info(f"{name}'s nickname has been changed to {nickname}")
        else:
            await ctx.reply(f"{user.display_name}'s nickname has been reset.")
            logger.info(f"{user.display_name}'s nickname has been reset")
    except Exception as e:
        await ctx.reply(f"Error: {e}")
        logger.error(f"Error changing nickname: {e}")
