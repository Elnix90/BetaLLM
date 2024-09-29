from data.constants import *
from functions.check_admin import is_admin
from data.system_logs import *

@bot.command()
async def toggle_history(ctx):
    """Toggle messages history for the channel"""
    print(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):
        data = load_logs(ctx)
        HISTORY = data["HISTORY"]
        HISTORY = not HISTORY
        save_logs(ctx,history=HISTORY)

        await ctx.reply(f"History **{'ENABLED' if HISTORY else 'DISABLED'}**")
        print          (f"History {'ENABLED' if HISTORY else 'DISABLED'}")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        print(f"{ctx.author.name} n'a pas les autorisations suffisantes pour executer la commande.\n")