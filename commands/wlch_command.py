from data.system_variables import *
from data.constants import *
from functions.check_admin import is_admin

@bot.command()
async def wlch(ctx):
    """Add channel to the whitelist if admin, else, ask the admin his approbation to whitelist channel"""
    print(f"{ctx.author.name} used {ctx.message.content}")

    user_id = ctx.author.id
    channel_id = ctx.channel.id
    is_dm = isinstance(ctx.channel, discord.DMChannel)

    if is_admin(user_id):
        if is_dm:
            if channel_id not in ALLOWED_DM_IDS:
                ALLOWED_DM_IDS.append(channel_id)
                save_vars(wldm=ALLOWED_DM_IDS)

                await ctx.reply(f"DM {ctx.channel.name} (ID: {channel_id}) ajouté à la whitelist.")
                print          (f"DM {ctx.channel.name} (ID: {channel_id}) ajouté à la whitelist\n")

            else:

                await ctx.reply("Ce DM est déjà dans la whitelist.")
                print          ("Ce DM est déjà dans whitelist\n")
        else:
            if channel_id not in ALLOWED_CHANNELS_IDS:
                ALLOWED_CHANNELS_IDS.append(channel_id)
                save_vars(wlch=ALLOWED_CHANNELS_IDS)

                await ctx.reply(f"Salon {ctx.channel.name} (ID: {channel_id}) aouté à la whitelist par l'admin {user_id}.")
                print          (f"Salon {ctx.channel.name} (ID: {channel_id}) aouté à la whitelist par l'admin {user_id}\n")

            else:

                await ctx.reply("Ce salon est déjà dans la whitelist.")
                print          ("Ce salon est déjà dans la whitelist\n")

        
        if channel_id in PENDING_REQUEST:
            PENDING_REQUEST.remove(channel_id)
            save_vars(pending=PENDING_REQUEST)
    else:
        if (is_dm and channel_id not in ALLOWED_DM_IDS) or (not is_dm and channel_id not in ALLOWED_CHANNELS_IDS):
            if channel_id not in PENDING_REQUEST:
                PENDING_REQUEST.append(channel_id)
                save_vars(pending=PENDING_REQUEST)
                
                admin_dm = await bot.fetch_user(permanent_admin)

                message = await admin_dm.send(f"Demande de whitelist pour {'le DM' if is_dm else 'le salon'} {channel_id} par l'utilisateur {ctx.author.name} (ID: {user_id}). Réagissez avec ✅ pour accepter ou ❌ pour refuser.")
                
                await message.add_reaction(ACCEPT_EMOJI)
                await message.add_reaction(REFUSE_EMOJI)
                
                await ctx.reply("Votre demande de whitelist a été envoyée à l'administrateur.")
                print(f"Demande de whitelist pour {'le DM' if is_dm else 'le salon'} {channel_id} envoyée par l'utilisateur {user_id}")
                
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

                        await ctx.reply(f"{ACCEPT_EMOJI} : Demande de whitelist pour {'le DM' if is_dm else 'le salon'} {channel_id} acceptée.")
                        print          (f"Demande de whitelist pour {'le DM' if is_dm else 'le salon'} {channel_id} acceptée\n")

                    else:
                        PENDING_REQUEST.remove(channel_id)
                        save_vars(pending=PENDING_REQUEST)

                        await ctx.reply(f"{REFUSE_EMOJI} : Demande de whitelist pour {'le DM' if is_dm else 'le salon'} {channel_id} refusée.")
                        print          (f"Demande de whitelist pour {'le DM' if is_dm else 'le salon'} {channel_id} refusée\n")

                except Exception as e:

                    print(f"Erreur lors de l'attente de la réaction : {e}")
            else:
                await ctx.reply("Une demande de whitelist pour ce salon est déjà en attente.")
                print          ("Une demande de whitelist pour ce salon est déjà en attente\n")
        else:
            await ctx.reply("Ce salon est déjà dans la whitelist.")
            print          ("Ce salon est déjà dans la whitelist\n")
