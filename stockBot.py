# Work with Python 3.6
import json
from discord.ext import commands
import discord
import re
import urllib.request
import credentials

BOT_PREFIX = ("?", "!")
TOKEN = credentials.secrets['TOKEN']
BRAVOS_API = credentials.secrets['BRAVOS_API']

client = commands.Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_ready():
    print('Bot is Ready!!!')


@client.event
async def on_message(message):
    author = message.author
    content = message.content
    channel = message.channel
    tickers = re.findall('[$](\w{1,4})', content)
    print(tickers)
    for ticker in tickers:
        print(ticker)
        url = 'https://data.bravos.co/v1/quote?symbols=' + ticker + \
            '&apikey=' + BRAVOS_API + '&format=json'
        print(url)

        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            nameTicker = data[ticker.upper()]['name']
            print(nameTicker)
            priceTicker = data[ticker.upper()]['price']
            print(str(priceTicker))
            await client.send_message(channel, 'The current stock price of ' + nameTicker + ' is $' + str(priceTicker))


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)

client.run(TOKEN)
