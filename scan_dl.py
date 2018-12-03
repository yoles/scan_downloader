#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import os
import sys


def print_help():
    print("you must need abreviation of manga as name: ")
    print("op = one-piece\n" +
    "boruto = boruto\n" +
    "mha = my-hero-academia\n" +
    "hxh = hunterx-hunter\n" +
    "bcl = black-clover\n" +
    "kdom = kingdom\n" +
    "drstone = dr-stone\n" +
    "tpn = the-promised-neverland\n" +
    "anima = anima\n" +
    "ft = fairy-tail-100-years-quest\n" +
    "op = one-piece\n" +
    "boruto = boruto\n" +
    "mha = my-hero-academia\n" +
    "hxh = hunterx-hunter\n" +
    "bcl = black-clover\n" +
    "kdom = kingdom\n" +
    "drstone = dr-stone\n" +
    "tpn = the-promised-neverland\n" +
    "anima = anima\n" +
    "ft = fairy-tail-100-years-quest\n")

def isName(str):
    op = "one-piece"
    boruto = "boruto"
    mha = "my-hero-academia"
    hxh = "hunterx-hunter"
    bcl = "black-clover"
    kdom = "kingdom"
    drstone = "dr-stone"
    tpn = "the-promised-neverland"
    anima = "anima"
    ft = "fairy-tail-100-years-quest"

    if (str == "op"):
        return  op
    elif (str == "boruto"):
        return boruto
    elif (str == "mha"):
        return mha
    elif (str == "hxh"):
        return hxh
    elif (str == "bcl"):
        return bcl
    elif (str == "kdom"):
        return kdom
    elif (str == "drstone"):
        return drstone
    elif (str == "tpn"):
        return tpn
    elif (str == "kdom"):
        return kdom
    elif (str == "anima"):
        return anima
    elif (str == "ft"):
        return ft


def dorRequestOnUrl(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def getHrefFromSoup(soup):
    chapterUrl = []
    strongArray = soup.find_all("strong")

    for str in strongArray:
        chapterUrl.append(str.a.get('href'))
    return chapterUrl

if (sys.argv[1] == "help"):
        print_help()
        exit(0)

if (len(sys.argv) < 3):
    print("Veuillez entrer des arguments ex: ./ bundlescrapper.py [name] [chapitre]")
    exit(-1)

manga = isName(sys.argv[1])
try:
    chapitre = int(sys.argv[2])
except ValueError:
        print("Oops!  That was no valid number.  Try again...")
        exit(-1)

url = "https://scan-france.com" + "/" + manga

soup = dorRequestOnUrl(url)
hrefs = getHrefFromSoup(soup)

splited = hrefs[len(hrefs) - 1].split('/');
ch_max = int(splited[len(splited) - 2])

if (chapitre < 1 or chapitre > ch_max):
    print("Error: Ce chapitre n'existe pas")
    exit(-1)

i = 0
for href in hrefs:
    print(i)
    if(href.find(str(chapitre)) != -1):
        chapitre = i
        break
    i += 1

url = "https:" + hrefs[chapitre]
soup = dorRequestOnUrl(url)
pages = []
pagesValue = []

selectArray = soup.find_all("select", id="listepages")
for select in selectArray:
    pages.extend(select.select("option"))

for page in pages:
    pagesValue.append(page['value'])

nbPage = len(pages)
# copyUrl = url
for pageValue in pagesValue:
    soup = dorRequestOnUrl(url + pageValue)
    imgs = soup.find_all("img")
    imgUrl = url + imgs[1]['src']
    if not os.path.exists(manga):
        os.makedirs(manga)
    with open(manga + "/" + imgs[1]['src'], 'wb') as f:
        print("downloading: " + imgUrl)
        f.write(requests.get(imgUrl).content)
