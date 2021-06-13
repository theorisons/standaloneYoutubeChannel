from PIL import Image, ImageDraw, ImageFont
import os

sizeVideo = (1920, 1080)  #FullHD size
sizeBorder = 100
folderDestination = "thumbnails"
usedFont = "fonts/TexgyrecursorBold-V7Rw.otf"  #Monospaced font
colorText = (255, 255, 255)  # White


class Thumbnail:
    def __init__(self, textInput, colorBackground, path, name):
        pathFont = path + usedFont
        value = self._getMetric(textInput, pathFont)

        img = Image.new('RGB', sizeVideo, color=tuple(colorBackground))
        f = ImageFont.truetype(pathFont, value[1])
        d = ImageDraw.Draw(img)
        d.text(value[0], textInput, font=f, fill=colorText)

        img.save("{}{}/{}.png".format(path, folderDestination, name))

    def _getMetric(self, textInput, font):
        # Compute K to get sizeFont * K = sizeText
        # Compute the correct font size of the text to fit in the picture
        # Compute the ancor of the text
        s1 = 100
        y1 = ImageFont.truetype(font, s1).getsize(textInput)[0]
        metric = y1 / s1

        sizeText = sizeVideo[0] - 2 * sizeBorder
        fontSize = int(sizeText / metric)

        t = ImageFont.truetype(font, fontSize).getsize(textInput)

        xPosition = (sizeVideo[0] - t[0]) / 2
        yPosition = (sizeVideo[1] - t[1]) / 2

        return ([(xPosition, yPosition), fontSize])
