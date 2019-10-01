import discord, requests, time, re
from discord.ext import commands
from bs4 import BeautifulSoup

client = commands.Bot(command_prefix = "?")
with open("token.txt", "r") as f: token = f.read()[:-1]


@client.event
async def on_ready():
    print("Pastey Online")
    await client.change_presence(activity=discord.Activity(name="Protecting the campus enviorment"))
    client.help_command = commands.DefaultHelpCommand(no_category='Commands')


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! My latency is {round(client.latency *100)}ms!")

@client.command(aliases=["purge", "c", "p"])
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)

@client.command()
async def start(ctx):
    await ctx.send("I have began scraping http://pastebin.com! :slight_smile:")
    linkRegrex = re.compile(r'href="/\w{8}"')
    scraped_links = []
    prune_limit = 49
    while True:
        r = requests.get("https://pastebin.com/archive")
        soup = BeautifulSoup(r.text, features="lxml")
        match = soup.html.body.div.find("div", id="super_frame").div.div.find("div", id="content_left").find("div", style="padding: 0 0 10px 0").table
        links = linkRegrex.findall(str(match))
        for link in links:
            l = "http://pastebin.com/raw/"+link.split('/')[1][:-1]
            if l not in scraped_links:
                try:
                    await ctx.send(f"```{requests.get(l).text}```")
                except:
                    await ctx.send("Paste larger than 2000 characters (will fix in future)")
            scraped_links.append(l)
        while len(scraped_links) >= prune_limit:
            scraped_links = scraped_links[1:]
client.run(token)