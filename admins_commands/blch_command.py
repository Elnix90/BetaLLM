from data.system_variables import *
from data.constants import *
from functions.check_admin import is_admin

@bot.command()
async def blch(ctx):
    """Remove context channel from the whitelisted channel list"""
    print(f"{ctx.author.name} used {ctx.message.content}")

    user_id = ctx.author.id
    channel_id = ctx.channel.id
    is_dm = isinstance(ctx.channel, discord.DMChannel)

    if is_admin(user_id):
        if is_dm:
            if channel_id in ALLOWED_DM_IDS:
                ALLOWED_DM_IDS.remove(channel_id)
                save_vars(wldm=ALLOWED_DM_IDS)

                await ctx.reply(f"DM {ctx.channel.name} (ID: {channel_id}) retiré de la whitelist.")
                print          (f"DM {ctx.channel.name} (ID: {channel_id}) retiré de la whitelist.\n")

            else:
                
                await ctx.reply("Ce DM n'est pas dans la whitelist.")
                print          ("Ce DM n'est pas dans la whitelist\n")
                
        else:
            if channel_id in ALLOWED_CHANNELS_IDS:
                    ALLOWED_CHANNELS_IDS.remove(channel_id)
                    save_vars(wlch=ALLOWED_CHANNELS_IDS)

                    await ctx.reply(f"Salon {ctx.channel.name} (ID: {channel_id}) retiré de la whitelist.")
                    print          (f"Salon {ctx.channel.name} (ID: {channel_id}) retiré de la whitelist.\n")

            else:
                await ctx.reply("Ce salon n'est pas dans la whitelist.")
                print          ("Ce salon n'est pas dans la whitelist.\n")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        print(f"{ctx.author.name} n'a pas les autorisations suffisantes pour executer la commande.\n")