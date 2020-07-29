from moviepy.editor import *
import subprocess
import os

sizeVideo = (1920, 1080)  #FullHD size
font = "FiraCode-Regular"  #All letter have same size

colorText = "white"

finalText = "Video generée automatiquement"
finalCopyright = "Théorisons 2020\nhttps://www.youtube.com/théorisons"
# linkToChannel = "https://www.youtube.com/théorisons"

pathToFablesFromRoot = "./webScrapping/fables/"
outputFolderVideos = "videos"

background = ColorClip(size=sizeVideo, color=[0, 255, 0])  #Background


class VideoMaker:
    # Create a segment of the video
    def __init__(self, textTop, sizeTop, textBottom="", sizeBottom=100):
        # Create the segment with the top text and bottom and the size
        self.top = TextToDisplay(sizeTop, textTop)
        self.bottom = TextToDisplay(sizeBottom, textBottom)

        self._setVideo()

    def _setVideo(self):
        if (self.bottom.textValue == ""):  #Only one text to display
            self.video = self._createVideoSingleText()

        else:
            self.video = self._createVideo()

    def _createVideoSingleText(self):
        clipTop = TextClip(self.top.textValue,
                           color=colorText,
                           fontsize=self.top.fontSize,
                           font=font)

        return (CompositeVideoClip([
            background,
            clipTop.set_position(("center", "center")),
        ]).set_duration(1))

    def _createVideo(self):
        clipTop = TextClip(self.top.textValue,
                           color=colorText,
                           fontsize=self.top.fontSize,
                           font=font)

        clipBottom = TextClip(self.bottom.textValue,
                              color=colorText,
                              fontsize=self.bottom.fontSize,
                              font=font)

        return (CompositeVideoClip([
            background,
            clipTop.set_position(("center", "top")),
            clipBottom.set_position(("center", "bottom"))
        ]).set_duration(1))


class TextToDisplay:
    # Handle text
    def __init__(self, fontSize, textValue):
        self.fontSize = fontSize
        self.textValue = textValue

        widthLetter = int(self.fontSize / 2 * 1.2)
        self.letterMaxLine = int(sizeVideo[0] / widthLetter)

        self._format()

    def _format(self):
        # Add \n to the text in order to avoid to display out of the screen
        words = self.textValue.split(" ")  # Remove all spaces

        nText = ""
        cSize = 0

        for w in words:
            # Create the new word to fit

            if (len(w) + 1 + cSize < self.letterMaxLine):
                # The word can be add to the line
                # +1 for the space
                if (nText == ""):
                    nText = "{}".format(w)
                else:
                    nText = "{} {}".format(nText, w)
                cSize += 1 + len(w)

            else:
                # Create a new line
                nText = "{}\n{}".format(nText, w)
                cSize = len(w)

        self.textValue = nText


class ProcessFable:
    def __init__(self, fablePath, outputName, pathOutput):
        fable = open(fablePath, "r")
        lines = fable.readlines()
        fable.close()

        nbBook = lines[0].strip("\n")
        nbFable = lines[1].strip("\n")
        title = lines[2].strip("\n")

        tabSegments = []

        tabSegments.append(
            VideoMaker(title, 150, "Livre {} fable {}".format(nbBook, nbFable),
                       100).video)

        for i in range(3, len(lines), 2):
            if (i == len(lines) -
                    1):  #Odd number lines, last segment has no bottom text
                tabSegments.append(
                    VideoMaker(lines[i].strip("\n"),
                               100).video)  # Bottom can't be empty
            else:
                tabSegments.append(
                    VideoMaker(lines[i].strip("\n"), 100,
                               lines[i + 1].strip("\n"), 100).video)

        tabSegments.append(
            VideoMaker(finalText, 150, finalCopyright, 75).video)

        concat = concatenate_videoclips(tabSegments)
        concat.write_videofile("{}/{}".format(pathOutput, outputName),
                               fps=30,
                               codec='mpeg4')


def main():

    os.system("mkdir {}".format(outputFolderVideos))
    os.chdir("../{}".format(pathToFablesFromRoot))

    nbFolders = len(subprocess.getoutput("ls").split("\n"))

    for folder in range(1, nbFolders + 1):
        os.chdir("{}".format(folder))
        nbFiles = len(subprocess.getoutput("ls").split("\n"))

        for file in range(1, nbFiles + 1):
            ProcessFable("{}.txt".format(file),
                         "{}_{}.avi".format(folder, file),
                         "../../../videoEditing/{}".format(outputFolderVideos))
        os.chdir("..")


if __name__ == "__main__":
    main()