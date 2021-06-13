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
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    'https://www.googleapis.com/auth/youtube.upload',
    "https://www.googleapis.com/auth/youtube.force-ssl"
]
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')


class OptionGoogle:
    def __init__(self):
        self.generateMetadataSuper()

    def generateMetadataSuper(self):
        self.body = {}
        self.snippet = {}
        self.status = {}

        self.body["snippet"] = self.snippet
        self.body["status"] = self.status

    def applyDescription(self, description):
        self.snippet["description"] = description

    def applyCategoryId(self, categoryId=1):
        # https://gist.github.com/dgp/1b24bf2961521bd75d6c
        self.snippet["categoryId"] = categoryId  # Default (Film and Animation)

    def applyVisibility(self, visibility):
        self.status["privacyStatus"] = visibility

    def applyLanguage(self, lang):
        self.snippet["defaultLanguage"] = lang

    def applyDeclaredMadeForKids(self, madeForKids=True):
        # The content if totally for kids (at least it was meant to be)
        self.status["madeForKids"] = madeForKids
        self.status["selfDeclaredMadeForKids"] = madeForKids

    def applyTitle(self, title):
        self.snippet["title"] = title

    def getTitle(self):
        return (self.snippet["title"])

    def applyTag(self, tagsList):
        self.snippet["tags"] = tagsList.split(",")

    def __repr__(self):
        s = "body: {}".format(pprint.pformat(self.body))
        return (s)


class OptionGoogleVideo(OptionGoogle):
    def __init__(self, pathMeta, pathVideo, book, fable, lang):
        super().__init__()

        self.pathMeta = pathMeta
        self.pathVideo = pathVideo
        self.nameFile = "{}_{}".format(book, fable)
        self.book = book
        self.fable = fable
        self.lang = lang

        self.generateMetadata()

    def generateMetadata(self):
        self.setDescription()
        self.setCategoryId()
        self.setThumbnails()
        self.setVisibility()
        self.setLanguage()
        self.setDeclaredMadeForKids()
        self.setTitle()
        self.setTag()
        self.setPathVideo()

    def setDescription(self):
        nameFile = "{}{}.description.{}".format(self.pathMeta, self.nameFile,
                                                self.lang)
        super().applyDescription(self.getTextFromFile(nameFile))

    def setCategoryId(self):
        # https://gist.github.com/dgp/1b24bf2961521bd75d6c
        super().applyCategoryId()  # Default film and animation

    def setThumbnails(self):
        # super().snippet["thumbnails"] = {}
        pass

    def setVisibility(self):
        super().applyVisibility("public")

    def setLanguage(self):
        super().applyLanguage(self.lang)

    def setDeclaredMadeForKids(self):
        # The content if totally for kids (at least it was meant to be)
        super().applyDeclaredMadeForKids(True)

    def setTitle(self):
        nameFile = "{}{}.title.{}".format(self.pathMeta, self.nameFile,
                                          self.lang)
        super().applyTitle(self.getTextFromFile(nameFile))

    def setTag(self):
        nameFile = "{}{}.tag.{}".format(self.pathMeta, self.nameFile,
                                        self.lang)
        super().applyTag(self.getTextFromFile(nameFile))

    def setPathVideo(self):
        self.pathVideo = "{}{}.{}.avi".format(self.pathVideo, self.nameFile,
                                              self.lang)

    def getTextFromFile(self, filePath):
        f = open(filePath, "r")
        content = f.read()
        f.close()
        return (content)

    def __repr__(self):
        s = super().__repr__()
        return (s)


class OptionGooglePlaylist(OptionGoogle):
    def __init__(self, book, lang):
        super().__init__()

        self.book = book
        self.lang = lang

        self.generateMetadata()

    def generateMetadata(self):
        self.setTitle()
        self.setDescription()
        self.setLanguage()
        self.setVisibility()

    def setTitle(self):
        author = "Jean de la Fontaine"
        if (self.lang == "fr"):
            title = "Livre "
        else:
            title = "Book "

        title = title + "{} - {}".format(self.book, author)
        super().applyTitle(title)

    def setDescription(self):
        super().applyDescription(super().getTitle())

    def setVisibility(self):
        super().applyVisibility("public")

    def setLanguage(self):
        super().applyLanguage(self.lang)

    def __repr__(self):
        s = super().__repr__()
        return (s)


class Google:
    def __init__(self):
        self.youtube = self.get_authenticated_service()

    def get_authenticated_service(self):
        # Authorize the request and store authorization credentials.
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_console()
        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    def upload(self, optionGoogle):
        self.initialize_upload(optionGoogle)

    def getIdVideosFromPlaylist(self, idPlaylist):
        list_request = self.youtube.playlistItems().list(part="snippet",
                                                         maxResults=50,
                                                         playlistId=idPlaylist)
        response = list_request.execute()
        listVideo = response["items"]
        ids = []

        for v in listVideo:
            ids.append({
                "id": v["snippet"]["resourceId"]["videoId"],
                "resourceId": v["snippet"]["resourceId"],
                "title": v["snippet"]["title"]
            })

        return (ids)

    def addThumbnailToVideo(self, videoId, thumbnailPath):
        request = self.youtube.thumbnails().set(
            videoId=videoId, media_body=MediaFileUpload(thumbnailPath))
        response = request.execute()

    def addVideoToPlaylist(self, resourceId, playlistId, position):
        request = self.youtube.playlistItems().insert(part="snippet",
                                                      body={
                                                          "snippet": {
                                                              "playlistId":
                                                              playlistId,
                                                              "resourceId":
                                                              resourceId,
                                                              "position":
                                                              position
                                                          }
                                                      })
        response = request.execute()

    def createPlaylist(self, snippet, status):
        request = self.youtube.playlists().insert(part="snippet, status",
                                                  body={
                                                      "snippet": snippet,
                                                      "status": status
                                                  })
        response = request.execute()
        return (response["id"])

    def updateVideo(self, id, snippet, status):
        request = self.youtube.videos().update(part="snippet, status",
                                               body={
                                                   "id": id,
                                                   "snippet": snippet,
                                                   "status": status
                                               })
        response = request.execute()

    def initialize_upload(self, optionVideo):
        # Call the API's videos.insert method to create and upload the video.
        insert_request = self.youtube.videos().insert(
            part=','.join(optionVideo.body.keys()),
            body=optionVideo.body,
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
            media_body=MediaFileUpload(optionVideo.pathVideo,
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