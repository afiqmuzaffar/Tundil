from backend.chatbot_api.Bot.model import User
from backend.chatbot_api import Server
from backend.chatbot_model import tundil_brain

class Brain(object):

    def __init__(self):
        self.db = Server().db

    def keygen(self):
        import random, string
        return ''.join(random.choice(string.ascii_letters+string.digits) for i in range(10)).lower()

    def user_validation(self,apikey):
        fetch = self.db.session.query(User).filter_by(apikey = apikey).count()
        if fetch == 0:
            return False
        else:
            return True

    def user_register(self,name,phone):
        key= self.keygen()
        try:
            user_req = User(key,name,phone)
            self.db.session.add(user_req)
            self.db.session.commit()
            self.db.session.close()

        except Exception as e:
            return e

        else:
            return key

    def tundil_bot(self,user_query):
        bot_instance = tundil_brain.Tundil_bot()
        return bot_instance.inference_reply(user_query)
        # return str(bot_instance.inference_reply(user_query)+self.computing_usage())

    def computing_usage(self):
        import psutil, os
        process = psutil.Process(os.getpid())
        ram = process.memory_info().rss
        return '{}MB RAM used on Server.'.format(ram/1048576)