from data.constants import *
from functions.check_admin import is_admin
from data.system_variables import *

@bot.command()
async def global_unpause(ctx):
    """Unpause the bot everywhere if it's paused"""
    print(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):

        if GLOBAL_PAUSE:
            GLOBAL_PAUSE = 0
            save_vars(glopa=GLOBAL_PAUSE)
            
            await ctx.reply("Bot pause has been manually cancelled.")
            print         ("Bot pause has been manually cancelled.\n")

        else:
            await ctx.reply("The bot isn't paused.")
            print         ("The bot isn't paused.\n")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        print(f"{ctx.author.name} n'a pas les autorisations suffisantes pour executer la commande.\n")