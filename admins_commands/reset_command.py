import os
from data.constants import *
from functions.check_admin import is_admin
from data.system_logs import get_file_path

@bot.command()
async def reset(ctx):
    """Erase log file for the context channel to reset bot's memory"""
    print(f"{ctx.author.name} used {ctx.message.content}")

    if is_admin(ctx.author.id):
        filename = get_file_path(ctx)
        try:
            if os.path.exists(filename):
                os.remove(filename)
                await ctx.reply(f"Les logs du {'DM' if isinstance(ctx.channel, discord.DMChannel) else 'salon'} ID {ctx.channel.id} ont été réinitialisés !")
                print          (f"Les logs du {'DM' if isinstance(ctx.channel, discord.DMChannel) else 'salon'} ID {ctx.channel.id} ont été réinitialisés")
            else:
                await ctx.reply(f"Aucun fichier de logs trouvé pour ce {'DM' if isinstance(ctx.channel, discord.DMChannel) else 'salon'}.")
                print          (f"Aucun fichier de logs trouvé pour ce {'DM' if isinstance(ctx.channel, discord.DMChannel) else 'salon'}\n")
        except Exception as e:
            await ctx.reply(f"Une erreur est survenue lors de la réinitialisation des logs : {e}")
            print          (f"Une erreur est survenue lors de la réinitialisation des logs : {e}\n")
    else:
        await ctx.reply(NO_PERMISSION_DENY_MESSAGE)
        print(f"{ctx.author.name} n'a pas les autorisations suffisantes pour executer la commande.\n")