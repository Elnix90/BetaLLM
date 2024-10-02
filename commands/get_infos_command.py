import os
import aiohttp
from data.constants import *
from data.keys import *
from data.system_variables import *
from init_logger import setup_logger

logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

@bot.command()
async def get_infos(ctx):
    """Get detailed information about the API key and current model"""
    
    url = "https://openrouter.ai/api/v1/auth/key"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEYS[CURRENT_API]}"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                
                # API key information
                info_message = (
                    f"**Label**: {data['data']['label']}\n"
                    f"**Usage**: {data['data']['usage']} credits\n"
                    f"**Limit**: {data['data']['limit'] or 'Unlimited'} credits\n"
                    f"**Remaining credits**: {data['data']['limit'] - data['data']['usage'] if data['data']['limit'] else 'Unlimited'} credits\n"
                    f"**Free tier**: {'Yes' if data['data']['is_free_tier'] else 'No'}\n"
                    f"**Rate limit**: {data['data']['rate_limit']['requests']} requests per {data['data']['rate_limit']['interval']}\n"
                )
                
                # Token information
                if 'token_usage' in data['data']:
                    info_message += (
                        f"**Tokens used**: {data['data']['token_usage']['total']}\n"
                        f"**Input tokens**: {data['data']['token_usage']['prompt']}\n"
                        f"**Output tokens**: {data['data']['token_usage']['completion']}\n"
                    )
                
                # Currently used model
                info_message += f"\n**Current model**: {free_models_list[CURRENT_MODEL]}"
                
                logger.info(info_message)
                await ctx.reply(info_message)
            else:
                error_message = f"Error: {response.status}\n{await response.text()}"
                logger.error(error_message)
                await ctx.reply(error_message)
