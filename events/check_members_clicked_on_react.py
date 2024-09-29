import discord
from discord.ext import commands
from data.constants import *

async def give_member_role():
    GUILD_ID = 1286313400447668369
    MESSAGE_ID = 1286947250949591070
    ROLE_NAME = "Membre"

    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print("Serveur introuvable !")
        return
    
    
    for channel in guild.text_channels:
        try:
            message = await channel.fetch_message(MESSAGE_ID)
            break
        except discord.NotFound:
            continue

    if message is None:
        print("Message introuvable !")
        return

    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    if role is None:
        print(f"Le rôle {ROLE_NAME} n'existe pas sur ce serveur !")
        return


    for reaction in message.reactions:
        async for user in reaction.users():
            if user.bot:
                continue
            
            member = guild.get_member(user.id)
            if member is not None and role not in member.roles:
                try:
                    await member.add_roles(role)
                    print(f"Rôle '{ROLE_NAME}' attribué à {member.display_name}.")
                except discord.Forbidden:
                    print(f"Impossible d'attribuer le rôle à {member.display_name} (permissions manquantes).")
