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

    if message.author == client.user:
        return

    author = message.author
    content = message.content
    channel = message.channel
    tickers = re.findall('[$](\w{1,4})', content)
    print(tickers)
    url = 'https://data.bravos.co/v1/quote?symbols=' + ",".join(tickers) + \
        '&apikey=' + BRAVOS_API + '&format=json'
    print(url)
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
        for ticker in tickers:
            try:
                nameTicker = data[ticker.upper()]['name']
                priceTicker = data[ticker.upper()]['price']
                await client.send_message(channel, 'The current stock price of ' + nameTicker + ' is $' + str(priceTicker))
            except KeyError:
                await client.send_message(channel, ticker.upper() + ' does not exist.')
                pass


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)

client.run(TOKEN)
