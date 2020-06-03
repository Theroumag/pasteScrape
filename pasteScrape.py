#!/usr/bin/python
import requests, re
from bs4 import BeautifulSoup

linkRegrex = re.compile(r'href="/\w{8}"')
scraped_links = []
keywords = ["database", "username", "password", "bitcoin"]
proxies = []
dead_proxies = []
url = "https://api.proxyscrape.com/?request=getproxies&proxytype=https&timeout=10000&country=all&ssl=all&anonymity=all"

def genProxies(proxyList):
    scrapedProxies = requests.get(url).text.strip()

    for proxy in scrapedProxies.split('\n'):
        proxy = proxy.split('\r')[0]

        if proxy not in dead_proxies:
            proxyList.append(proxy)

    return proxyList


def scrape(proxy_list):
    for proxy in proxy_list:
        if proxy not in dead_proxies:
            r = requests.get("https://pastebin.com/archive", proxies={"http": proxy})
            if (r.status_code == 200):
                soup = BeautifulSoup(r.text, features="html5lib")
                match = soup.html.body.div.find("div", id="super_frame").div.div.find("div", id="content_left").find("div", style="padding: 0 0 10px 0").table
                print(match)
            else:
                proxies.remove(proxy)
                dead_proxies.append(proxy)
            """
            links = linkRegrex.findall(str(match))

            for link in links:
                raw_link = "http://pastebin.com/raw/"+link.split('/')[1][:-1]
                    for keyword in keywords:
                        if keyword in tr.get(raw_link).text:
                            if raw_link not in scraped_links:
                                scraped_links.append(raw_link)
                                print(raw_link)
                """

genProxies(proxies)
scrape(proxies)
