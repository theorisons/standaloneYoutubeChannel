#!/usr/bin/python3
# -*- coding: utf-8 -*-
from moviepy.editor import *
import subprocess
import random
import hashlib

from multiprocessing import Process

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# Change the working directory.
# Use the parent one. Allows to import module from a parent directory.

from API.aws import TextToSpeech

## Video script

# La Fontaine's Fables / Les fables de la Fontaine
# <Title>

# <Fable>

textToInsert = {
    "fr": {
        "finalText": "Video generée automatiquement",
        "book": "Livre",
        "fable": "Fable",
        "writer": "Les fables de la Fontaine"
    },
    "en": {
        "finalText": "Video generated automatically",
        "book": "Book",
        "fable": "Fable",
        "writer": "La Fontaine's Fables"
    }
}

finalCopyright = "Théorisons 2020"

sizeVideo = (1920, 1080)  #FullHD size
font = "TeXGyreCursor-Regular"  #Monospaced font

colorText = "white"

pathToFablesFromRoot = "./webScrapping/fables/"
pathFromInsideFable = "../../../videoEditing/"
folderTmp = "tmp"
outputFolderVideos = "videos"

fromFableToTmp = "{}{}".format(pathFromInsideFable, folderTmp)

fromFableToWriter = pathFromInsideFable
folderWriterAudio = "src"
nameFileWriter = "presentation"

delayBeetwenSentence = 0.5

colorBackground = [
    # Background color
    [26, 188, 156],
    [22, 160, 133],
    [46, 204, 113],
    [39, 174, 96],
    [52, 152, 219],
    [41, 128, 185],
    [155, 89, 182],
    [142, 68, 173],
    [52, 73, 94],
    [44, 62, 80],
    [241, 196, 15],
    [243, 156, 18],
    [230, 126, 34],
    [211, 84, 0],
    [229, 80, 57],
    [74, 105, 189],
    [56, 173, 169],
    [7, 153, 146],
    [10, 61, 98],
    [183, 21, 64],
    [229, 142, 38],
    [250, 152, 58],
    [184, 233, 148]
]


def generateName(text):
    # Generate name of the audio file
    # md5 of the text in hexa
    # Avoid to have same names and non unicode character
    result = hashlib.md5(text.encode())
    return (result.hexdigest())


def getAudio(lang, text, path, polly="", name=""):
    # Generate the audio from the text with aws polly
    # Path is the file where the audio will be save
    # If no name given, one will be generated

    nameFile = name if name != "" else generateName(text)

    service = polly if polly != "" else TextToSpeech()

    pathOutput = "{}/{}".format(path, nameFile)
    service.translate(lang, text, pathOutput)

    return ("{}.{}.mp3".format(pathOutput, lang))


class SegmentVideo:
    # Create a video segment with a single text display in the center
    def __init__(self, polly, lang, background, textTop, sizeTop, textRead,
                 audioFile, delay):
        # Init all given parameters
        self.polly = polly
        self.lang = lang

        self.background = background
        self.delay = delay

        self.top = TextToDisplay(sizeTop, textTop)

        self.textRead = textRead
        self.audioFile = audioFile

    def _getAudio(self):
        # Handle if the clip needs audio
        if self.audioFile != "":
            # Premade audio file
            return (self.audioFile)

        if self.textRead != "":
            # Need to generate audio for the text on top
            return (getAudio(self.lang, self.textRead, fromFableToTmp,
                             self.polly))

        # No audio for this clip
        return ("")

    def createVideo(self):
        # Create the segment of the video
        textTop = TextClip(self.top.textValue,
                           color=colorText,
                           fontsize=self.top.fontSize,
                           font=font)

        audioFile = self._getAudio()

        if (audioFile == ""):
            # No audio on this portion
            return (CompositeVideoClip([
                self.background,
                textTop.set_position(("center", "center")),
            ]).set_duration(self.delay))

        audio = AudioFileClip(audioFile)
        return (CompositeVideoClip([
            self.background,
            textTop.set_position(("center", "center")),
        ]).set_duration(audio.duration + self.delay).set_audio(audio))


class SegmentVideoMultiple(SegmentVideo):
    # Create a segment of video with 2 texts display, on the top and on the bottom
    def __init__(self, polly, lang, background, textTop, sizeTop, textRead,
                 audioFile, delay, textBottom, sizeBottom):
        # Init parameters

        SegmentVideo.__init__(self, polly, lang, background, textTop, sizeTop,
                              textRead, audioFile, delay)  # Use OOP

        self.bottom = TextToDisplay(sizeBottom, textBottom)

    def createVideo(self):
        # Generate top and bottom text
        clipTop = TextClip(self.top.textValue,
                           color=colorText,
                           fontsize=self.top.fontSize,
                           font=font)

        clipBottom = TextClip(self.bottom.textValue,
                              color=colorText,
                              fontsize=self.bottom.fontSize,
                              font=font)

        audioFile = self._getAudio()

        if (audioFile == ""):
            # No audio on this portion
            return (CompositeVideoClip([
                self.background,
                clipTop.set_position(("center", "top")),
                clipBottom.set_position(("center", "bottom"))
            ]).set_duration(self.delay))

        audio = AudioFileClip(audioFile)

        return (CompositeVideoClip([
            self.background,
            clipTop.set_position(("center", "top")),
            clipBottom.set_position(("center", "bottom"))
        ]).set_duration(audio.duration + self.delay).set_audio(audio))


