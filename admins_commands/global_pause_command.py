from data.constants import *
from functions.check_admin import is_admin
from data.system_variables import *
import asyncio

@bot.command()
async def global_pause(ctx, duration: int = None):
    """Pause the bot everywhere for 'duration' or indefinitely if not duration"""
    print(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):
        if not GLOBAL_PAUSE:
            GLOBAL_PAUSE = 1
            save_vars(glopa=GLOBAL_PAUSE)

            if duration:
                await ctx.reply(f"Bot will be paused for {duration} seconds.")
                print          (f"Bot will be paused for {duration} seconds.\n")

                await asyncio.sleep(duration)

                GLOBAL_PAUSE = 0
                save_vars(glopa=GLOBAL_PAUSE)

                await ctx.send("Bot is now active again!")
                print         ("Bot is now active again!\n")

            else:
                await ctx.reply("Bot has been paused indefinitely.")
                print          ("Bot has been paused indefinitely.\n")
        else:
            await ctx.reply("The bot is already paused.")
            print          ("The bot is already paused.\n")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        print(f"{ctx.author.name} n'a pas les autorisations suffisantes pour executer la commande.\n")