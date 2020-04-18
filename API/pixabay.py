#!/usr/bin/python3
# -*- coding: utf-8 -*-

import credentials
import requests
import os
from PIL import Image


class generateURL:
    def __init__(self, query):
        self.query = query

    def getLink(self):
        link = credentials.infosPixabay()["link"]
        return (link)

    def getPrivateKey(self):
        privateKey = credentials.infosPixabay()["key"]
        return (f"key={privateKey}")

    def getQuery(self):
        queryFormatted = self.query.replace(" ", "+")
        return (f"q={queryFormatted}")

    def getLanguage(self):
        return ("lang=fr")

    def getSize(self):
        width = 1920
        height = 1080
        return (f"min_width={width}&min_height={height}")

    def getSafeSearch(self):
        return ("safesearch=true")

    def getUrl(self):
        URL = f"{self.getLink()}?{self.getPrivateKey()}&{self.getQuery()}&{self.getLanguage()}&{self.getSize()}&{self.getSafeSearch()}"
        return (URL)


class Pixabay:
    def __init__(self, query):
        self.responseJson = requests.get(generateURL(query).getUrl()).json()
        os.system("mkdir images")


        items = self.responseJson["hits"]

        for i in range(5):
            item = items[i]
            urlImage = item["largeImageURL"]
            ide = item["id"]

            img = Image.open(requests.get(urlImage, stream=True).raw)
            img.save(f"images/img{ide}.png")


def main():
    Pixabay("loup")


if __name__ == "__main__":
    main()
