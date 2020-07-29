#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup

# constantes
MAIN_URL = "http://www.lesfables.fr"


class HtmlParser:
    #Parse a url address
    def __init__(self, url):
        """ Init the object with the targeted url"""
        self.url = url

    def getHtml(self):
        """ Get the html corresponding to the url"""
        self.html = requests.get(self.url).text

    def parsing(self):
        """ Parse the html page """
        self.parse = BeautifulSoup(self.html, "html.parser")

    def getParse(self):
        """ Getter of the html page parsed"""
        return (self.parse)

    def do(self):
        """ Do every thing """
        self.getHtml()
        self.parsing()


class ExtractInformationsFable:
    # From a book url, extract all the fables
    def __init__(self, url):
        self.parsed = HtmlParser(url)
        self.parsed.do()

        self.linksFables = []

    def setListFables(self):
        """ Set the list of url and name of fables """
        container = self.parsed.getParse().find_all(
            "div", "view-content")  # Container 0 contains div with fables

        divFablesInfos = container[0].find_all("div")

        for i in divFablesInfos:
            nameHref = self.getNameHref(i)
            number = self.getNumber(i)

            link = MAIN_URL + nameHref["href"]
            fable = ExtractFable(link)

            self.linksFables.append({
                "link": link,
                "name": nameHref["name"],
                "number": int(number),
                "fable": fable.getFable()
            })

    def getNameHref(self, target):
        """ Return the name and href of the fable"""
        tmpTag = target.find_all("a", href=True)[0]

        href = tmpTag["href"]
        name = tmpTag.text

        return ({"href": href, "name": name})

    def getNumber(self, target):
        """ Return the number of the fable"""
        tagNumber = target.find_all(
            "span", "views-field views-field-field-num-ro-de-fable")
        return (tagNumber[0].text)

    def getListFables(self):
        """ Get the list of url and name of fables """
        return (self.linksFables)


class ExtractFable:
    # Take url of the fable, return the content
    def __init__(self, url):
        self.parsed = HtmlParser(url)
        self.parsed.do()

    def getFable(self):
        fable = []

        tmpFable = self.parsed.getParse().find_all(
            "div", "field-item even")[3]  # fable container

        tmpFable = tmpFable.find_all("p")

        for f in tmpFable:
            fable += f.text.split("\n")
        # Convert the fable in array
        # Each entry is a line

        return (fable)


def generateUrlBooks():
    # Get all the url of the books
    arrayUrl = []

    for i in range(1, 13):
        arrayUrl.append({
            "number": int(i),
            "link": f"{MAIN_URL}/livre-{str(i)}"
        })

    return (arrayUrl)


def main():
    rootDirectory = "fables/"
    os.system(f"mkdir {rootDirectory}")
    # Create directory to store fables

    listBooks = generateUrlBooks()  # Generate link of books
    infos = []

    for book in listBooks:
        # Get all informations of books
        infosFable = ExtractInformationsFable(book["link"])
        infosFable.setListFables()
        infos += [{
            "book": book["number"],
            "link": book["link"],
            "fables": infosFable.getListFables()
        }]

    for book in infos:
        # For all books, export fable into new directory
        bookDir = book["book"]
        os.system(f"mkdir {rootDirectory}{bookDir}")
        # Create new directory for book

        for fable in book["fables"]:
            # Write the fable in a new text file
            fableNumber = fable["number"]
            fableName = fable["name"]
            fableStory = fable["fable"]

            ## Write the fable in French
            f = open(f"{rootDirectory}{bookDir}/{fableNumber}.fr", "w")

            # Fable content:
            #
            # <BookNumber>
            # <FableNumber>
            # <Title>
            # <Content>

            f.write(f"{bookDir}\n")
            f.write(f"{fableNumber}\n")
            f.write(f"{fableName}")  # No \n

            # \n at begin of line, avoid final \n

            for line in fableStory:
                f.write(f"\n{line}")

            f.close()


if __name__ == "__main__":
    main()
