# Simple Discord Stock Bot

Super simple Discord Bot wrote in Python for displaying the price of a stock, or news about a stock quickly and easily.

## Motivation

[Google Allo](https://blog.google/products/messages/latest-messages-allo-duo-and-hangouts/) is disappearing in March 2019 so me and my friends who use it for talking about stocks need a replacement. Allo has a feature that allows you to talk to the Google Assitant right in the chat which makes pulling up a news article or a stock quote in chat extremely easy. This bot aims to replace that specific functionality.

## Features

The bot checks every message for tickers which can be called by putting a dollar sign in front of the stock symbol like this: ```$tsla``` The bot is pretty smart and can handle as many tickers in a message as you put in.

For example the message:

```I want to know about $tsla $djia $f $aaxn $baba $amzn```

Will output:

![Discord-Bot-Stock-Price-Example](https://blog.ansonbiggs.com/content/images/2019/01/Discord-Bot-Stock-Price-Example.png)

 The bot can also quickly give you news links about any tickers you need. Simply putting ```!news``` in front of your message like this:

 ```!news $tsla```

 Will output:

![Discord-Bot-Stock-News-Example](https://blog.ansonbiggs.com/content/images/2019/01/Discord-Bot-Stock-News-Example.png)

 The news feature also works with as many tickers as you want to put in a message at once for example: ```!news I want to know about $tsla $amzn```

## How it works

The most important part of the project is [discord.py](https://github.com/Rapptz/discord.py) which is an API wrapper for Discord written in Python. discord.py made this project a breeze.

The other important part is the [Bravos API](https://bravos.co/a/data) which is used to get the current quote for the provided ticker. The API works perfectly and is free with an account.

The news sources are currently hardcoded, and the code simply puts the stock ticker into a URL where its needed to get a page on that specific ticker. The image of the company that is shown in the embeds are taken from Motley Fool without an official API. There's probably a better way to get the images but I couldn't find one easily.

## Installation

- Follow install instructions for [discord.py](https://github.com/Rapptz/discord.py#installing) without full voice support.
- Follow directions in credentials.py
  - Get Discord Token [Here](https://discordapp.com/developers/applications/) > BOTNAME > Bot > 'copy token'
  - Get Bravos API key [Here](https://bravos.co/a/data) after you make a free account
- Run stockBot.py

## Contribute

This project probably won't get additional development since I decided to use Telegram instead of Discord for group messaging, but if you would like add anything feel free to make your own clone repo, or you can contact me and maybe get a pull request going. Would also love to hear about all the things I did wrong in my code<3

## License

In laymen (not a substitute for the actual license) you can do whatever you want with this project as long as you also share it, and [give me credit](https://blog.ansonbiggs.com).

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Simple Discord Stock Bot</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://blog.ansonbiggs.com" property="cc:attributionName" rel="cc:attributionURL">Anson Biggs</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://gitlab.com/MisterBiggs/simple-discord-stock-bot" rel="dct:source">https://gitlab.com/MisterBiggs/simple-discord-stock-bot</a>.