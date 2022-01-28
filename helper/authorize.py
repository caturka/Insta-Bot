from config import Config
import ast
class Auth_user:
    
    def search_auth(authid):
        AUTH = [Config.AUTH]
        a ='[%s]' % ', '.join(map(str, AUTH))
        AUTH = ast.literal_eval(a)
        default = Config.OWNER
        try:
            for id in range(len(AUTH)):
                if AUTH[id] == authid:
                    return str(authid)
            return str(default)
        except:
            pass

#GROUP chat AUTH
class Auth_chat:

    def search_chat(chatid):
        GROUP = [Config.GROUP]
        a ='[%s]' % ', '.join(map(str, GROUP))
        GROUP = ast.literal_eval(a)
        default=-1001192804366
        try:
            for id in range(len(GROUP)):
                if GROUP[id] == chatid:
                    return str(chatid)  
            return str(default)     
        except:
           pass 
