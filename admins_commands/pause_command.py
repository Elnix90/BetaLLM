from data.constants import *
from functions.check_admin import is_admin
from data.system_logs import *
import asyncio

@bot.command()
async def pause(ctx, duration: int = None):
    """Pause the bot  in context channel for 'duration' or indefinitely if not duration"""
    print(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):

        data = load_logs(ctx)
        PAUSE_BOT = data["PAUSE"]

        if not PAUSE_BOT:
            PAUSE_BOT = True
            save_logs(ctx,pause=PAUSE_BOT)

            if duration:
                await ctx.reply(f"Bot will be paused for {duration} seconds in this channel.")
                print         (f"Bot will be paused for {duration} seconds in this channel.\n")

                await asyncio.sleep(duration)

                PAUSE_BOT = False
                save_logs(ctx,pause=PAUSE_BOT)

                await ctx.send("Bot is now active again in this channel!")
                print         ("Bot is now active again in this channel!\n")

            else:
                await ctx.reply("Bot has been paused indefinitely in this channel.")
                print         ("Bot has been paused indefinitely in this channel.\n")
        else:
            await ctx.reply("The bot is already paused in this channel.")
            print         ("The bot is already paused in this channel.\n")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        print(f"{ctx.author.name} n'a pas les autorisations suffisantes pour executer la commande.\n")