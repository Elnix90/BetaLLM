import json
import os

from init_logger import setup_logger
logger = setup_logger(os.path.splitext(os.path.basename(__file__))[0])

ALLOWED_CHANNELS_KEY = "ALLOWED_CHANNELS_IDS"
ALLOWED_DM_KEY = "ALLOWED_DM_IDS"
ADMINS_USERS_KEY = "ADMINS_USERS_IDS"
PENDING_REQUEST_KEY = "PENDING_REQUEST"
GLOBAL_PAUSE_KEY = "GLOBAL_PAUSE"
CURRENT_MODEL_KEY = "CURRENT_MODEL"

def load_vars():
    try:
        with open("data/vars.json", "r") as f:
            data = json.load(f)
        logger.info("Variables loaded successfully from vars.json")
        return data
    except FileNotFoundError:
        logger.warning("vars.json not found. Initializing with default values.")
        return {
            ALLOWED_CHANNELS_KEY: [],
            ALLOWED_DM_KEY: [],
            ADMINS_USERS_KEY: [],
            PENDING_REQUEST_KEY: [],
            GLOBAL_PAUSE_KEY: 0,
            CURRENT_MODEL_KEY: 0
        }
    except json.JSONDecodeError:
        logger.error("Error decoding vars.json. Initializing with default values.")
        return {
            ALLOWED_CHANNELS_KEY: [],
            ALLOWED_DM_KEY: [],
            ADMINS_USERS_KEY: [],
            PENDING_REQUEST_KEY: [],
            GLOBAL_PAUSE_KEY: 0,
            CURRENT_MODEL_KEY: 0
        }

def save_vars(wlch=None,wldm=None,admin=None,pending=None,glopa=None,curmo=None):
    data = load_vars()
    
    if wlch is not None:
        data[ALLOWED_CHANNELS_KEY] = wlch
        logger.info(f"Updated ALLOWED_CHANNELS_IDS: {wlch}")
    if wldm is not None:
        data[ALLOWED_DM_KEY] = wldm
        logger.info(f"Updated ALLOWED_DM_IDS: {wldm}")
    if admin is not None:
        data[ADMINS_USERS_KEY] = admin
        logger.info(f"Updated ADMINS_USERS_IDS: {admin}")
    if pending is not None:
        data[PENDING_REQUEST_KEY] = pending
        logger.info(f"Updated PENDING_REQUEST: {pending}")
    if glopa is not None:
        data[GLOBAL_PAUSE_KEY] = glopa
        logger.info(f"Updated GLOBAL_PAUSE: {glopa}")
    if curmo is not None:
        data[CURRENT_MODEL_KEY] = curmo
        logger.info(f"Updated CURRENT_MODEL: {curmo}")

    try:
        with open("data/vars.json", "w") as f:
            json.dump(data, f, indent=4)
        logger.info("Variables saved successfully to vars.json")
    except IOError:
        logger.error("Error writing to vars.json")

logger.info("Loading variables...")
variables = load_vars()
ALLOWED_CHANNELS_IDS = variables[ALLOWED_CHANNELS_KEY]
ALLOWED_DM_IDS = variables[ALLOWED_DM_KEY]
ADMINS_USERS_IDS = variables[ADMINS_USERS_KEY]
PENDING_REQUEST = variables[PENDING_REQUEST_KEY]
GLOBAL_PAUSE = variables[GLOBAL_PAUSE_KEY]
CURRENT_MODEL = variables[CURRENT_MODEL_KEY]
logger.info("Variables loaded and initialized")
