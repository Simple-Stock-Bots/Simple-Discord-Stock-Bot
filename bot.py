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


@bot.command(description="Information on how to donate.")
async def donate(ctx, cmd: str):
    print("donate")
    await ctx.send("donate:" + cmd)


@bot.command()
async def dividend(ctx, cmd: str):
    await ctx.send("dividend:" + cmd)


@bot.command()
async def intra(ctx, cmd: str):
    await ctx.send("intra:" + cmd)


@bot.command()
async def chart(ctx, cmd: str):
    await ctx.send("chart:" + cmd)


@bot.command()
async def news(ctx, cmd: str):
    await ctx.send("news:" + cmd)


@bot.command()
async def info(ctx, cmd: str):
    await ctx.send("info:" + cmd)


@bot.command()
async def stat(ctx, cmd: str):
    await ctx.send("stat:" + cmd)


# @bot.command()
# async def help(ctx, cmd: str):
#     await ctx.send("help:" + cmd)


s = Symbol(IEX_TOKEN)
bot.run(DISCORD_TOKEN)
