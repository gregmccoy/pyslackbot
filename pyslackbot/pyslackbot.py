from slackclient import SlackClient
import threading
import time
import csv

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

    def add_handler(self, handler_id, msg, reply, run=None, channel=None, con=True):
        handler = SlackHandler(handler_id, msg, reply, run, con, channel)
        self.handlers.append(handler)

    def add_handler_csv(self, data, delimit=","):
        items = []
        with open(data) as f:
            reader = csv.reader(f, delimiter=delimit)
            for row in reader:
                try:
                    if len(row) == 3:
                        self.add_handler(row[0], row[1], row[2].encode("utf-8").decode('unicode_escape'))
                    elif len(row) == 4:
                        functions = globals().copy()
                        #try:
                        #    self.add_handler(row[0], row[1], functions.get(row[2]))
                        #except Exception as e:
                        #    print("Function " + str(row[2]) + " not found\n" + str(e))
                        #    break
                except Exception as e:
                    print("Error adding handler from CSV")
                    print(e)
                    break


    def watch_message(self):
        if self.connect:
            self.sc.server.login_data["self"]["id"]
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
                                self.parse_message(text, message[0]["channel"])
                    except:
                        #excepts when the message doesn't have a type, just ignore and keep going
                        pass
                time.sleep(1)

    def parse_message(self, message, channel):
        for handler in self.handlers:
            if handler.con:
                if handler.message != "NULL":
                    if handler.message.lower() in message.lower() or message.lower() in handler.message.lower():
                        self.run_handler(handler, channel)

            elif handler.message == message:
                handler.run()

    def run_handler(self, handler, channel):
        if handler.run != None:
            if self.debug:
                print("Excuting - " + str(handler.run))
            try:
                handler.run()
            except:
                print("Exception during handler function")

        if handler.reply != "" and handler.reply != None:
            if handler.channel != None:
                channel = handler.channel
            if self.debug:
                print("Replying - " + str(handler.reply))
            self.sc.rtm_send_message(channel, str(handler.reply))




class SlackHandler(object):
    def __init__(self, handler_id, message, reply, run, con, channel):
        self.handler_id = handler_id
        self.message = message
        self.reply = reply
        self.run = run
        self.con = con
        self.channel = channel

