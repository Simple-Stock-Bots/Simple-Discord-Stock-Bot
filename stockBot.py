# Work with Python 3.6
import json
from discord.ext import commands
import discord
import re
import urllib.request
import credentials
from datetime import datetime

# Make sure to update credentials.py with your secrets
TOKEN = credentials.secrets['TOKEN']
BRAVOS_API = credentials.secrets['BRAVOS_API']
BOT_PREFIX = ("?", "!")

client = commands.Bot(command_prefix=BOT_PREFIX)


@client.event  # Make bot say when its ready
async def on_ready():
    print('Bot is Ready!!!')


@client.event
async def on_message(message):

    if message.author == client.user:  # Prevent bot from reacting to its own messages
        return

    # define information about the message
    author = message.author
    content = message.content
    channel = message.channel

    try:
        # regex to find tickers in messages
        tickers = re.findall('[$](\w{1,4})', content)

        # get ticker information from bravos api
        url = 'https://data.bravos.co/v1/quote?symbols=' + ",".join(tickers) + \
            '&apikey=' + BRAVOS_API + '&format=json'

        # load json data from url as an object
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            for ticker in tickers:  # iterate through the tickers and print relevant info one message at a time
                try:  # checks if data is a valid ticker, if it is not tells the user
                    nameTicker = data[ticker.upper()]['name']
                    priceTicker = data[ticker.upper()]['price']
                    if message.content.startswith('!news'):
                        embed = displayembed(ticker, nameTicker, priceTicker)
                        await client.send_message(channel, embed=embed)
                    else:
                        await client.send_message(channel, 'The current stock price of ' + nameTicker + ' is $**' + str(priceTicker) + '**')
                except KeyError:
                    await client.send_message(channel, ticker.upper() + ' does not exist.')
                    pass
    except:
        pass


def displayembed(ticker, nameTicker, priceTicker):

    embed = discord.Embed(
        title='News for ' + nameTicker,
        description='The current stock price of ' +
        nameTicker + ' is $**' + str(priceTicker) + '**',
        color=0x50bdfe
    )

    embed.set_thumbnail(
        url='https://g.foolcdn.com/art/companylogos/mark/' + ticker + '.png')
    embed.add_field(name='Seeking Alpha',
                    value='https://seekingalpha.com/symbol/' + ticker, inline=True)
    embed.add_field(
        name='MSN Money', value='https://www.msn.com/en-us/money/stockdetails?symbol=' + ticker, inline=False)
    embed.add_field(name='Yahoo Finance',
                    value='https://finance.yahoo.com/quote/' + ticker, inline=False)
    embed.add_field(name='Wall Street Journal',
                    value='https://quotes.wsj.com/' + ticker, inline=False)
    embed.add_field(
        name='The Street', value='https://www.thestreet.com/quote/' + ticker + '.html', inline=False)
    embed.add_field(
        name='Zacks', value='https://www.zacks.com/stock/quote/' + ticker, inline=False)
    return embed


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)

client.run(TOKEN)
