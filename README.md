# Personal News Bot

Telegram chatbot that fetches news according to a list of specified keywords. Uses BeautifulSoup library to scrape the headlines of articles on androidpolice.com and matches it to a list of keywords. It is programmed to automatically send the relevant news article with url to a user specified account at 9am (GMT+8) everyday.

This is my personal project to experiment with the telegram bot API and deploying to heroku using docker. 

## Getting Started

To create a telegram bot, you first need to create one from the system by talking to the Telegram Bot called BotFather. Then you will get an API token, which you must put it into the environment variable `TOKEN`. 

Antoher env variable `MODE` must be selected from 2 values: `dev`, and `prod` for the 2 ways of work: development (local) and production (heroku)

`HEROKU_APP_NAME` is the name of your application that you have created in Heroku. 

`CHAT_ID` is the ID of your telegram account that you want this bot to send the daily news to. You can obtain it by talking to [@userinfobot](https://t.me/userinfobot) on telegram

Some codes are adapted from [this page](https://medium.com/python4you/creating-telegram-bot-and-deploying-it-on-heroku-471de1d96554)

### Prerequisites

```
Docker
```

### Installing

To run this bot locally, you need to run the following commands:
Set the environment variables:
```
MODE=dev
TOKEN=<your TOKEN from botfather>
CHAT_ID=<your userid>
```

And run application.py

```
python application.py
```

## Deployment

To deploy to heroku, you can follow the Heroku section from [this page](https://medium.com/python4you/creating-telegram-bot-and-deploying-it-on-heroku-471de1d96554)
