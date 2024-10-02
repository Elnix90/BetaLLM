import discord
from discord.ext import commands
import aiohttp
import os

from data.system_logs import *
from data.constants import *
from data.keys import *
from data.system_variables import *
from events.check_members_clicked_on_react import *
from send_large_mesage import *
from server_logs import *

from admins_commands.add_admin_command import *
from admins_commands.blch_command import *
from admins_commands.global_pause_command import *
from admins_commands.global_unpause_command import *
from admins_commands.pause_command import *
from admins_commands.remove_admin_command import *
from admins_commands.reset_command import *
from admins_commands.unpause_command import *

from commands.admin_list_command import *
from commands.clear_command import *
from commands.get_infos_command import *
from commands.nick_command import *
from commands.set_history_command import *
from commands.switch_api_command import *
from commands.switch_model_command import *
from commands.toggle_history_command import *
from commands.wlch_command import *

from init_logger import setup_logger
logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

#############################################################################
#                                                                           #
#                           on_ready EVENT                                  #
#                     Say connected when is online                          #
#############################################################################

@bot.event
async def on_ready():
    logger.info(f"The bot is connected as {bot.user}")
    print("Bot connected!")
    
    # Envoie d'un message dans un salon spécifique
    channel = bot.get_channel(1287054887024328766)
    if channel:
        await channel.send("Test message: Bot is now connected!")
    
    user = bot.get_user(703604544348749994)
    if user:
        try:
            await user.send("Hello! The bot is now connected.")
            logger.info(f"DM sent to user {user.id}")
        except Exception as e:
            logger.error(f"Failed to send DM to user {user.id}: {e}")
    
    # Assigner des rôles aux membres
    await give_member_role()
    logger.info("Member roles have been assigned")


#############################################################################
#                                                                           #
#                           on reaction EVENT                               #
#                Add 'Member' role if reacted to rules message              #
#############################################################################

@bot.event
async def on_raw_reaction_add(payload):
    if payload.guild_id is None:
        return

    guild = bot.get_guild(payload.guild_id)
    
    role = discord.utils.get(guild.roles, id=ROLE_ID)
    if role is None:
        logger.warning(f"Role {ROLE_NAME} not found")
        return

    if payload.message_id == MESSAGE_ID and str(payload.emoji) == ACCEPT_EMOJI:
        member = guild.get_member(payload.user_id)
        if member is not None:
            await member.add_roles(role)
            logger.info(f"Role {role.name} assigned to {member.name}")
        else:
            logger.warning(f"Member with ID {payload.user_id} not found")

#############################################################################
#                                                                           #
#                        ANSWER ON COMMAND ERROR                            #
#                                                                           #
#############################################################################

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        logger.warning(f"Command not found: {ctx.message.content}")
        await ctx.reply("Command not found. Use `%help` to see the list of commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        logger.warning(f"Missing argument for command: {ctx.command}")
        await ctx.reply(f"Missing required argument for the command. Use `%help {ctx.command}` for proper usage.")
    else:
        logger.error(f"An error occurred: {error}")
        await ctx.reply(f"An error occurred: {error}")

#############################################################################
#                                                                           #
#                              API REQUEST                                  #
#           Send a request to openrouter's API to get a response            #
#############################################################################

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    if ctx.content.startswith("%"):
        logger.info(f"Message starts with command: {ctx.content} -> processing")
        await bot.process_commands(ctx)
        return
    elif bot.user in ctx.mentions:
        logger.info(f"Message started as a question: {ctx.content} -> sending request to API")
        if GLOBAL_PAUSE and not is_admin(ctx.author.id):
            await ctx.reply("Global pause is enabled. Only admins can use me at the moment.")
            logger.info("Global pause is enabled, request from non-admin user rejected")
            return
        data = load_logs(ctx)
        if data["PAUSE"] == True and not is_admin(ctx.author.id):
            await ctx.reply("Pause is enabled in this channel. You can ask an admin or wait for a while.")
            logger.info("Channel pause is enabled, request from non-admin user rejected")
            return

        if (ctx.channel.id in ALLOWED_CHANNELS_IDS or
            (isinstance(ctx.channel, discord.DMChannel) and ctx.channel.id in ALLOWED_DM_IDS)):
            question = ctx.content.replace(f"<@{bot.user.id}>", "").strip()
            if question:
                url = "https://openrouter.ai/api/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {OPENROUTER_API_KEYS[CURRENT_API]}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": free_models_list[CURRENT_MODEL],
                    "messages": [{"role": "system", "content": "Tu es BetaLLM, created by Elnix. Réponds précisément et de manière concise."}]
                }
                past_interactions = get_past_interactions(ctx)
                data['messages'].extend(past_interactions)
                data['messages'].append({"role": "user", "content": question})
                try:
                    async with ctx.channel.typing():
                        async with aiohttp.ClientSession() as session:
                            async with session.post(url, headers=headers, json=data) as response:
                                response_data = await response.json()
                                if 'error' in response_data:
                                    error_message = response_data['error'].get('message', 'Unknown error')
                                    error_code = response_data['error'].get('code', 'Unknown code')
                                    error_responses = {
                                        400: "Bad request. Please check your input and try again.",
                                        401: "Unauthorized. There's an issue with the API key.",
                                        402: "I'm sorry, but I've run out of credits. Please contact the bot administrator.",
                                        403: "Forbidden. You don't have permission to use this resource.",
                                        404: "Not found. The requested resource doesn't exist.",
                                        429: "Too many requests. Please try again later.",
                                        500: "Internal server error. The API is having issues.",
                                        503: "Service unavailable. The API is currently down for maintenance."
                                    }
                                    user_message = error_responses.get(error_code, f"An unexpected error occurred: {error_message}")
                                    await ctx.channel.send(user_message)
                                    logger.error(f"API Error: Code {error_code}, Message: {error_message}")
                                    return
                                bot_response = response_data['choices'][0]['message']['content']
                                # Send the bot response in chunks if it exceeds Discord's character limit
                                await log_to_server(ctx, question, bot_response)
                                await send_large_message(ctx, bot_response)

                                logs_to_save = {"user_id": ctx.author.id, "user_message": question, "bot_response": bot_response}
                                save_logs(ctx, logs=logs_to_save)
                                logger.info(f"Response sent and logs saved for channel {ctx.channel.id}")
                except Exception as e:
                    await ctx.channel.send(f"An error occurred while calling the API: {e}")
                    logger.error(f"Error during API call: {e}")
        elif (ctx.author != bot.user) and (bot.user in ctx.mentions):
            await ctx.channel.send("This Channel/DM is not whitelisted. You can ask an admin to whitelist your channel using '%wlch'.")
            logger.warning(f"Attempt to use bot in non-whitelisted channel: {ctx.channel.id}")

bot.run(DISCORD_TOKEN)