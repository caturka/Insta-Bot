
from config import Config

class Auth_user:
    
    def search_auth(authid):
        auth_list=Config.AUTH
        default = Config.OWNER
        try:
            for id in range(len(auth_list)):
                if auth_list[id] == authid:
                    return str(authid)
            return str(default)
        except:
            pass

#GROUP chat AUTH
class Auth_chat:

    def search_chat(chatid):
        group_list = Config.GROUP
        default=-1001192804366
        try:
            for id in range(len(group_list)):
                if group_list[id] == chatid:
                    return str(chatid)  
            return str(default)     
        except:
           pass 

