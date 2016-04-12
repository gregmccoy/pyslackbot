Getting Start
=============

Install
+++++++

To install from github using pip run.

.. code-block:: bash

    pip install git+https://github.com/gmccoy42/pyslackbot.git

Importing
+++++++++

You can import the library using:

.. code-block:: python

    from pyslackbot.pyslackbot import SlackBot



You will need a api token from Slack, once you have that your ready to go.

Example
+++++++

.. code-block:: python

    from pyslackbot.pyslackbot import SlackBot

    def run():
        print("Hello World")

    def get_time():
        handler = bot.get_handler("TIME")
        handler.reply[0] = handler.reply[0].format(datetime.now())

    bot = SlackBot("<TOKEN>", True)
    bot.add_handler("ID-4", "print", "", run)
    bot.add_handler("TIME", "What time is it?", "{}", get_time)
