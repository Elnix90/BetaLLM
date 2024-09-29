from data.system_variables import *
from data.constants import *
from functions.check_admin import is_admin

@bot.command()
async def add_admin(ctx, user: discord.User):
    """Promote mentionned user to let him use all bot commands"""
    print(f"{ctx.author.name} used {ctx.message.content}")
    
    if is_admin(ctx.author.id):
        user_id = user.id
        if user_id not in ADMINS_USERS_IDS:

            ADMINS_USERS_IDS.append(user_id)
            save_vars(admin=ADMINS_USERS_IDS)

            await ctx.reply(f"User {user.mention} has been added as an admin by {ctx.author.mention}")
            print          (f"User {user.mention} has been added as an admin by {ctx.author.mention}")

        else:
            await ctx.reply(f"{user_id} is already an admin.")
            print          (f"{user_id} is already an admin.")

    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        print(f"{ctx.author.name} n'a pas les autorisations suffisantes pour executer la commande.\n")