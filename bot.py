import discord
from functions import *

client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check for dividend command
    if message.content.startswith("/dividend"):
        replies = tickerDividend(getTickers(message.content))
        if replies:
            for tick, reply in replies.items():
                await message.channel.send(reply)
        else:
            await message.channel.send("No tickers found.")

    elif message.content.startswith("/news"):
        replies = tickerNews(getTickers(message.content))
        if replies:
            for tick, reply in replies.items():
                await message.channel.send(reply)
        else:
            await message.channel.send("No tickers found.")

    elif message.content.startswith("/info"):
        replies = tickerInfo(getTickers(message.content))
        if replies:
            for tick, reply in replies.items():
                await message.channel.send(reply)
        else:
            await message.channel.send("No tickers found.")

    elif message.content.startswith('/help'):
        """Send link to docs when the command /help is issued."""
        message = "[Please see the docs for Bot information](https://simple-stock-bots.gitlab.io/site/discord/)"
        await message.channel.send(message)

    # If no commands, check for any tickers.
    else:
        replies = tickerDataReply(getTickers(message.content))
        if replies:
            for symbol, reply in replies.items():
                await message.channel.send(reply)
        else:
            return


client.run(os.environ["DISCORD"])
