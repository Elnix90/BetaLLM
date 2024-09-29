from data.system_variables import *
from data.constants import *
from functions.check_admin import is_admin

@bot.command()
async def remove_admin(ctx, user: discord.User):
    """Remove mentionned admin from admin users list"""
    print(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):
        user_id = user.id
        if user_id in ADMINS_USERS_IDS:

            ADMINS_USERS_IDS.remove(user_id)
            save_vars(admin=ADMINS_USERS_IDS)

            await ctx.reply(f"User {user.mention} has been removed as an admin by {ctx.author.mention}")
            print          (f"User {user.mention} has been removed as an admin by {ctx.author.mention}\n")

        else:
            await ctx.reply(f"{user_id} is not an admin.")
            print          (f"{user_id} is not an admin.\n")

    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        print(f"{ctx.author.name} n'a pas les autorisations suffisantes pour executer la commande.\n")