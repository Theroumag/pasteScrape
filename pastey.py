import discord
from discord.ext import commands

client = commands.Bot(command_prefix = "?")
with open("token.txt", "r") as f: token = f.read()[:-1]



@client.event
async def on_ready():
	print("Pastey Online")

@client.event
async def on_member_join(member):
	print(f"{member} has joined the server")

@client.event
async def on_member_remove(member):
	print(f"{member} has left the server")

@client.command()
async def ping(ctx):
	await ctx.send("pong")


client.run(token)