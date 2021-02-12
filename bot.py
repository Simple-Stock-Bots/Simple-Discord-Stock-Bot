import os

import discord
from discord.ext import commands

from functions import Symbol

client = discord.Client()

DISCORD_TOKEN = os.environ["DISCORD"]

try:
    IEX_TOKEN = os.environ["IEX"]
except KeyError:
    IEX_TOKEN = ""
    print("Starting without an IEX Token will not allow you to get market data!")


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
    command_prefix="/",
    description="Simple bot for getting stock market information.",
    intents=intents,
)


@bot.event
async def on_ready():
    print("Starting Simple Stock Bot")
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.event
async def on_message(message):

    if message.author == client.user:
        return

    if "$" in message.content:
        symbols = s.find_symbols(message.content)

        if symbols:

            for reply in s.price_reply(symbols).items():
                await message.channel.send(reply[1])

@bot.command()
async def dividend(ctx, sym: str):
    symbols = s.find_symbols(sym)

    if symbols:
        for symbol in symbols:
            await ctx.send(s.dividend_reply(symbol))


@bot.command()
async def news(ctx, sym: str):
    symbols = s.find_symbols(sym)

    if symbols:
        for reply in s.news_reply(symbols).items():
            await ctx.send(reply[1])


@bot.command()
async def info(ctx, sym: str):
    symbols = s.find_symbols(sym)

    if symbols:
        for reply in s.info_reply(symbols).items():
            await ctx.send(reply[1])


@bot.command()
async def search(ctx, query: str):
    results = s.search_symbols(query)
    if results:
        reply = "*Search Results:*\n`$ticker: Company Name`\n"
        for query in results:
            reply += "`" + query[1] + "`\n"
        await ctx.send(reply)


@bot.command()
async def intra(ctx, cmd: str):
    await ctx.send("intra:" + cmd)


@bot.command()
async def chart(ctx, cmd: str):
    await ctx.send("chart:" + cmd)


@bot.command()
async def crypto(ctx, symbol: str):
    reply = s.crypto_reply(symbol)
    await ctx.send(reply)


@bot.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content[0] == "/":
        await bot.process_commands(message)
        return

    if "$" in message.content:
        symbols = s.find_symbols(message.content)

        if symbols:
            for reply in s.price_reply(symbols).items():
                await message.channel.send(reply[1])
            return


s = Symbol(IEX_TOKEN)
bot.run(DISCORD_TOKEN)
