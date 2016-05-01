# pyslackbot
A simple programmable slackbot. Meant to allow for a easy interface to create custom slackbots. Under development.

##Documentation
http://pyslackbot.readthedocs.org/

## Install
`pip install git+https://github.com/gmccoy42/pyslackbot.git`

## Usage
```python
from pyslackbot.pyslackbot import SlackBot

def run():
    print("Hello World")

def get_time():
    handler = bot.get_handler("TIME")
    handler.format_reply(datetime.now())
    
bot = SlackBot("<TOKEN>", True)
bot.add_handler("ID-4", "print", "", run)
bot.add_handler_json("data.json")
bot.add_handler("TIME", "What time is it?", "{}", get_time)
```


data.json
```json
{
    "handlers": [
        {
            "id":"#GREET",
            "message": [
                "Hello",
                "Hi",
                "Howdy"
            ],
            "reply": [ 
                "Hello",
                "Hi",
                "Howdy"
            ]
        },
    ]
}
```