class TextToDisplay:
    # Handle text
    # Edit the text to display it correctly
    def __init__(self, fontSize, textValue):
        self.fontSize = fontSize
        self.textValue = textValue

        widthLetter = int(self.fontSize / 2 * 1.2)
        self.letterMaxLine = int(sizeVideo[0] /
                                 widthLetter)  # Letter aspect ratio

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

        self.textValue = nText  # Final text to display


class ProcessFable:
    def __init__(self, polly, fablePath, pathOutput):
        # Create the video for a fable
        self.generateBackground()

        self.polly = polly

        lang = fablePath[
            -2:]  # Get the language of the fable based on its extension

        # Get the fable
        fable = open(fablePath, "r")
        lines = fable.readlines()
        fable.close()

        # Get meta informations of the fable
        nbBook = lines[0].strip("\n")
        nbFable = lines[1].strip("\n")
        title = lines[2].strip("\n")

        tabSegments = []  # Segments of the video

        writerRead = SegmentVideoMultiple(
            self.polly, lang, self.background, title, 150, "",
            "{}{}/{}.{}.mp3".format(fromFableToWriter, folderWriterAudio,
                                    nameFileWriter, lang), 0.2,
            "{} {} {} {}".format(textToInsert[lang]["book"], nbBook,
                                 textToInsert[lang]["fable"], nbFable),
            100).createVideo()  # Read the writer, generate once

        titleRead = SegmentVideoMultiple(
            self.polly, lang, self.background, title, 150, title, "",
            delayBeetwenSentence,
            "{} {} {} {}".format(textToInsert[lang]["book"], nbBook,
                                 textToInsert[lang]["fable"], nbFable),
            100).createVideo()  # Read the title, generate by polly

        tabSegments.append(writerRead)
        tabSegments.append(titleRead)

        for i in range(3, len(lines), 2):  # Iterate on the fable text
            if (i == len(lines) -
                    1):  #Odd number lines, last segment has no bottom text
                tabSegments.append(
                    SegmentVideo(self.polly, lang, self.background,
                                 lines[i].strip("\n"), 100, lines[i], "",
                                 delayBeetwenSentence).createVideo()
                )  # Bottom can't be empty
            else:
                tabSegments.append(
                    SegmentVideoMultiple(self.polly, lang, self.background,
                                         lines[i].strip("\n"), 100, lines[i],
                                         "", delayBeetwenSentence,
                                         lines[i + 1].strip('\n'),
                                         100).createVideo())  # Read top line

                tabSegments.append(
                    SegmentVideoMultiple(self.polly, lang, self.background,
                                         lines[i].strip("\n"), 100,
                                         lines[i + 1], "",
                                         delayBeetwenSentence,
                                         lines[i + 1].strip('\n'),
                                         100).createVideo())  # Read top line
        # Add the final copyright
        tabSegments.append(
            SegmentVideoMultiple(self.polly, lang, self.background,
                                 textToInsert[lang]["finalText"], 150, "", "",
                                 delayBeetwenSentence * 5, finalCopyright,
                                 75).createVideo())  # No audio on this segment

        concat = concatenate_videoclips(tabSegments)

        concat.write_videofile("{}/{}".format(
            pathOutput, "{}_{}.{}.avi".format(nbBook, nbFable, lang)),
                               fps=30,
                               codec='mpeg4')  # Create the output file

    def generateBackground(self):
        # Generate the background for the video
        color = random.choice(colorBackground)
        self.background = ColorClip(size=sizeVideo, color=color)


def generateOnceWriter():
    # Generate the audio for the writer
    os.system("mkdir {}".format(folderWriterAudio))  # Create the folder

    getAudio("fr", textToInsert["fr"]["writer"],
             "{}/".format(folderWriterAudio), "", nameFileWriter)
    getAudio("en", textToInsert["en"]["writer"],
             "{}/".format(folderWriterAudio), "", nameFileWriter)


def processFolder(folder):
    # Process all video in 1 folder.
    # Use for parallelism
    os.chdir("{}".format(folder))

    polly = TextToSpeech()  # Generate one instance of polly

    files = os.listdir()

    for file in files:
        ProcessFable(polly, file, "{}{}".format(pathFromInsideFable,
                                                outputFolderVideos))

    os.chdir("..")


def main():
    os.system("mkdir {}".format(
        outputFolderVideos))  # Create the ouput folder for the video
    os.system("mkdir {}".format(
        folderTmp))  # Create the temporary file for the audio

    # Create the audio use multiple time (writer name)
    generateOnceWriter()

    os.chdir("../{}".format(
        pathToFablesFromRoot))  # Change directory into the fable

    ## Loop on folders
    folders = os.listdir()

    for folder in folders:
        # Multiprocessing on the folder
        Process(target=processFolder, args=(str(folder), )).start()


if __name__ == "__main__":
    main()