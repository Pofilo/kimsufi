# How to get Token and chatID for Telegram notifier

Official notice available [here](https://core.telegram.org/bots#6-botfather).

## How to create your bot ?

+ Speak to [@botfather](https://t.me/BotFather) and type `/start`
+ Type `/newbot` and give a name to your bot
+ Save the API token in `TOKEN` in your configuration file

## How to generate chatID ?

+ Speak to [@cid_bot](https://t.me/cid_bot) and type `/start`
+ Type `chatid` to get your chatID
+ Save it in the `CHATID` in your configuration file

## How to send a message ?

The API use is [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) due to its simplicity.
For example to send a message using this API, you need the *token* and the *chatID* generated previously and this kind of code:

```
bot = telegram.Bot(token)
bot.send_message(chatID, 'This is a message send with "python-telegram-bot"!!')
```

You can find the implementation in `notifications.py`.