from data.constants import *
from data.system_variables import *

@bot.command()
async def switch(ctx, n : int = None):
    """Change the ai model used to gererate a response"""
    print(f"{ctx.author.name} used {ctx.message.content}")

    global CURRENT_MODEL

    if n:
        if n >= 0 and n <= len(free_models_list):
            CURRENT_MODEL = n
            save_vars(curmo=CURRENT_MODEL)
    else:
        CURRENT_MODEL = (CURRENT_MODEL+1) % len(free_models_list)
    
    await ctx.reply(f"My model is now {free_models_list[CURRENT_MODEL]}.")
    print          (f"My model is now {free_models_list[CURRENT_MODEL]}.\n")