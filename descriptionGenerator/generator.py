#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import os

writer = "Jean de la Fontaine"

extensionDescription = "description"
extensionTag = "tag"
extensionTitle = "title"

textToInsert = {
    "fr": {
        "finalText": "Video generée automatiquement",
        "linkChannel": "https://www.youtube.com/théorisons",
        "book": "Livre",
        "fable": "Fable",
        "children": "Enfants",
        "text": "texte",
        "speech": "raconte"
    },
    "en": {
        "finalText": "Video generated automatically",
        "linkChannel": "https://www.youtube.com/théorisons",
        "book": "Book",
        "fable": "Fable",
        "children": "Children",
        "text": "text",
        "speech": "speech",
    }
}

finalCopyright = "Théorisons 2020"

nameFileDescriptions = "descriptionGenerator"
pathToFablesFromRoot = "./webScrapping/fables/"
outputFolderDescriptions = "descriptions"


class ProcessFable:
    def __init__(self, fablePath, pathOutput):
        self.lang = fablePath[-2:]

        fable = open(fablePath, "r")
        lines = fable.readlines()
        fable.close()

        self.nbBook = lines[0].strip("\n")
        self.nbFable = lines[1].strip("\n")
        self.title = lines[2].strip("\n")

        text = []
        for i in range(3, len(lines)):
            text.append(lines[i].strip("\n"))

        self.textFable = text

        self.generateTitle()
        self.generateDescription()
        self.generateTag()

        self.writeFile(
            self.videoTitle,
            "{}/{}_{}.{}.{}".format(pathOutput, self.nbBook, self.nbFable,
                                    extensionTitle, self.lang))
        self.writeFile(
            self.videoDescription,
            "{}/{}_{}.{}.{}".format(pathOutput, self.nbBook, self.nbFable,
                                    extensionDescription, self.lang))
        self.writeFile(
            self.videoTag,
            "{}/{}_{}.{}.{}".format(pathOutput, self.nbBook, self.nbFable,
                                    extensionTag, self.lang), ",")

    def generateTitle(self):
        self.videoTitle = "{} | {} | {} {} {} {}".format(
            self.title, writer, textToInsert[self.lang]["book"], self.nbBook,
            textToInsert[self.lang]["fable"], self.nbFable)

    def generateDescription(self):
        self.videoDescription = []

        self.videoDescription.append(self.videoTitle)
        self.videoDescription.append("\n")
        self.videoDescription.append("\n")
        self.videoDescription.append("___")
        self.videoDescription.append("\n")
        self.videoDescription.append("\n")

        for i in self.textFable:
            self.videoDescription.append(i)
            self.videoDescription.append("\n")

        self.videoDescription.append("\n")
        self.videoDescription.append("___")
        self.videoDescription.append("\n")
        self.videoDescription.append("\n")

        self.videoDescription.append(textToInsert[self.lang]["finalText"])
        self.videoDescription.append("\n")
        self.videoDescription.append(finalCopyright)
        self.videoDescription.append("\n")
        self.videoDescription.append("🇬🇧 / 🇺🇸 : ")
        self.videoDescription.append(textToInsert["en"]["linkChannel"])
        self.videoDescription.append("\n")
        self.videoDescription.append("🇫🇷 : ")
        self.videoDescription.append(textToInsert["fr"]["linkChannel"])
        self.videoDescription.append("\n")

    def generateTag(self):
        self.videoTag = [writer]
        self.videoTag += ["Fable"]
        self.videoTag += [
            "{} {}".format(textToInsert[self.lang]["book"], self.nbBook)
        ]
        self.videoTag += [
            "{} {}".format(textToInsert[self.lang]["fable"], self.nbFable)
        ]
        self.videoTag += [self.title]
        self.videoTag += self.title.split()
        self.videoTag += [textToInsert[self.lang]["children"]]
        self.videoTag += [textToInsert[self.lang]["text"]]
        self.videoTag += [textToInsert[self.lang]["speech"]]

    def writeFile(self, text, output, sep=""):
        output = open(output, "w")

        for t in text:
            output.write(t)
            output.write(sep)

        output.close()


def main():
    os.system("mkdir {}".format(outputFolderDescriptions))
    os.chdir("../{}".format(pathToFablesFromRoot))

    foldersBooks = os.listdir()  # Get all books

    for folder in foldersBooks:
        os.chdir("{}".format(folder))
        fables = os.listdir()

        for file in fables:
            ProcessFable(
                file, "../../../{}/{}".format(nameFileDescriptions,
                                              outputFolderDescriptions))
        os.chdir("..")


if __name__ == "__main__":
    main()