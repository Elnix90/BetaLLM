import os
from data.system_variables import *
from data.constants import *
from functions.check_admin import is_admin
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def blch(ctx):
    """Remove context channel from the whitelisted channel list"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")

    user_id = ctx.author.id
    channel_id = ctx.channel.id
    is_dm = isinstance(ctx.channel, discord.DMChannel)

    if is_admin(user_id):
        if is_dm:
            if channel_id in ALLOWED_DM_IDS:
                ALLOWED_DM_IDS.remove(channel_id)
                save_vars(wldm=ALLOWED_DM_IDS)

                await ctx.reply(f"DM {ctx.channel.name} (ID: {channel_id}) removed from the whitelist.")
                logger.info(f"DM {ctx.channel.name} (ID: {channel_id}) removed from the whitelist.")

            else:
                await ctx.reply("This DM is not in the whitelist.")
                logger.info("This DM is not in the whitelist.")
                
        else:
            if channel_id in ALLOWED_CHANNELS_IDS:
                ALLOWED_CHANNELS_IDS.remove(channel_id)
                save_vars(wlch=ALLOWED_CHANNELS_IDS)

                await ctx.reply(f"Channel {ctx.channel.name} (ID: {channel_id}) removed from the whitelist.")
                logger.info(f"Channel {ctx.channel.name} (ID: {channel_id}) removed from the whitelist.")

            else:
                await ctx.reply("This channel is not in the whitelist.")
                logger.info("This channel is not in the whitelist.")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        logger.warning(f"{ctx.author.name} does not have sufficient permissions to execute the command.")