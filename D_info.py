"""Functions and Info specific to the discord Bot
"""

import re

import requests as r


class D_info:
    license = re.sub(
        r"\b\n",
        " ",
        r.get("https://gitlab.com/simple-stock-bots/simple-discord-stock-bot/-/raw/master/LICENSE").text,
    )

    help_text = """
Thanks for using this bot, consider supporting it by [buying me a beer.](https://www.buymeacoffee.com/Anson)

If you are interested in stock market data, or want to host your own bot, be sure to use my affiliate link so that the bot can stay free: [marketdata.app](https://dashboard.marketdata.app/marketdata/aff/go/misterbiggs?keyword=discord)

Keep up with the latest news for the bot in its discord Channel: https://t.me/simplestockbotnews

Full documentation on using and running your own stock bot can be found on the bots [docs.](https://docs.simplestockbot.com)

The bot detects _"Symbols"_ using either one `$` or two `$$` dollar signs before the symbol. One dollar sign is for a stock market ticker, while two is for a cryptocurrency coin. `/chart $$eth` would return a chart of the past month of data for Ethereum, while `/dividend $psec` returns dividend information for Prospect Capital stock.

Simply calling a symbol in any message that the bot can see will also return the price. So a message like: `I wonder if $$btc will go to the Moon now that $tsla accepts it as payment` would return the current price for both Bitcoin and Tesla. 

**Commands**
        - `/donate [amount in USD]` to donate. 🎗️
        - `/intra $[symbol]` Plot of the stocks movement since the last market open.  📈
        - `/chart $[symbol]` Plot of the stocks movement for the past 1 month. 📊
        - `/trending` Trending Stocks and Cryptos. 💬
        - `/help` Get some help using the bot. 🆘

**Inline Features**
    You can type @SimpleStockBot `[search]` in any chat or direct message to search for the stock bots full list of stock and crypto symbols and return the price. Then once you select the ticker want the bot will send a message as you in that chat with the latest stock price. Prices may be delayed by up to an hour.

    Market data is provided by [marketdata.app](https://dashboard.marketdata.app/marketdata/aff/go/misterbiggs?keyword=discord)

    If you believe the bot is not behaving properly run `/status` or [get in touch](https://docs.simplestockbot.com/contact).
    """

    donate_text = """
Simple Stock Bot is run entirely on donations[.](https://www.buymeacoffee.com/Anson)
All donations go directly towards paying for servers, and market data is provided by
[marketdata.app](https://dashboard.marketdata.app/marketdata/aff/go/misterbiggs?keyword=discord).

The easiest way to donate is to run the `/donate [amount in USD]` command with US dollars you would like to donate.

Example: `/donate 2` would donate 2 USD.

An alternative way to donate is through https://www.buymeacoffee.com/Anson which requires no account and accepts Paypal or Credit card.
If you have any questions see the [website](https://docs.simplestockbot.com)

    """


commands = """ # Not used by the bot but for updating commands with BotFather
donate - Donate to the bot 🎗️
help - Get some help using the bot. 🆘
trending - Trending Stocks and Cryptos. 💬
intra - $[symbol] Plot since the last market open. 📈
chart - $[chart] Plot of the past month. 📊
"""
