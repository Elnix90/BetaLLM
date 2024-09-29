from data.constants import permanent_admin
from data.system_variables import ADMINS_USERS_IDS

def is_admin(id):
    if id in ADMINS_USERS_IDS or id == permanent_admin:
        return True
    return False