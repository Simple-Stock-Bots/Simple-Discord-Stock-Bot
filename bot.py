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
        replies = symbolDividend(getSymbols(message.content))
        if replies:
            for reply in replies.items():
                await message.channel.send(reply[1])
        else:
            await message.channel.send("No tickers found.")

    elif message.content.startswith("/news"):
        replies = symbolNews(getSymbols(message.content))
        if replies:
            for reply in replies.items():
                await message.channel.send(reply[1])
        else:
            await message.channel.send("No tickers found.")

    elif message.content.startswith("/info"):
        replies = symbolInfo(getSymbols(message.content))
        if replies:
            for reply in replies.items():
                await message.channel.send(reply[1])
        else:
            await message.channel.send("No tickers found.")

    elif message.content.startswith("/help"):
        """Send link to docs when the command /help is issued."""
        reply = "[Please see the documentation for Bot information](https://simple-stock-bots.gitlab.io/site/discord/)"
        await message.channel.send(message)

    # If no commands, check for any tickers.
    else:
        replies = symbolDataReply(getSymbols(message.content))
        if replies:
            for reply in replies.items():
                await message.channel.send(reply[1])
        else:
            return


client.run(os.environ["DISCORD"])
