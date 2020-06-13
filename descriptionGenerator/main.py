from moviepy.editor import *
import subprocess
import os

writer = "Jean de la Fontaine"

extensionDescription = "description"
extensionTag = "tag"
extensionTitle = "title"

finalText = "Video generée automatiquement"
finalCopyright = "Théorisons 2020"
linkToChannel = "https://www.youtube.com/théorisons"

pathToFablesFromRoot = "./webScrapping/fables/"
outputFolderDescriptions = "descriptions"


class ProcessFable:
    def __init__(self, fablePath, outputName, pathOutput):
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
            self.videoTitle, "{}/{}.{}.txt".format(pathOutput, outputName,
                                                   extensionTitle))
        self.writeFile(
            self.videoDescription,
            "{}/{}.{}.txt".format(pathOutput, outputName,
                                  extensionDescription))
        self.writeFile(
            self.videoTag, "{}/{}.{}.txt".format(pathOutput, outputName,
                                                 extensionTag), ",")

    def generateTitle(self):
        self.videoTitle = "{} | {} | Livre {} Fable {}".format(
            self.title, writer, self.nbBook, self.nbFable)

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

        self.videoDescription.append(finalText)
        self.videoDescription.append("\n")
        self.videoDescription.append(finalCopyright)
        self.videoDescription.append("\n")
        self.videoDescription.append(linkToChannel)

    def generateTag(self):
        self.videoTag = ["Jean de la Fontaine"]
        self.videoTag += ["Fable"]
        self.videoTag += [self.title]
        self.videoTag += self.title.split()

    def writeFile(self, text, output, sep=""):
        output = open(output, "w")

        for t in text:
            output.write(t)
            output.write(sep)

        output.close()


def main():
    os.system("mkdir {}".format(outputFolderDescriptions))
    os.chdir("../{}".format(pathToFablesFromRoot))

    nbFolders = len(subprocess.getoutput("ls").split("\n"))

    for folder in range(1, nbFolders + 1):
        os.chdir("{}".format(folder))
        nbFiles = len(subprocess.getoutput("ls").split("\n"))

        for file in range(1, nbFiles + 1):
            ProcessFable(
                "{}.txt".format(file), "{}_{}".format(folder, file),
                "../../../descriptionGenerator/{}".format(
                    outputFolderDescriptions))
        os.chdir("..")


if __name__ == "__main__":
    main()