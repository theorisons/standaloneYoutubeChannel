# Standalone YouTube channel

## Overview 

Source code of an Autonomous YouTube channel. Global explanation in the video _How to create a standalone YouTube channel_ **[here in english](https://youtu.be/LIEN "Watch the video")** or **[ici en français](https://youtu.be/LIEN "Regarder la vidéo")**.

The project is to create and publish automatic contents for a YouTube channel. Videos are about _les fables de La Fontaine_, French stories that are in public domain.

- Les fables are collected with _webscrapping_ `/webScrapping` then placed in the folder depending on the book `/webScrapping/fables`.

The french version contains the extension `.fr`, the english version `.en`.

- Titles, descriptions, tags are in `/descriptionGenerator` are generated thanks to the text of the fablesthen placed in the folder `/descriptionGenerator/descriptions`. Extensions are :
  - `.description` for the descriptions
  - `.tag` for the tags
  - `.title` for the titres

The french version contains the extension `.fr`, the english version `.en`.

- The edit `/videoEditing` is based on the text.
- API `/API` use multiple services:
  - Get copyright-free images
  - Translation of text from French to English
  - Text to speach (French / English)
  - Upload videos on YouTube
  - Answer comments on YouTube


## Dependences

- Python 3
- BeautifulSoup
- moviepy
- boto3

## API

### AWS

The cloud service of Amazon is used for:
- Translate text with **[Amazon Translate](https://aws.amazon.com/fr/translate/ "See demonstration")**
- Text to speach **[Amazon Polly](https://aws.amazon.com/fr/polly/ "See demonstation")**

### Google

Google's API are used to upload videos on YouTube with the title, description, tags and thumbnails.


## Execution

Command to run scripts. The working directory is supposed to be `./`.

### WebScrapping Fables

```
cd ./webScrapping
python3 webscrappingFrench.py
```

Create a new folder `fables` with subfolders with books number. In each subfolders, there is text files with names `<numeroFable>.fr`.


Pattern of fables is

```
<Book number>
<Fable number>
<Title>
<Content>
```

### Translate fables in English

```
cd ./webScrapping
python3 translateFablesEnglish.py
```

Iterate over all fables `<numeroFable>.fr` then create a new file `<numeroFable>.en` where the content is translated.

**WARNING NO FILES `.en` HAS TO BE IN THE FOLDER** otherwise the content will be erased. (From the fact that we iterate over all files and not only `.fr` files).

Pattern of the fable remains similar.

### Generation of the metadata for the fables

```
cd ./descriptionGenerator
python3 generator.py
```

Create a folder `descriptions`. Iterate over all files `<numeroFable>.*` then create 3 files per fable (title, tags and description).

### Generation of video

```
cd ./videoEditing
python3 main.py
```

Create a folder `videos`. Iterate over all fables and create a video.