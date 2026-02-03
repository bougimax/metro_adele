# Métro Adèle

*Quand je dis avec la commande ou rentrer la commander, juste tu copies, tu colles dans le terminal et tu
tapes la touche entrée*

## Etape 1 : Cloner le Git

Va dans ton terminal, théoriquement tu vas arriver à ton `Home` directory, i.e. le dossier que tu as quand tu
ouvres Finder. Là cette étape va consister à télécharger les fichiers que j'ai édité, pour ça tu vas devoir
choisir où tu les mets. Pour ça ce que tu peux faire c'est aller dans ton Finder, créer un dossier là où tu
veux et ensuite tu fais clic-droit dessus et normalement tu devrais avoir une option **Nouveau terminal au
dossier**. Si tu cliques dessus ça va t'ouvrir un terminal dans ce dossier.

A partir de là tu peux faire:

```sh
git clone https://github.com/bougimax/metro_adele.git
```

Puis:

```sh
cd metro_adele
```

Pour aller dans le dossier


## Etape 2 : Installer Python

Ensuite tu vas installer [HomeBrew](https://brew.sh/) avec la commande suivante (dans le terminal, c'est une
app du mac):


```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Puis:

```sh
brew update
```

Ca va permettre de télécharger `python` avec:

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


## Etape 3 : Installer les dépendances

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
python3 -m pip install -r requirements.txt
```

## Etape 4 : Lancer l'application

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
