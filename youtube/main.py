#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# Change the working directory.
# Use the parent one. Allows to import module from a parent directory.

from API.Google.google import OptionGooglePlaylist, OptionGoogleVideo, Google

pathMeta = "../descriptionGenerator/descriptions/"
pathVideo = "../videoEditing/videos/"

idPlaylist = "PLlcK22VpdeaegrGgGl0m2u7VPA6GjuAjF"


def main():
    yt = Google()

    # All playlist create
    # Sort in array
    playlists = dict()
    playlists["fr"] = []
    playlists["en"] = []

    videos = dict()
    # All videos online, use dict with index = fable
    videos["fr"] = dict()
    videos["en"] = dict()

    # Create playlist
    for lang in ["fr"
                 # , "en"
                 ]:
        for p in range(1, 2, 1):
        # for p in range(1, 13, 1):
            playlistOption = OptionGooglePlaylist(p, lang).body
            # Add id into playlist right position
            snippet = playlistOption["snippet"]
            status = playlistOption["status"]
            playlists[lang].append(yt.createPlaylist(snippet, status))

    listVideos = yt.getIdVideosFromPlaylist(idPlaylist)
    # Update videos matadata
    for video in listVideos:
        processOptionVideo(video)
        yt.updateVideo(video.get("id"),
                       video.get("option").snippet,
                       video.get("option").status)
        # Create tree architecture
        if (not videos[video["option"].lang].get(video["option"].book)):
            videos[video["option"].lang][video["option"].book] = dict()

        videos[video["option"].lang][video["option"].book][video["option"].fable] = video.get("resourceId")
        if (videos[video["option"].lang][video["option"].book].get("maxFable")):
            if (videos[video["option"].lang][video["option"].book]["maxFable"] < video["option"].fable):
                videos[video["option"].lang][video["option"].book]["maxFable"] = video["option"].fable
        else:
            videos[video["option"].lang][video["option"].book]["maxFable"] = video["option"].fable

    # Insert video into the right playlist at the right spot
    for lang in ["fr", "en"]:
        bookIndex = "1"
        t = videos[lang].get(bookIndex)
        while (t):
            m = videos[lang][bookIndex]["maxFable"]
            for i in range(int(m)):
                index = str(i)
                videoId = videos[lang][bookIndex][str(i + 1)]
                playlistId = playlists[lang][i]

                yt.addVideoToPlaylist(videoId, playlistId, index)
            bookIndex = str(int(bookIndex) + 1)
            t = videos[lang].get(bookIndex)


def processOptionVideo(video):
    titleSplitted = video.get("title").split(" ")
    book = titleSplitted[0]
    fable = titleSplitted[1]
    language = titleSplitted[2]

    option = OptionGoogleVideo(pathMeta, pathVideo, book, fable, language)
    video['option'] = option


if __name__ == "__main__":
    main()