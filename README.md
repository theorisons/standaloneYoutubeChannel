- [:fr: : Lire en Français](#chaîne-youtube-autonome)
- [:gb: / :us: : Read in English](#standolone-youtube-channel)

# Standolone YouTube channel

## Overview 

Autonomous YouTube channel source code. Global explanation in the video **[Title](https://youtu.be/LIEN "Watch the video")**.

The project is to create automatic contents for a YouTube channel. Videos are about _les fables de La Fontaine_, French stories that are in public domain.

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

### Pixabay

Used to get copyright free images.
The API needs authentification with private token. It is necessary to login in with an account and add the token to the file `/API/credentials.py`.

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



# Chaîne YouTube autonome

## Présentation

Code de la chaîne youtube autonome, présenté dans la video **[Titre](https://youtu.be/LIEN "Voir la vidéo")**.

Le projet consiste à alimenter une chaîne YouTube en contenue de manière autonome. Le thème choisi est _les fables de La Fontaine_ (étant des oeuvres du domaine public).

- Les fables sont récupérées grâce à du _webscrapping_ `/webScrapping` puis placé dans un dossier selon leur ouvrage `/webScrapping/fables`.

Le contenu en Français possède une extension `.fr`, celui en Anglais une extension `.en`.

- Les titres, descriptions, tags `/descriptionGenerator` sont générés grâce aux textes des fables puis placé dans un dossier `/descriptionGenerator/descriptions`. Les extensions sont :
  - `.description` pour les descriptions
  - `.tag` pour les tags
  - `.title` pour les titres

Le contenu en Français possède une extension `.fr`, celui en Anglais une extension `.en`.

- Le montage vidéo `/videoEditing` s'appuie sur les textes.
- Les API `/API` gèrent les différents service:
  - Récupération d'images libre de droit
  - Traduction de texte Français / Anglais
  - Conversion Texte vers Parole (Anglais et Français)
  - Upload de vidéo sur YouTube
  - Réponse aux commentaires sur YouTube

## Dépendences

- Python 3
- BeautifulSoup
- moviepy
- boto3

## API

### AWS

Le service cloud d'Amazon est utilisé pour:

- Traduire du texte avec **[Amazon Translate](https://aws.amazon.com/fr/translate/ "Voir la présentation")**
- Convertir du texte en voix avec **[Amazon Polly](https://aws.amazon.com/fr/polly/ "Voir la présentation")**

### Google

Les API de Google sont utilisées pour uploader des vidéos sur YouTube avec titre, description, tags et miniature.

### Pixabay

Permet de récupérer des images libres de droits.
Les requêtes API nécessitent d'être identifier avec un jeton privé. Il faut donc s'enregistrer avec un compte sur les différents service et ajouter ses jetons dans le fichier `/API/credentials.py`.

## Exécution

Liste des commandes pour réaliser toutes les manipulations pensées pour ce projet.
On suppose que le répertoire de travail est `./` .

### WebScrapping des textes de Fables

```
cd ./webScrapping
python3 webscrappingFrench.py
```

Crée un nouveau répertoire `fables` avec des sous-dossiers contenant le numéro du livre. Dans chaque sous-dossier, se situe des fichiers textes dont le nom est `<numeroFable>.fr`.

La structure des fables est:

```
<Numéro du livre>
<Numéro de la fable>
<Titre de la fable>
<Contenu de la fable>
```

### Traduction des fables en Anglais

```
cd ./webScrapping
python3 translateFablesEnglish.py
```

Parcourt tous les fichiers de fables `<numeroFable>.fr` puis crée un nouveau fichier `<numeroFable>.en` contenu le contenu traduit.

**ATTENTION AUCUN FICHIER `.en` NE DOIT ETRE PRESENT** sinon le contenu sera simplement écrasé. (Vient du fait que l'on itère sur tous les fichiers et non juste les fichiers en `.fr`).

La structure des fables reste la même.

### Génération des métadonnées des vidéos

```
cd ./descriptionGenerator
python3 generator.py
```

Crée un répertoire `descriptions`. Parcourt tous les fichiers de fables `<numeroFable>.*` puis crée un 3 fichiers par fables (titre, tags et description).

### Génération des vidéos

```
cd ./videoEditing
python3 main.py
```

Crée un répertoire `videos`. Parcourt toutes les fables et construit la vidéo.
