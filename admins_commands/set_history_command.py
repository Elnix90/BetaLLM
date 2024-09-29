from data.system_variables import *
from data.constants import *
from functions.check_admin import is_admin
from data.system_logs import *

@bot.command()
async def set_history(ctx, value: int = 5):
    """Set the HISTORY value for the logs in the channel."""
    print(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):

        data = load_logs(ctx)

        if value > 30:
            value = 30
        if value < 0:
            value = 1

        data["MAX_HISTORY"] = value

        await ctx.reply(f"HISTORY has been set to {value} for this channel.")
        print         (f"HISTORY has been set to {value} for this channel.\n")

    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        print(f"{ctx.author.name} n'a pas les autorisations suffisantes pour executer la commande.\n")