import discord
from functions import Symbol
import os

client = discord.Client()
s = Symbol(os.environ["IEX"])


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check for dividend command
    if message.content.startswith("/dividend"):
        replies = s.dividend_reply(s.find_symbols(message.content))
        if replies:
            for reply in replies.items():
                await message.channel.send(reply[1])
        else:

            await message.channel.send(
                "Command requires a ticker. See /help for more information."
            )

    elif message.content.startswith("/news"):
        replies = s.news_reply(s.find_symbols(message.content))
        if replies:
            for reply in replies.items():
                await message.channel.send(reply[1])
        else:
            await message.channel.send(
                "Command requires a ticker. See /help for more information."
            )

    elif message.content.startswith("/info"):
        replies = s.info_reply(s.find_symbols(message.content))
        if replies:
            for reply in replies.items():
                await message.channel.send(reply[1])
        else:
            await message.channel.send(
                "Command requires a ticker. See /help for more information."
            )

    elif message.content.startswith("/search"):
        queries = s.search_symbols(message.content[7:])[:6]
        if queries:
            reply = "*Search Results:*\n`$ticker: Company Name`\n"
            for query in queries:
                reply += "`" + query[1] + "`\n"
            await message.channel.send(reply)

        else:
            await message.channel.send(
                "Command requires a query. See /help for more information."
            )

    elif message.content.startswith("/help"):
        """Send link to docs when the command /help is issued."""
        reply = "[Please see the documentation for Bot information](https://simple-stock-bots.gitlab.io/site/discord/)"
        await message.channel.send(s.help_text)

    # If no commands, check for any tickers.
    else:
        replies = s.price_reply(s.find_symbols(message.content))
        if replies:
            for reply in replies.items():
                await message.channel.send(reply[1])
        else:
            return


client.run(os.environ["DISCORD"])
