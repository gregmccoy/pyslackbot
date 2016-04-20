from slackclient import SlackClient
import threading
import time
import json
import random

class SlackBot(object):
    """Handles Slackbot interface

    Base class from the slackbot, create a bot and listens for messages.
    Handles messages using handlers.

    Args:
        bot_id (str): The SlackAPI token used to create the bot.
        debug (bool): Determines if debug mode is enabled.
    """
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
        """Triggers handler based on ID

        Args:
            handler_id (str): Unique ID of handler.
        """
        handler = self.get_handler(handler_id)
        self.run_handler(handler, handler.channel)

    def get_handler(self, handler_id):
        """Gets a handler based on ID

        Args:
            handler_id (str): Unique ID of handler.

        Returns:
            Handler if ID matches a handler, otherwise None
        """
        for h in self.handlers:
            if h.handler_id == handler_id:
                return h
        return None

    def add_handler(self, handler_id, msg, reply, run=None, channel=None):
        """Creates a handler

        Args:
            handler_id (str): Unique ID of handler.
            msg (str): Message that the handler will watch for.
            reply (str): Reply to be send when message is recieved.
            run (Optional [func]): function to be run when message is recieved.
            channel (Optional [str]): Channel reply will be sent to.

        """
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
        """Creates a handler based on json file

        Args:
            data (str): File location of json file.

        """
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
        """Watchs for message on slack

        Thread that constatnly watchs for new messages, If the bot is tagged
        in the message it will check the handlers to see if there is a handler
        for that message.

        """
        if self.connect:
            self.user = self.sc.server.login_data["self"]["id"]
            while True:
                try:
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
                                    self.parse_message(text, message[0]["channel"])
                        except:
                            #excepts when the message doesn't have a type, just ignore and keep going
                            pass
                except:
                    print("Connection Problems trying again in 10 seconds")
                    time.sleep(10)
                time.sleep(1)

    def parse_message(self, message, channel):
        """Checks message for handler

        Args:
            message (str): Message that was recieved
            channel (str): Channel of the message recieved
        """
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
        """Sends reply and run handler functions

        Sends the reply message over slack and executes the function if
        it is not None.

        Args:
            handler (:class:`SlackHandler`): Handler that needs to be triggered
            channel (str): Channel of the message recieved
        """
        if handler.run != None:
            if self.debug:
                print("Excuting - " + str(handler.run))
            try:
                handler.run()
            except Exception as e:
                print("Exception during handler function")
                print(e)

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
            handler.reply = handler.org_reply




class SlackHandler(object):
    """Handle message triggers and replies

    Class used to create handlers for messages and replies.

    Args:
        handler_id (str): A unique ID for the handler.
        message (list):  List of messages that with trigger the handler.
        reply (list): List of replies to send back when the message is received.
        org_reply (list): Copy of reply to allow reseting reply after it is formatted.
        run (func): An function that will be run when message is received.
        channel (channel): Channel that the reply will be sent to.
        received (channel): Initalizes as None, will be set to the message recievied.
    """
    def __init__(self, handler_id, message, reply, run, channel):
        self.handler_id = handler_id
        self.message = message
        self.reply = reply
        self.org_reply = reply
        self.run = run
        self.channel = channel
        self.received = None

