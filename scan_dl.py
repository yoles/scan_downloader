#!/usr/bin/env python3
"""
    Command Line Interface to download latest scan on https://scantrad.net/
"""
import requests
from bs4 import BeautifulSoup
import os
import sys

def print_help():
    """
        print the manual of the program with the list of all mangas available
    """
    msg = "PRESS Q TO EXIT THE HELPER MODE"
    wildCard = ""
    for i in range(len(msg)):
        wildCard += "*"
    print("*****"+wildCard+"*****")
    print("**** "+msg+" ****")
    print("*****"+wildCard+"*****")
    print("NAME\n\tscan_dl - Command line to donwload scan chapter on https://scantrad.net/")
    print("DESCRIPTION\n\tyou must write the manga's name and chapter as option of the program:")
    print('EXAMPLE\n\t./scan_dl.py "Golden Kamuy" 158\n')
    for m in mangas:
        print(m.description())

def isName(str):
    """
    Args:    
        str (str): the user input
    Returns:
        Manga: an instance of Manga representing the one chosen by user or quit if didn't exist
    """
    for m in mangas:
        if(str.strip().lower() == m.name.lower()):
            return m
    print("'%s' didn't exist, have you made a mistake in the name ?\n" % (str))
    print("Here the list of manga's name available: ")
    for m in mangas:
        print(m.name)
    exit(-1)

class Manga:
    """
    Attributes:
        url (str): is the url where to find images to download
        name (str): represent the name of the manga. Usefull to create directories, and put downloaded images.
        lastChapter (int): number which represent the last chapter available of the manga s
    """
    url = ''
    name = ''
    lastChapter = 0

    def description(self):
        """
        Args:
            none
        Returns:
            str: contains the name and the last chapter available of the manga. Used in helping option command.
        """
        return "nom: %s\nDernier Chapitre: %d\n" % (self.name, self.lastChapter)

def mangasAvailable():
    """
    Get all mangas available on https://scantrad.net/mangas as List of Manga.
    Args:
        none
    Returns:
        List<Manga>: represent the list of the mangas available on "scantrad.net". Instance of Manga class
    """
    url = "https://scantrad.net/mangas"
    soup = dorRequestOnUrl(url)

    mangas = []
    mangasName = soup.find_all("div", class_="hmi-titre")
    mangasUrl = soup.find_all("a", class_="home-manga")
    mangasChapter = soup.find_all("div", class_="hmi-sub")

    for i in range(len(mangasName)):
        manga = Manga()
        manga.name = mangasName[i].string
        str = mangasChapter[i].string
        manga.lastChapter = int(str[18:len(str)])
        manga.url = mangasUrl[i].get('href')
        mangas.append(manga)
    return  mangas

def dorRequestOnUrl(url):
    """
    Get all mangas available on https://scantrad.net/mangas as List of Manga.
    Args:
        url (str): url target to request 
    Returns:
        BeautifulSoup: representing the html tags of the targeted url 
    """
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def getImgFromSoup(soup):
    """
    Get all images from a soup as a string list
    Args:
        soup (BeautifulSoup): Html tags as object
    Returns:
        List<str>: List of strings representing the ending of images path  i.e: ['/lel/12f.jpg']
    """
    chapterImgs = []
    strongArray = soup.find_all("img")
    for str in strongArray:
        id = str.get('id')
        if(id and id.startswith('scimg-')):
            chapterImgs.append(str.get('data-src'))
    return chapterImgs

def getLastChapter():
    """
    Asking user if he really want download the latest scan chapter, yes => return 
    Args:
        none
    Returns:
        int: number of the last chapter of the manga chosen by user or quit the programe if "no" is chosen
    """
    answer = "no"
    while(answer != "y" and answer != "yes"):
        answer = input("The last chapter of "+ manga.name +" is " + str(manga.lastChapter) + 
            "\nDo you still want download it ? [y/n] ").lower()
        if (answer == "n" or answer == "no"):
            exit(0)
    return manga.lastChapter

def main():
    if (len(sys.argv) < 2 or sys.argv[1] == "help" or sys.argv[1] == "--h"):
            print_help()
            exit(0)

    if (len(sys.argv) > 3):
        print("Valid arugments are required  i.e: ./scan_dl.py [name] [chapter] | less")
        print("Enter:\n\t./scan_dl.py help \nto see all available options ")
        exit(-1)

    global manga
    manga = isName(sys.argv[1])
    try:
        chapter = getLastChapter() if (sys.argv[2] == "last") else int(sys.argv[2])
    except ValueError:
            print("Oops!    That was no valid number.  Try again...")
            print("Valid arugments are required  i.e: ./scan_dl.py [name] [chapter] | less")
            exit(-1)

    url = "https://scantrad.net"
    full_url = "%s/mangas%s/%s" % (url,manga.url,chapter)

    soup = dorRequestOnUrl(full_url)
    imgs = getImgFromSoup(soup)

    if (len(imgs) < 1):
        print("Error: can't find this chapter")
        print("The chapter number %d is maybe too old or not available" % (chapter))
        exit(-1)

    i = 0
    if not os.path.exists(manga.name):
        os.makedirs(manga.name)
    chapterName = "%s/chapter%d" % (manga.name, chapter)
    if not os.path.exists(chapterName):
        os.makedirs(chapterName)

    for img in imgs:
        if(not(img.startswith('lel'))):
            imgs.remove(img)
    for img in imgs:
        i += 1
        img_url = url + "/" + img
        page = '/page' + str(i)
        with open(chapterName + page, 'wb') as f:
            print("downloading: " + page[1:len(page)])
            f.write(requests.get(img_url).content)

if __name__ == "__main__":
    # global mangas
    mangas = mangasAvailable()
    main()