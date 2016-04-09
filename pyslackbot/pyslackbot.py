from slackclient import SlackClient
import threading
import time
import json
import random

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

    def trigger_handler(self, handler_id):
        handler = self.get_handler(handler_id)
        self.run_handler(handler, handler.channel)

    def get_handler(self, handler_id):
        for h in self.handlers:
            if h.handler_id == handler_id:
                return h
        return None

    def add_handler(self, handler_id, msg, reply, run=None, channel=None):
        msgs = []
        replys = []
        if type(reply) is str:
            replys.append(reply.lower())
        else:
            replys = reply

        if type(msg) is str:
            msgs.append(msg.lower())
        else:
            for i in range(len(msg)):
                msg[i] = msg[i].lower()
            msgs = msg

        handler = SlackHandler(handler_id, msgs, replys, run, channel)
        self.handlers.append(handler)

    def add_handler_json(self, data):
        with open(data) as f:
            reader = json.load(f)
            for item in reader["handlers"]:
                try:
                    for i in item["reply"]:
                        i = i.encode("utf-8").decode("unicode_escape")
                    for i in item["message"]:
                        i = i.lower()
                    self.add_handler(item['id'], item['message'], item['reply'])
                except Exception as e:
                    print("Error adding handler from CSV")
                    print(e)
                    break


    def watch_message(self):
        if self.connect:
            self.user = self.sc.server.login_data["self"]["id"]
            while True:
                message = self.sc.rtm_read()
                if message:
                    try:
                        if message[0]["type"] == "message" and message[0]["user"] != self.user:
                            #There is a message from a user
                            text = message[0]["text"]
                            if self.debug:
                                print("Message - " + text)
                            if self.user in text:
                                text = text.replace("<@" + self.user + ">", "")
                                print(text)
                                self.parse_message(text, message[0]["channel"])
                    except:
                        #excepts when the message doesn't have a type, just ignore and keep going
                        pass
                time.sleep(1)

    def parse_message(self, message, channel):
        for handler in self.handlers:
            for msg in handler.message:
                if msg in message.lower():
                    handler.received = message
                    self.run_handler(handler, channel)
                    return 0
            if message.lower() in handler.message:
                handler.received = message
                self.run_handler(handler, channel)
                return 0

    def run_handler(self, handler, channel):
        if handler.run != None:
            if self.debug:
                print("Excuting - " + str(handler.run))
            try:
                handler.run()
            except:
                print("Exception during handler function")

        print(handler.reply)
        if handler.reply != [""] and handler.reply != None:
            if handler.channel != None:
                channel = handler.channel
            if channel == None:
                print("Error: No channel selected")
                return 1

            reply = random.choice(handler.reply)
            if self.debug:
                print("Reply: " + str(channel) + "  - " + str(reply))
            self.sc.rtm_send_message(str(channel), str(reply))




class SlackHandler(object):
    def __init__(self, handler_id, message, reply, run, channel):
        self.handler_id = handler_id
        self.message = message
        self.reply = reply
        self.run = run
        self.channel = channel
        self.received = None

