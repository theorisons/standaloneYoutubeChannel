#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import http.client
import httplib2
import os
import random
import time

import pprint

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError,
                        http.client.NotConnected, http.client.IncompleteRead,
                        http.client.ImproperConnectionState,
                        http.client.CannotSendRequest,
                        http.client.CannotSendHeader,
                        http.client.ResponseNotReady,
                        http.client.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = "../API/Google/credentialsGoogle.json"
# Path from where it is called

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')


class OptionGoogle:
    def __init__(self, pathMeta, pathVideo, nameFile, lang):
        self.pathMeta = pathMeta
        self.pathVideo = pathVideo
        self.nameFile = nameFile
        self.lang = lang
        self.generateMetadata()

    def generateMetadata(self):
        self.body = {}
        self.snippet = {}
        self.status = {}

        self.setDescription()
        self.setCategoryId()
        self.setThumbnails()
        self.setVisibility()
        self.setLanguage()
        self.setDeclaredMadeForKids()
        self.setTitle()
        self.setTag()
        self.setPathVideo()

        self.body["snippet"] = self.snippet
        self.body["status"] = self.status

    def setDescription(self):
        nameFile = "{}{}.description.{}".format(self.pathMeta, self.nameFile,
                                                self.lang)
        self.snippet["description"] = self.getTextFromFile(nameFile)

    def setCategoryId(self):
        # https://gist.github.com/dgp/1b24bf2961521bd75d6c
        self.snippet["categoryId"] = 27  # Education

    def setThumbnails(self):
        self.snippet["thumbnails"] = {}

    def setVisibility(self):
        self.status["privacyStatus"] = "unlisted"

    def setLanguage(self):
        self.snippet["defaultLanguage"] = self.lang

    def setDeclaredMadeForKids(self):
        # The content if totally for kids (at least it was meant to be)
        self.status["madeForKids"] = True
        self.status["selfDeclaredMadeForKids"] = True

    def setTitle(self):
        nameFile = "{}{}.title.{}".format(self.pathMeta, self.nameFile,
                                          self.lang)
        self.snippet["title"] = self.getTextFromFile(nameFile)

    def setTag(self):
        nameFile = "{}{}.tag.{}".format(self.pathMeta, self.nameFile,
                                        self.lang)
        self.snippet["tags"] = self.getTextFromFile(nameFile).split(",")

    def setPathVideo(self):
        self.pathVideo = "{}{}.{}.avi".format(self.pathVideo, self.nameFile,
                                              self.lang)

    def getTextFromFile(self, filePath):
        f = open(filePath, "r")
        content = f.read()
        f.close()
        return (content)

    def __repr__(self):
        s = "path file: {}".format(self.pathVideo)
        s = "{}\nbody: {}".format(s, pprint.pformat(self.body))
        return (s)


class Google:
    def __init__(self):
        self.youtube = self.get_authenticated_service()

    def upload(self, optionGoogle):
        self.initialize_upload(optionGoogle)

    def get_authenticated_service(self):
        # Authorize the request and store authorization credentials.
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_console()
        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    def initialize_upload(self, optionGoogle):
        # Call the API's videos.insert method to create and upload the video.
        insert_request = self.youtube.videos().insert(
            part=','.join(optionGoogle.body.keys()),
            body=optionGoogle.body,
            # The chunksize parameter specifies the size of each chunk of data, in
            # bytes, that will be uploaded at a time. Set a higher value for
            # reliable connections as fewer chunks lead to faster uploads. Set a lower
            # value for better recovery on less reliable connections.
            #
            # Setting 'chunksize' equal to -1 in the code below means that the entire
            # file will be uploaded in a single HTTP request. (If the upload fails,
            # it will still be retried where it left off.) This is usually a best
            # practice, but if you're using Python older than 2.6 or if you're
            # running on App Engine, you should set the chunksize to something like
            # 1024 * 1024 (1 megabyte).
            media_body=MediaFileUpload(optionGoogle.pathVideo,
                                       chunksize=-1,
                                       resumable=True))

        self.resumable_upload(insert_request)

    # This method implements an exponential backoff strategy to resume a
    # failed upload.
    def resumable_upload(self, request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print('Uploading file...')
                status, response = request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print(
                            'Video id "{}" was successfully uploaded.'.format(
                                response['id']))
                    else:
                        exit(
                            'The upload failed with an unexpected response: {}'
                            .format(response))
            except HttpError as e:
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    error = 'A retriable HTTP error {} occurred:\n{}'.format(
                        e.resp.status, e.content)
                else:
                    raise
            except RETRIABLE_EXCEPTIONS as e:
                error = 'A retriable error occurred: {}'.format(e)

            if error is not None:
                print(error)
                retry += 1
                if retry > MAX_RETRIES:
                    exit('No longer attempting to retry.')

                max_sleep = 2**retry
                sleep_seconds = random.random() * max_sleep
                print('Sleeping {} seconds and then retrying...'.format(
                    sleep_seconds))
                time.sleep(sleep_seconds)


def main():
    pass


if __name__ == "__main__":
    main()