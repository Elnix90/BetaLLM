from data.constants import *
from functions.check_admin import is_admin
from data.system_logs import *

@bot.command()
async def unpause(ctx):
    """Unpause the bot if it's paused"""
    print(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):

        data = load_logs(ctx)
        PAUSE_BOT = data["PAUSE"]

        if PAUSE_BOT:
            PAUSE_BOT = 0
            save_logs(ctx,pause=PAUSE_BOT)
            
            await ctx.reply("Bot pause has been manually cancelled.")
            print         ("Bot pause has been manually cancelled.\n")

        else:
            await ctx.reply("The bot isn't paused in this channel.")
            print         ("The bot isn't paused in this channel.\n")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        print(f"{ctx.author.name} n'a pas les autorisations suffisantes pour executer la commande.\n")