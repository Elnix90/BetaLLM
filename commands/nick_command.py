from data.constants import *
from functions.check_admin import is_admin

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, user: discord.Member, *, nickname: str = None):
    """change nickane of mentionned user to string given, else reset original nickname"""
    print(f"{ctx.author.name} used {ctx.message.content}")
    
    name = user.display_name
    try:
        await user.edit(nick=nickname)
        if nickname:
            await ctx.reply(f"Le pseudo de {name} a été changé en {nickname}.")
            print          (f"Le pseudo de {name} a été changé en {nickname}\n")
        else:
            await ctx.reply(f"Le pseudo de {user.display_name} a été réinitialisé.")
            print          (f"Le pseudo de {user.display_name} a été réinitialisé\n")
    except Exception as e:
        await ctx.reply(f"Error : {e}")
        print          (f"Error : {e}")