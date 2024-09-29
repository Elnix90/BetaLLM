import os
from data.system_variables import *
from data.constants import *
from functions.check_admin import is_admin
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def wlch(ctx):
    """Add channel to the whitelist if admin, else ask for admin approval to whitelist the channel"""
    logger.info(f"{ctx.author.name} used {ctx.message.content}")

    user_id = ctx.author.id
    channel_id = ctx.channel.id
    is_dm = isinstance(ctx.channel, discord.DMChannel)

    if is_admin(user_id):
        if is_dm:
            if channel_id not in ALLOWED_DM_IDS:
                ALLOWED_DM_IDS.append(channel_id)
                save_vars(wldm=ALLOWED_DM_IDS)
                await ctx.reply(f"DM {ctx.channel.name} (ID: {channel_id}) added to the whitelist.")
                logger.info(f"DM {ctx.channel.name} (ID: {channel_id}) added to the whitelist")
            else:
                await ctx.reply("This DM is already in the whitelist.")
                logger.info("This DM is already in the whitelist")
        else:
            if channel_id not in ALLOWED_CHANNELS_IDS:
                ALLOWED_CHANNELS_IDS.append(channel_id)
                save_vars(wlch=ALLOWED_CHANNELS_IDS)
                await ctx.reply(f"Channel {ctx.channel.name} (ID: {channel_id}) added to the whitelist by admin {user_id}.")
                logger.info(f"Channel {ctx.channel.name} (ID: {channel_id}) added to the whitelist by admin {user_id}")
            else:
                await ctx.reply("This channel is already in the whitelist.")
                logger.info("This channel is already in the whitelist")
        
        if channel_id in PENDING_REQUEST:
            PENDING_REQUEST.remove(channel_id)
            save_vars(pending=PENDING_REQUEST)
    else:
        if (is_dm and channel_id not in ALLOWED_DM_IDS) or (not is_dm and channel_id not in ALLOWED_CHANNELS_IDS):
            if channel_id not in PENDING_REQUEST:
                PENDING_REQUEST.append(channel_id)
                save_vars(pending=PENDING_REQUEST)
                
                admin_dm = await bot.fetch_user(permanent_admin)
                message = await admin_dm.send(f"Whitelist request for {'DM' if is_dm else 'channel'} {channel_id} by user {ctx.author.name} (ID: {user_id}). React with ✅ to accept or ❌ to refuse.")
                
                await message.add_reaction(ACCEPT_EMOJI)
                await message.add_reaction(REFUSE_EMOJI)
                
                await ctx.reply("Your whitelist request has been sent to the administrator.")
                logger.info(f"Whitelist request for {'DM' if is_dm else 'channel'} {channel_id} sent by user {user_id}")
                
                def check(reaction, user):
                    return user.id == permanent_admin and str(reaction.emoji) in [ACCEPT_EMOJI, REFUSE_EMOJI] and reaction.message.id == message.id
                
                try:
                    reaction, _ = await bot.wait_for('reaction_add', check=check)
                    if str(reaction.emoji) == ACCEPT_EMOJI:
                        if is_dm:
                            ALLOWED_DM_IDS.append(channel_id)
                            save_vars(wldm=ALLOWED_DM_IDS)
                        else:
                            ALLOWED_CHANNELS_IDS.append(channel_id)
                            save_vars(wlch=ALLOWED_CHANNELS_IDS)
                        PENDING_REQUEST.remove(channel_id)
                        save_vars(pending=PENDING_REQUEST)

                        await ctx.reply(f"{ACCEPT_EMOJI} : Whitelist request for {'DM' if is_dm else 'channel'} {channel_id} accepted.")
                        logger.info(f"Whitelist request for {'DM' if is_dm else 'channel'} {channel_id} accepted")
                    else:
                        PENDING_REQUEST.remove(channel_id)
                        save_vars(pending=PENDING_REQUEST)

                        await ctx.reply(f"{REFUSE_EMOJI} : Whitelist request for {'DM' if is_dm else 'channel'} {channel_id} refused.")
                        logger.info(f"Whitelist request for {'DM' if is_dm else 'channel'} {channel_id} refused")

                except Exception as e:
                    logger.error(f"Error while waiting for reaction: {e}")
            else:
                await ctx.reply("A whitelist request for this channel is already pending.")
                logger.info("A whitelist request for this channel is already pending")
        else:
            await ctx.reply("This channel is already in the whitelist.")
            logger.info("This channel is already in the whitelist")
