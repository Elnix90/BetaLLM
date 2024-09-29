from data.constants import *
from functions.check_admin import is_admin

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = None):
    """CLear amount of messages in context channel or clear everything if amount not specified"""
    print(f"{ctx.author.name} used {ctx.message.content}")
    
    if amount is None:
        await ctx.channel.purge()
        print("Tous les messages ont été effacés\n")

    else:
        messages = await ctx.channel.history(limit=None).flatten()
        total_messages = len(messages)
            
        if amount > total_messages:
            await ctx.channel.purge()
            print("Tous les messages ont été effacés\n")
            
        else:
            deleted = await ctx.channel.purge(limit=amount + 1)
            print(f"{amount} messages ont été effacés\n")