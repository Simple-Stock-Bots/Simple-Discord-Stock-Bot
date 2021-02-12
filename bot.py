import datetime
import io
import os

import discord
import mplfinance as mpf
import pandas as pd
from discord.ext import commands

from functions import Symbol

DISCORD_TOKEN = os.environ["DISCORD"]

try:
    IEX_TOKEN = os.environ["IEX"]
except KeyError:
    IEX_TOKEN = ""
    print("Starting without an IEX Token will not allow you to get market data!")


client = discord.Client()

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


@bot.command()
async def status(ctx):
    message = ""
    try:
        # IEX Status
        message += s.iex_status() + "\n"

        # Message Status
        message += s.message_status()
    except Exception as ex:
        message += (
            f"*\n\nERROR ENCOUNTERED:*\n{ex}\n\n"
            + "*The bot encountered an error while attempting to find errors. Please contact the bot admin.*"
        )
    await ctx.send(message)


@bot.command()
async def license(ctx):
    await ctx.send(s.license)


@bot.command()
async def donate(ctx):
    await ctx.send(s.donate_text)


@bot.command()
async def stat(ctx, *, sym: str):
    symbols = s.find_symbols(sym)

    if symbols:
        for reply in s.stat_reply(symbols).items():
            await ctx.send(reply[1])


@bot.command()
async def dividend(ctx, *, sym: str):
    symbols = s.find_symbols(sym)

    if symbols:
        for symbol in symbols:
            await ctx.send(s.dividend_reply(symbol))


@bot.command()
async def news(ctx, *, sym: str):
    symbols = s.find_symbols(sym)

    if symbols:
        for reply in s.news_reply(symbols).items():
            await ctx.send(reply[1])


@bot.command()
async def info(ctx, *, sym: str):
    symbols = s.find_symbols(sym)

    if symbols:
        for reply in s.info_reply(symbols).items():
            await ctx.send(reply[1])


@bot.command()
async def search(ctx, *, query: str):
    results = s.search_symbols(query)
    if results:
        reply = "*Search Results:*\n`$ticker: Company Name`\n"
        for query in results:
            reply += "`" + query[1] + "`\n"
        await ctx.send(reply)


@bot.command()
async def crypto(ctx, symbol: str):
    reply = s.crypto_reply(symbol)
    await ctx.send(reply)


@bot.command()
async def intra(ctx, sym: str):

    symbol = s.find_symbols(sym)[0]

    df = s.intra_reply(symbol)
    if df.empty:
        await ctx.send("Invalid symbol please see `/help` for usage details.")
        return

    buf = io.BytesIO()
    mpf.plot(
        df,
        type="renko",
        title=f"\n${symbol.upper()}",
        volume=True,
        style="yahoo",
        mav=20,
        savefig=dict(fname=buf, dpi=400, bbox_inches="tight"),
    )
    buf.seek(0)

    caption = (
        f"\nIntraday chart for ${symbol.upper()} from {df.first_valid_index().strftime('%I:%M')} to"
        + f" {df.last_valid_index().strftime('%I:%M')} ET on"
        + f" {datetime.date.today().strftime('%d, %b %Y')}"
    )

    await ctx.send(
        content=caption,
        file=discord.File(
            buf,
            filename=f"{symbol.upper()}:{datetime.date.today().strftime('%d%b%Y')}.png",
        ),
    )


@bot.command()
async def chart(ctx, sym: str):

    symbol = s.find_symbols(sym)[0]

    df = s.intra_reply(symbol)
    if df.empty:
        await ctx.send("Invalid symbol please see `/help` for usage details.")
        return

    buf = io.BytesIO()
    mpf.plot(
        df,
        type="candle",
        title=f"\n${symbol.upper()}",
        volume=True,
        style="yahoo",
        savefig=dict(fname=buf, dpi=400, bbox_inches="tight"),
    )
    buf.seek(0)

    caption = (
        f"\n1 Month chart for ${symbol.upper()} from {df.first_valid_index().strftime('%d, %b %Y')}"
        + f" to {df.last_valid_index().strftime('%d, %b %Y')}"
    )

    await ctx.send(
        content=caption,
        file=discord.File(
            buf,
            filename=f"{symbol.upper()}:{datetime.date.today().strftime('1M%d%b%Y')}.png",
        ),
    )


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
