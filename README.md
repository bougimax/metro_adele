# Métro Adèle

## Etape 1 : Installer Python

Tout d'abord, installer [HomeBrew](https://brew.sh/) avec la commande suivante (dans le terminal, c'est une
app du mac):

*Quand je dis avec la commande ou rentrer la commander, juste tu copies, tu colles dans le terminal et tu
tapes la touche entrée*

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Puis

```sh
brew update
```

Et enfin:

```sh
brew install python
```

Pour vérifier que ça c'est bien installé:

```sh
python3 --version
```

Où tu devrais obtenir:

```sh
Python 3.x.x
```

où les x vont être des numéros chez toi


## Etape 2 : Installer les dépendances

Installer les dépendances du projet, on commence par créer un environnement virtuel:

```sh
python3 -m venv .venv
```

puis on se met dedans pour pouvoir y installer nos dépendances:

```sh
source .venv/bin/activate
```

Enfin tu peux exécuter:

```sh
python -m pip install -r requirements.txt
```

## Etape 3 : Lancer l'application

Tu lances l'application avec:

```sh
python3 app.py
```

Et tu vas obtenir une réponse du style:

```sh
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

Enfin pour avoir dans ton navigateur tu laisses tourner ça et tu copie colle l'adresse [après le `Running
on`](http://127.0.0.1:5000).
