import requests
from data.constants import *
from data.keys import *

@bot.command()
async def get_infos(ctx):
    """Get Infos of the Api key"""
    
    url = "https://openrouter.ai/api/v1/auth/key"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        info_message = (
            "Informations sur la clé API :\n"
            f"Label : {data['data']['label']}\n"
            f"Utilisation : {data['data']['usage']} crédits\n"
            f"Limite : {data['data']['limit'] or 'Illimité'} crédits\n"
            f"Tier gratuit : {'Oui' if data['data']['is_free_tier'] else 'Non'}\n"
            f"Limite de taux : {data['data']['rate_limit']['requests']} requêtes par {data['data']['rate_limit']['interval']}"
        )
        
        print(info_message)
        await ctx.reply(info_message)
    else:
        error_message = f"Erreur : {response.status_code}\n{response.text}"
        print(error_message)
        await ctx.reply(error_message)
