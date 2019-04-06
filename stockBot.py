# Work with Python 3.6
import discord
import re
import urllib.request
import json
import tickerInfo as ti

TOKEN = "Discord Token"
TICKER_REGEX = "[$]([a-zA-Z]{1,4})"

client = discord.Client()


@client.event
async def on_message(message):
    """
    This runs every time a message is detected.
    """

    # Check that message wasnt the bot.
    if message.author == client.user:
        return

    tickers = re.findall(TICKER_REGEX, message.content)
    if tickers is not []:
        print(tickers)
        await client.send_typing(message.channel)
        await client.send_message(message.channel, ti.tickerMessage(tickers))
        return

    # print(message.author.id)

    # if message.content.startswith("!hello"):
    #     print(dir(message.author))
    #     msg = "Hello {0.author.mention}".format(message)
    #     await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")


client.run(TOKEN)
