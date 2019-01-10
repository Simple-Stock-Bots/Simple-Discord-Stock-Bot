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
    content = message.content.lower()
    channel = message.channel

    try:
        # regex to find tickers in messages, looks for up to 4 word characters following a dollar sign and captures the 4 word characters
        tickers = re.findall('[$](\w{1,4})', content)

        # get ticker information from bravos api, turns tickers into comma separated list so that only one api call is needed per message
        url = 'https://data.bravos.co/v1/quote?symbols=' + ",".join(tickers) + \
            '&apikey=' + BRAVOS_API + '&format=json'

        # load json data from url as an object
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())

            for ticker in tickers:  # iterate through the tickers and print relevant info one message at a time
                try:  # checks if data is a valid ticker, if it is not tells the user

                    # Get Stock ticker name from Data Object
                    nameTicker = data[ticker.upper()]['name']
                    # Get Stock Ticker price from Object
                    priceTicker = data[ticker.upper()]['price']

                    # Checks if !news is called, and prints news embed if it is
                    if content.startswith('!news'):

                        embed = displayembed(ticker, nameTicker, priceTicker)
                        await client.send_message(channel, embed=embed)
                    else:  # If news embed isnt called, print normal stock price
                        await client.send_message(channel, 'The current stock price of ' + nameTicker + ' is $**' + str(priceTicker) + '**')

                except KeyError:  # If searching for the ticker in loaded data fails, then Bravos didnt provide it, so tell the user.
                    await client.send_message(channel, ticker.upper() + ' does not exist.')
                    pass
    except:
        pass


# Prints an embed full of news about listed stock
def displayembed(ticker, nameTicker, priceTicker):

    embed = discord.Embed(
        title='News for ' + nameTicker,
        description='The current stock price of ' +
        nameTicker + ' is $**' + str(priceTicker) + '**',
        color=0x50bdfe
    )
    '''
    Get ticker logo from Motley Fool, then get then print the following sources:
    Bravos, Seeking Alpha, MSN Money, Yahoo Finance, Wall Street Journal, The Street.
    '''
    embed.set_thumbnail(
        url='https://g.foolcdn.com/art/companylogos/mark/' + ticker + '.png')
    embed.add_field(name='Bravos',
                    value='https://bravos.co/' + ticker, inline=False)
    embed.add_field(name='Seeking Alpha',
                    value='https://seekingalpha.com/symbol/' + ticker, inline=False)
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
