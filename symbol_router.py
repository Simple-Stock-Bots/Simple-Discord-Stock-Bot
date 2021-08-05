"""Function that routes symbols to the correct API provider.
"""

import datetime
import random
import re
from logging import critical, debug, error, info, warning

import pandas as pd
from fuzzywuzzy import fuzz

from cg_Crypto import cg_Crypto
from IEX_Symbol import IEX_Symbol
from Symbol import Coin, Stock, Symbol


class Router:
    STOCK_REGEX = "(?:^|[^\\$])\\$([a-zA-Z.]{1,6})"
    CRYPTO_REGEX = "[$]{2}([a-zA-Z]{1,20})"
    searched_symbols = {}

    def __init__(self):
        self.stock = IEX_Symbol()
        self.crypto = cg_Crypto()

    def find_symbols(self, text: str) -> list[Symbol]:
        """Finds stock tickers starting with a dollar sign, and cryptocurrencies with two dollar signs
        in a blob of text and returns them in a list.

        Parameters
        ----------
        text : str
            Blob of text.

        Returns
        -------
        list[str]
            List of stock symbols as strings without dollar sign.
        """
        symbols = []
        stocks = set(re.findall(self.STOCK_REGEX, text))
        for stock in stocks:
            if stock.upper() in self.stock.symbol_list["symbol"].values:
                symbols.append(Stock(stock))
            else:
                info(f"{stock} is not in list of stocks")

        coins = set(re.findall(self.CRYPTO_REGEX, text))
        for coin in coins:
            if coin.lower() in self.crypto.symbol_list["symbol"].values:
                symbols.append(Coin(coin.lower()))
            else:
                info(f"{coin} is not in list of coins")
        info(symbols)
        return symbols

    def status(self, bot_resp) -> str:
        """Checks for any issues with APIs.

        Returns
        -------
        str
            Human readable text on status of the bot and relevant APIs
        """

        stats = f"""
        Bot Status:
        {bot_resp}

        Stock Market Data:
        {self.stock.status()}

        Cryptocurrency Data:
        {self.crypto.status()}
        """

        warning(stats)

        return stats

    def search_symbols(self, search: str) -> list[tuple[str, str]]:
        """Performs a fuzzy search to find stock symbols closest to a search term.

        Parameters
        ----------
        search : str
            String used to search, could be a company name or something close to the companies stock ticker.

        Returns
        -------
        list[tuple[str, str]]
            A list tuples of every stock sorted in order of how well they match.
                Each tuple contains: (Symbol, Issue Name).
        """

        df = pd.concat([self.stock.symbol_list, self.crypto.symbol_list])

        search = search.lower()

        df["Match"] = df.apply(
            lambda x: fuzz.ratio(search, f"{x['symbol']}".lower()),
            axis=1,
        )

        df.sort_values(by="Match", ascending=False, inplace=True)
        # if df["Match"].head().sum() < 300:
        #     df["Match"] = df.apply(
        #         lambda x: fuzz.partial_ratio(search, x["name"].lower()),
        #         axis=1,
        #     )

        #     df.sort_values(by="Match", ascending=False, inplace=True)

        symbols = df.head(20)
        symbol_list = list(zip(list(symbols["symbol"]), list(symbols["description"])))
        self.searched_symbols[search] = symbol_list
        return symbol_list

    def inline_search(self, search: str) -> list[tuple[str, str]]:
        """Searches based on the shortest symbol that contains the same string as the search.
        Should be very fast compared to a fuzzy search.

        Parameters
        ----------
        search : str
            String used to match against symbols.

        Returns
        -------
        list[tuple[str, str]]
            Each tuple contains: (Symbol, Issue Name).
        """

        df = pd.concat([self.stock.symbol_list, self.crypto.symbol_list])

        search = search.lower()

        df = df[df["type_id"].str.contains(search, regex=False)].sort_values(
            by="type_id", key=lambda x: x.str.len()
        )

        symbols = df.head(20)
        symbol_list = list(zip(list(symbols["symbol"]), list(symbols["description"])))
        self.searched_symbols[search] = symbol_list
        return symbol_list

    def price_reply(self, symbols: list[Symbol]) -> list[str]:
        """Returns current market price or after hours if its available for a given stock symbol.

        Parameters
        ----------
        symbols : list
            List of stock symbols.

        Returns
        -------
        Dict[str, str]
            Each symbol passed in is a key with its value being a human readable
            markdown formatted string of the symbols price and movement.
        """
        replies = []

        for symbol in symbols:
            info(symbol)
            if isinstance(symbol, Stock):
                replies.append(self.stock.price_reply(symbol))
            elif isinstance(symbol, Coin):
                replies.append(self.crypto.price_reply(symbol))
            else:
                info(f"{symbol} is not a Stock or Coin")

        return replies

    def dividend_reply(self, symbols: list) -> list[str]:
        """Returns the most recent, or next dividend date for a stock symbol.

        Parameters
        ----------
        symbols : list
            List of stock symbols.

        Returns
        -------
        Dict[str, str]
            Each symbol passed in is a key with its value being a human readable
                formatted string of the symbols div dates.
        """
        replies = []
        for symbol in symbols:
            if isinstance(symbol, Stock):
                replies.append(self.stock.dividend_reply(symbol))
            elif isinstance(symbol, Coin):
                replies.append("Cryptocurrencies do no have Dividends.")
            else:
                print(f"{symbol} is not a Stock or Coin")

        return replies

    def news_reply(self, symbols: list) -> list[str]:
        """Gets recent english news on stock symbols.

        Parameters
        ----------
        symbols : list
            List of stock symbols.

        Returns
        -------
        Dict[str, str]
            Each symbol passed in is a key with its value being a human
                readable markdown formatted string of the symbols news.
        """
        replies = []

        for symbol in symbols:
            if isinstance(symbol, Stock):
                replies.append(self.stock.news_reply(symbol))
            elif isinstance(symbol, Coin):
                # replies.append(self.crypto.news_reply(symbol))
                replies.append(
                    "News is not yet supported for cryptocurrencies. If you have any suggestions for news sources please contatct @MisterBiggs"
                )
            else:
                print(f"{symbol} is not a Stock or Coin")

        return replies

    def info_reply(self, symbols: list) -> list[str]:
        """Gets information on stock symbols.

        Parameters
        ----------
        symbols : list[str]
            List of stock symbols.

        Returns
        -------
        Dict[str, str]
            Each symbol passed in is a key with its value being a human readable formatted
                string of the symbols information.
        """
        replies = []

        for symbol in symbols:
            if isinstance(symbol, Stock):
                replies.append(self.stock.info_reply(symbol))
            elif isinstance(symbol, Coin):
                replies.append(self.crypto.info_reply(symbol))
            else:
                print(f"{symbol} is not a Stock or Coin")

        return replies

    def intra_reply(self, symbol: Symbol) -> pd.DataFrame:
        """Returns price data for a symbol since the last market open.

        Parameters
        ----------
        symbol : str
            Stock symbol.

        Returns
        -------
        pd.DataFrame
            Returns a timeseries dataframe with high, low, and volume data if its available.
                Otherwise returns empty pd.DataFrame.
        """

        if isinstance(symbol, Stock):
            return self.stock.intra_reply(symbol)
        elif isinstance(symbol, Coin):
            return self.crypto.intra_reply(symbol)
        else:
            print(f"{symbol} is not a Stock or Coin")
            return pd.DataFrame()

    def chart_reply(self, symbol: Symbol) -> pd.DataFrame:
        """Returns price data for a symbol of the past month up until the previous trading days close.
        Also caches multiple requests made in the same day.

        Parameters
        ----------
        symbol : str
            Stock symbol.

        Returns
        -------
        pd.DataFrame
            Returns a timeseries dataframe with high, low, and volume data if its available.
                Otherwise returns empty pd.DataFrame.
        """
        if isinstance(symbol, Stock):
            return self.stock.chart_reply(symbol)
        elif isinstance(symbol, Coin):
            return self.crypto.chart_reply(symbol)
        else:
            print(f"{symbol} is not a Stock or Coin")
            return pd.DataFrame()

    def stat_reply(self, symbols: list[Symbol]) -> list[str]:
        """Gets key statistics for each symbol in the list

        Parameters
        ----------
        symbols : list[str]
            List of stock symbols

        Returns
        -------
        Dict[str, str]
            Each symbol passed in is a key with its value being a human readable
                formatted string of the symbols statistics.
        """
        replies = []

        for symbol in symbols:
            if isinstance(symbol, Stock):
                replies.append(self.stock.stat_reply(symbol))
            elif isinstance(symbol, Coin):
                replies.append(self.crypto.stat_reply(symbol))
            else:
                print(f"{symbol} is not a Stock or Coin")

        return replies

    def cap_reply(self, symbols: list[Symbol]) -> list[str]:
        """Gets market cap for each symbol in the list

        Parameters
        ----------
        symbols : list[str]
            List of stock symbols

        Returns
        -------
        Dict[str, str]
            Each symbol passed in is a key with its value being a human readable
                formatted string of the symbols market cap.
        """
        replies = []

        for symbol in symbols:
            if isinstance(symbol, Stock):
                replies.append(self.stock.cap_reply(symbol))
            elif isinstance(symbol, Coin):
                replies.append(self.crypto.cap_reply(symbol))
            else:
                print(f"{symbol} is not a Stock or Coin")

        return replies

    def trending(self) -> str:
        """Checks APIs for trending symbols.

        Returns
        -------
        list[str]
            List of preformatted strings to be sent to user.
        """

        stocks = self.stock.trending()
        coins = self.crypto.trending()

        reply = "Trending Stocks:\n"
        reply += "-" * len("Trending Stocks:") + "\n"
        for stock in stocks:
            reply += stock + "\n"

        reply += "\n\nTrending Crypto:\n"
        reply += "-" * len("Trending Crypto:") + "\n"
        for coin in coins:
            reply += coin + "\n"

        return reply

    def random_pick(self) -> str:

        choice = random.choice(
            list(self.stock.symbol_list["description"])
            + list(self.crypto.symbol_list["description"])
        )
        hold = (
            datetime.date.today() + datetime.timedelta(random.randint(1, 365))
        ).strftime("%b %d, %Y")

        return f"{choice}\nBuy and hold until: {hold}"

    def batch_price_reply(self, symbols: list[Symbol]) -> list[str]:
        """Returns current market price or after hours if its available for a given stock symbol.

        Parameters
        ----------
        symbols : list
            List of stock symbols.

        Returns
        -------
        Dict[str, str]
            Each symbol passed in is a key with its value being a human readable
            markdown formatted string of the symbols price and movement.
        """
        replies = []
        stocks = []
        coins = []

        for symbol in symbols:
            if isinstance(symbol, Stock):
                stocks.append(symbol)
            elif isinstance(symbol, Coin):
                coins.append(symbol)
            else:
                print(f"{symbol} is not a Stock or Coin")

        if stocks:
            # IEX batch endpoint doesnt seem to be working right now
            for stock in stocks:
                replies.append(self.stock.price_reply(stock))
        if coins:
            replies = replies + self.crypto.batch_price(coins)

        return replies
