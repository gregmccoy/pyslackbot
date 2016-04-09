# pyslackbot
A simple programmable slackbot. Meant to allow for a easy interface to create custom slackbots. Under development.

## Install
`pip install git+https://github.com/gmccoy42/pyslackbot.git`

## Usage
```python
from pyslackbot.pyslackbot import SlackBot

def run():
    print("Hello World")

def get_time():
    handler = bot.get_handler("TIME")
    handler.reply.format(datetime.now())
    
bot = SlackBot("<TOKEN>", True)
bot.add_handler("ID-4", "hello", "", run)
bot.add_handler_csv("data.csv")
bot.add_handler("TIME", "What time is it?", "{}", get_time)
```


Data.csv
```csv
ID-1, message, reply
ID-2, hello, world
ID-3, hi, howdy
```




