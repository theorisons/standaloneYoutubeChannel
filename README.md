_:gb: / :us: : Bellow !_

---

---

_:fr: Français ici_

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

Les requêtes API nécessitent d'être identifier avec un jeton privé. Il faut donc s'enregistrer avec un compte sur les différents service et ajouter ses jetons dans le fichier `/API/credentials.py`.

## Exécution

Liste des commandes pour réaliser toutes les manipulations pensées pour ce projet.
On suppose que le répertoire de travail est `./` .

### WebScrapping des textes de Fables

```
cd ./webScrapping
python3 webscrappingFrench.py
```

Crée un nouveau répertoire `fables` avec des sous-dossiers contenu le numéro du livre. Dans chaque sous-dossier, se situe des fichiers textes dont le nom est `<numeroFable>.fr`.

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

---

---

_:gb: / :us: : English here_

---

---

# Standalone YouTube Channel

## Overview

Code of the standalone youtube channel shown on the video **[Title](https://youtu.be/LINK "Watch the video")**.

---

---

```

```
