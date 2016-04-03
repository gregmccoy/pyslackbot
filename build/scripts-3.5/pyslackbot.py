from slackclient import SlackClient
import threading
import time

class SlackBot(object):
    def __init__(self, bot_id, debug=False):
        self.sc = SlackClient(bot_id)
        self.user = ""
        self.connect = self.sc.rtm_connect()
        self.debug = debug

        self.threads = []
        t = threading.Thread(target=self.watch_message)
        self.threads.append(t)
        t.start()

        self.handlers = []

    def add_handler(self, msg, reply, run=None, con=True):
        handler = SlackHandler(msg, run, con)
        self.handlers.append(handler)

    def watch_message(self):
        if self.connect:
            self.sc.server.login_data["self"]["id"]
            while True:
                message = self.sc.rtm_read()
                if message and message[0]["type"] == "message" and message[0]["user"] != self.user:
                    #There is a message from a user
                    text = message[0]["text"]
                    if self.debug:
                        print("Message - " + text)
                    self.parse_message(text, message[0]["channel"])
                time.sleep(1)

    def parse_message(self, message, channel):
        for handler in self.handlers:
            if handler.con:
                if handler.message in message:
                    if handler.run != None:
                        if self.debug:
                            print("Excuting - " + str(handler.run))
                        try:
                            handler.run()
                        except:
                            print("Exception during handler function")
                    self.sc.rtm_send_message(channel, message)

            elif handler.message == message:
                handler.run()

class SlackHandler(object):
    def __init__(self, message, run, con):
        self.message = message
        self.run = run
        self.con = con
