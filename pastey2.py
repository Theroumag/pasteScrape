import threading
import time

import requests

import discord
from discord.ext import commands

class RequestScheduler():
  def __init__(self):
    self.queue = []
    self.running = True

    self.schedulerThread = threading.Thread(target=self._SchedulerThread)

  def _SchedulerThread(self) -> None:
    while self.running:
      if self.queue:
        thread = self.queue[0]

        thread.cv.acquire()
        thread.cv.notify()
        thread.cv.release()

        self.queue.pop(0)

      time.sleep(1)

  def get(self, url: str) -> requests.Response:
    thread = _RequestScheduler_Worker(url)
    thread.start()

    self.queue.append(thread)

    return thread.join()

  def start(self) -> None:
    self.schedulerThread.start()

  def stop(self) -> None:
    self.running = False
    self.schedulerThread.join()

class _RequestScheduler_Worker(threading.Thread):
  def __init__(self, url: str):
    self.url = url
    self.cv = threading.Condition()
    self._return = None

    super(_RequestScheduler_Worker, self).__init__()

  def run(self) -> None:
    self.cv.acquire()
    self.cv.wait()

    rq = requests.get(self.url)

    print("%d: %s" % (rq.status_code, self.url))

    self._return = rq

  def join(self) -> requests.Response:
    threading.Thread.join(self)
    return self._return


import re
from bs4 import BeautifulSoup

def main() -> None:
  client = commands.Bot(command_prefix = "!")

  @client.event
  async def on_ready():
    print("Pastey ready")

    await client.change_presence(activity=discord.Activity(name="Protecting the campus enviorment"))
    client.help_command = commands.DefaultHelpCommand(no_category='Commands')

  @client.command()
  async def start(ctx):
    await ctx.send("I have begun scraping <http://pastebin.com>! :slight_smile:")

    rs = RequestScheduler()
    rs.start()

    regex = re.compile(r'href="/\w{8}"')
    scraped_links = []

    prune_limit = 50

    while True:
      print("Loop start")

      archive = rs.get("http://pastebin.com/archive")
      soup = BeautifulSoup(archive.text, features="lxml")

      match = soup.html.body.div.find("div", id="super_frame").div.div.find("div", id="content_left").find("div", style="padding: 0 0 10px 0").table
      links = regex.findall(str(match))

      for link in links:
        url = "http://pastebin.com/raw/%s" % link[7:15]

        if url not in scraped_links:
          scraped_links.append(url)

          rq = rs.get(url)
          response_text = rq.text

          if not rq.status_code == 200:
            print("banned")

            break

          header = "Paste: %s\n```\n" % url
          footer = "```"
          space = 2000 - len(header + footer)

          repeat_header = "```\n"
          repeat_footer = "```"
          repeat_space = 2000 - len(repeat_header + repeat_footer)

          if len(header + response_text + footer) <= 2000:
            await ctx.send(header + response_text + footer)
          else:
            await ctx.send(header + response_text[:space] + footer)

            response_text = response_text[space + 1:]

            while len(response_text):
              await ctx.send(repeat_header + response_text[:repeat_space] + repeat_footer)

              try:
                response_text = response_text[repeat_space + 1:]
              finally:
                pass

              continue

        if len(scraped_links) > prune_limit:
          scraped_links.pop(0)

      time.sleep(1)

  with open("./token.txt", "r") as f:
    token = f.read().strip()

  client.run(token)


if __name__ == "__main__":
  main()
