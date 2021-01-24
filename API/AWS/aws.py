#!/usr/bin/python3
# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import BotoCoreError, ClientError
import sys
from contextlib import closing


class Translate:
    #Use aws translation to translate text
    def __init__(self):
        # Init the connection
        self.translate = boto3.client(
            service_name='translate',
            region_name='eu-west-3',  # Paris server
            use_ssl=True)

    def translation(self, text, langInput="fr", langOutput="en"):
        # Translate a text
        self.result = self.translate.translate_text(
            Text=text,
            SourceLanguageCode=langInput,
            TargetLanguageCode=langOutput)

    def getResult(self):
        # Return the last translation
        return (self.result.get('TranslatedText'))


class TextToSpeech:
    #Use aws polly to use text to speech
    def __init__(self):
        # Init the connection
        # French voice -> Lea
        # US voice -> Kendra
        self.polly = boto3.client(
            service_name="polly",
            region_name='eu-west-3',  # Paris server
            use_ssl=True)

    def translate(self, lang, text, pathOutput):
        # Translate text in lang into speech
        voice = "Lea" if lang == "fr" else "Kendra"
        langCode = "fr-FR" if lang == "fr" else "en-US"

        response = self.polly.synthesize_speech(Engine="standard",
                                                Text=text,
                                                OutputFormat="mp3",
                                                VoiceId=voice,
                                                LanguageCode=langCode)

        file = open("{}.{}.mp3".format(pathOutput, lang), 'wb')
        file.write(response['AudioStream'].read())
        file.close()


def main():
    # Test main
    pass


if __name__ == "__main__":
    main()