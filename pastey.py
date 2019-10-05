import discord, re
from discord.ext import commands
from bs4 import BeautifulSoup
from torrequest import TorRequest
from os import system

client = commands.Bot(command_prefix = "?")
with open("token.txt", "r") as f: token = f.read()[:-1]


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(name="Protecting the campus enviorment"))
    client.help_command = commands.DefaultHelpCommand(no_category='Commands')
    tr=TorRequest(password=input("Unhashed Tor password: "))
    r = tr.get("https://pastebin.com/archive")
    system("clear")
    print("Pastey Online")

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! My latency is {round(client.latency *100)}ms!")

@client.command(aliases=["purge", "c", "p"])
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=(amount+1))

@client.command()
async def start(ctx):
    await ctx.send("I have began scraping http://pastebin.com! :slight_smile:")
    linkRegrex = re.compile(r'href="/\w{8}"')
    scraped_links = []
    keywords = []
    prune_limit = 49

    while True:
        try:
            r = tr.get("https://pastebin.com/archive")
        except:
            tr.reset_identity()
            r = tr.get("https://pastebin.com/archive")

        soup = BeautifulSoup(r.text, features="lxml")
        match = soup.html.body.div.find("div", id="super_frame").div.div.find("div", id="content_left").find("div", style="padding: 0 0 10px 0").table
        links = linkRegrex.findall(str(match))

        for link in links:
            l = "http://pastebin.com/raw/"+link.split('/')[1][:-1]
            for keyword in keywords:
                if keyword in tr.get(l).text:
                    if l not in scraped_links:
                        try:
                            await ctx.send(f"Paste: {l}\n```{tr.get(l).text}```")
                        except:
                            await ctx.send("Paste larger than 2000 characters (will fix in future)")
            scraped_links.append(l)
        while len(scraped_links) >= prune_limit:
            scraped_links.pop(0)

client.run(token)