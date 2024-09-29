import os
from data.constants import *
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = None):
    """Clear specified amount of messages in the context channel or clear everything if amount not specified"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")
    
    try:
        if amount is None:
            deleted = await ctx.channel.purge(limit=None)
            logger.info(f"All messages have been deleted. Total: {len(deleted)}")
        else:
            deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
            logger.info(f"{len(deleted) - 1} messages have been deleted")  # -1 to exclude the command message
        
        await ctx.send(f"{len(deleted)} messages have been deleted.", delete_after=5)
    except discord.errors.Forbidden:
        logger.error("Bot doesn't have permission to delete messages")
        await ctx.send("I don't have permission to delete messages in this channel.", delete_after=5)
    except Exception as e:
        logger.error(f"An error occurred while deleting messages: {str(e)}")
        await ctx.send("An error occurred while trying to delete messages.", delete_after=5)
