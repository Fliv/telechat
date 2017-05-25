import requests
import wechat
import thread
from config import BOT_TOKEN

BASE_URL = "https://api.telegram.org/bot"

PROXIES = {
    "http": "http://127.0.0.1:1080",
    "https": "https://127.0.0.1:1080"
}

PROXIES_TEST = {
    "http": "http://127.0.0.1:8080",
    "https": "https://127.0.0.1:8080"
}

# regist_fun = {}
#
# def register(categories):
#     def decorator(func):
#         for category in categories:
#             regist_fun[category] = func
#         return func
#     return decorator


def cmd_start(update):
    chat_id = update['message']['chat']['id']
    wechat.run(chat_id)

cmds = {"start": cmd_start}


class Telegram(object):

    def __init__(self):
        self.updates = []
        self.offset = 0

        self.s = requests.Session()

    def send_msg(self, chat_id, text):
        api = "sendMessage"
        url = "%s%s/%s" % (BASE_URL, BOT_TOKEN, api)
        params = {"chat_id": chat_id, "text": text}
        r = self.s.get(url, params=params, proxies=PROXIES)
        print r

    def send_photo(self, chat_id, photo, **kwargs):
        api = "sendPhoto"
        url = "%s%s/%s" % (BASE_URL, BOT_TOKEN, api)
        data = {"chat_id": chat_id}
        data.update(kwargs)
        files = {"photo": photo}
        r = self.s.post(url, files=files, data=data, proxies=PROXIES)
        print r.content

    def get_updates(self, **kw):
        api = "getUpdates"
        url = "%s%s/%s" % (BASE_URL, BOT_TOKEN, api)
        params = {"offset": self.offset}
        params.update(kw)
        r = self.s.get(url, params=params, proxies=PROXIES)
        return r.json()

    def extend_updates(self, updates):
        if updates["ok"] is True and updates["result"]:
            self.updates.extend(updates["result"])
            self.offset = self.updates[-1]["update_id"] + 1
            print self.offset

    def handle_updates(self):
        while self.updates:
            update = self.updates.pop(0)
            text = update['message'].get('text')
            if text and text[0] == '/':
                func = cmds[text[1:]]
                thread.start_new_thread(func, (update,))
            print text

    def run(self):
        while True:
            updates = self.get_updates(timeout=15)
            self.extend_updates(updates)
            self.handle_updates()

if __name__ == "__main__":
    tele = Telegram()
    wechat.set_tele_instance(tele)
    tele.run()

