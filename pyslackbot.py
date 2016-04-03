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

    def add_handler(self, msg, reply, run=None, channel=None, con=True):
        handler = SlackHandler(msg, reply, run, con, channel)
        self.handlers.append(handler)

    def add_handler_csv(self, data, delimit=","):
        items = []
        with open(data) as f:
            reader = csv.reader(f, delimiter=delimit)
            for row in reader:
                try:
                    if len(row) == 2:
                        self.add_handler(row[0], row[1])
                    elif len(row) == 3:
                        functions = globals().copy()
                        try:
                            self.add_handler(row[0], row[1], functions.get(row[2]))
                        except Exception as e:
                            print("Function " + str(row[2]) + " not found\n" + str(e))
                            break
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
                            self.parse_message(text, message[0]["channel"])
                    except:
                        #excepts when the message doesn't have a type, just ignore and keep going
                        pass
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

                    if handler.reply != "" and handler.reply != None:
                        if handler.channel != None:
                            channel = handler.channel
                        if self.debug:
                            print("Replying - " + str(handler.reply))
                        self.sc.rtm_send_message(channel, handler.reply)

            elif handler.message == message:
                handler.run()

class SlackHandler(object):
    def __init__(self, message, reply, run, con, channel):
        self.message = message
        self.reply = reply
        self.run = run
        self.con = con
        self.channel = channel

