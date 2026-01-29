# API Collection (Bruno)

Ce dossier contient la collection de tests API pour le projet, gérée avec **Bruno**, un client API open-source "Git-friendly".

## Architecture des fichiers
Contrairement aux outils cloud, Bruno sauvegarde les requêtes dans des fichiers texte lisibles (`.bru`). Cela permet de versionner les appels API directement avec le code source :

* `GET Quotes.bru` : Requêtes liées au service de citations.
* `GET Search.bru` : Requêtes liées au moteur de recherche.
* `GET Users.bru` : Requêtes liées à la gestion utilisateur.
* `/environments` : Configuration des variables selon le contexte (LocalHost, Production, Recette).

---

## Configuration et Utilisation

### 1. Installation
Si ce n'est pas déjà fait, installez le client Bruno (disponible sur Windows, Mac et Linux) :
👉 [https://www.usebruno.com/](https://www.usebruno.com/)

### 2. Import de la collection
1. Ouvrez l'application Bruno.
2. Cliquez sur **"Open Collection"**.
3. Sélectionnez le dossier `SAE503-BrunoCollection` présent dans ce dépôt.

### 3. Gestion des Environnements
Pour que les requêtes fonctionnent, vous devez sélectionner un environnement en haut à droite de l'interface (ex: `LocalHost`).

| Variable | Usage |
| :--- | :--- |
| `{{proto}}` | Protocole utilisé (http/https) |
| `{{server}}` | Host cible (ex: localhost) |
| `{{quotes_srv}}` | Port/URL du service Quotes |
| `{{users_srv}}` | Port/URL du service Users |
| `{{search_srv}}` | Port/URL du service Search |

### 4. Sécurité (Secrets)
Certaines variables, comme `admin_key`, sont marquées comme **Secret** dans Bruno.
> [!IMPORTANT]
> Les valeurs des secrets ne sont pas stockées dans les fichiers `.bru` pour éviter les fuites sur Git. Vous devrez les renseigner manuellement dans votre environnement lors de son chargement.