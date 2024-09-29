import discord
import json
import os

from init_logger import setup_logger
logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])


def get_file_path(ctx):
    if not os.path.exists("logs"):
        os.makedirs("logs")
        logger.info("Created 'logs' directory")
    
    if isinstance(ctx.channel, discord.DMChannel):
        prefix = "dm"
    elif isinstance(ctx.channel, discord.TextChannel):
        prefix = "ch"
    else:
        prefix = "uk"
    
    filepath = f"logs/{prefix}_{ctx.channel.id}_logs.json"
    logger.debug(f"File path generated: {filepath}")
    return filepath

def load_logs(ctx):
    filepath = get_file_path(ctx)
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        logger.info(f"Logs loaded successfully from {filepath}")
        return data
    except FileNotFoundError:
        logger.warning(f"Log file not found: {filepath}. Initializing with default values.")
        return {
            "HISTORY": True,
            "MAX_HISTORY": 5,
            "PAUSE": False,
            "LOGS": []
        }
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {filepath}. Initializing with default values.")
        return {
            "HISTORY": True,
            "MAX_HISTORY": 5,
            "PAUSE": False,
            "LOGS": []
        }

def save_logs(ctx, history=None, maxhistory=None, pause=None, logs=None):
    filename = get_file_path(ctx)
    data = load_logs(ctx)

    if history is not None:
        data["HISTORY"] = history
        logger.info(f"Updated HISTORY: {history}")
    if maxhistory is not None:
        data["MAX_HISTORY"] = maxhistory
        logger.info(f"Updated MAX_HISTORY: {maxhistory}")
    if pause is not None:
        data["PAUSE"] = pause
        logger.info(f"Updated PAUSE: {pause}")
    if logs is not None:
        data["LOGS"].append(logs)
        logger.info(f"Added new log entry")

    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Successfully updated {filename}")
    except IOError:
        logger.error(f"Error writing to {filename}")

def get_past_interactions(ctx):
    filename = get_file_path(ctx)
    data = load_logs(ctx)

    HISTORY = data["HISTORY"]
    MAX_HISTORY = data["MAX_HISTORY"]
    LOGS = data["LOGS"]
    
    if not HISTORY:
        logger.info("History is disabled, returning empty list")
        return []
    
    past_interactions = []
    for log in LOGS:
        past_interactions.append({
            "role": "user", 
            "content": log['user_message']
        })
        past_interactions.append({
            "role": "assistant", 
            "content": log['bot_response']
        })

    if len(past_interactions) >= MAX_HISTORY:
        logger.info(f"Returning last {MAX_HISTORY} interactions")
        return past_interactions[-MAX_HISTORY:]
    else:
        logger.info(f"Returning all {len(past_interactions)} interactions")
        return past_interactions
