import discord
import aiohttp
import json
from data.constants import *

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

DISCORD_TOKEN = DISCORD_TOKEN
OPENROUTER_API_KEY = OPENROUTER_API_KEY
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

@client.event
async def on_ready():
    print(f'Bot connecté en tant que {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ask '):
        query = message.content[5:]
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": query}]
            }
            
            try:
                async with session.post(OPENROUTER_URL, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        answer = data['choices'][0]['message']['content']
                        await message.channel.send(f"Réponse: {answer}")
                    else:
                        error_data = await response.text()
                        await message.channel.send(f"Erreur lors de la requête à l'API. Statut: {response.status}, Détails: {error_data}")
            except aiohttp.ClientError as e:
                await message.channel.send(f"Une erreur s'est produite lors de la connexion à l'API: {str(e)}")
            except json.JSONDecodeError:
                await message.channel.send("Erreur lors du décodage de la réponse JSON de l'API.")
            except Exception as e:
                await message.channel.send(f"Une erreur inattendue s'est produite: {str(e)}")

client.run(DISCORD_TOKEN)

