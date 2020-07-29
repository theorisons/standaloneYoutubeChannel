#!/usr/bin/python3
# -*- coding: utf-8 -*-

import boto3


class Translate:
    #Call aws translation to translate text
    def __init__(self):
        """ Init the connection"""
        self.translate = boto3.client(service_name='translate',
                                      region_name='eu-west-3',
                                      use_ssl=True)

    def translation(self, text, langInput="fr", langOutput="en"):
        """ Translate a text"""
        self.result = self.translate.translate_text(
            Text=text,
            SourceLanguageCode=langInput,
            TargetLanguageCode=langOutput)

    def getResult(self):
        """ Return the last translation """
        return (self.result.get('TranslatedText'))


def main():
    # Test main
    pass


if __name__ == "__main__":
    main()