# pyslackbot
A simple programmable slackbot. Meant to allow for a easy interface to create custom slackbots

## Install
`pip install git+https://github.com/gmccoy42/pyslackbot.git`

## Usage
```
from pyslackbot.pyslackbot import SlackBot

def run():
    print("Hello World")

bot = SlackBot("<TOKEN>", True)
bot.add_handler("hello", "", run)
bot.add_handler_csv("data.csv")
```

Data.csv
```
message, reply
hello, world
hi, howdy
```




