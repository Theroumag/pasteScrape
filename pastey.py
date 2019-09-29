import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix = "?")
with open("token.txt", "r") as f: token = f.read()[:-1]

@client.event
async def on_ready():
    print("Pastey Online")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "Hi Pastey!":
        await client.send_message(message.channel, f"Hi {message.author}!")

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! Latency is {round(client.latency *100)}ms ")

@client.command(aliases=["purge"])
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)


client.run(token)