# SQLVault Gateway — site vitrine

Site public de SQLVault Gateway (DEF TECH 2.0), publié avec GitHub Pages sur **https://sqlvaultgateway.github.io**
(puis, plus tard, sur un nom de domaine propre : voir « Ajouter un nom de domaine »).
Site statique : HTML, CSS et un peu de JavaScript, sans dépendance ni étape de construction.

```
index.html        page d'accueil (toutes les sections)
404.html          page « introuvable »
assets/style.css  mise en forme (ordinateur, tablette, téléphone)
assets/site.js    menu mobile, agrandissement des captures, animations
assets/img/       logo, captures, image de partage (og-cover.jpg)
assets/db/        logos des bases (Devicon, licence MIT)
assets/docs/      PDF publics : fiche produit, note DSI / RSSI (guide et document technique : sur demande)
assets/video/     vidéo de présentation
```

Aperçu local : `python3 -m http.server 8000`, puis http://localhost:8000.

## Mise en ligne (sans nom de domaine)

### 1. Compte GitHub
- Créer le compte `sqlvaultgateway` (ou, mieux, une **organisation** `sqlvaultgateway` rattachée à votre compte personnel, avec la double authentification activée).
- Créer un dépôt **public**, vide, nommé exactement `sqlvaultgateway.github.io`.

### 2. Envoyer le site
```bash
cd ~/Documents/bdk/sqlvaultgateway.io
git add .
git commit -m "Site vitrine SQLVault Gateway"
git branch -M main
git remote add origin https://github.com/sqlvaultgateway/sqlvaultgateway.github.io.git
git push -u origin main
```

### 3. Activer GitHub Pages
Dépôt → **Settings → Pages** : *Source* **Deploy from a branch**, branche `main`, dossier `/ (root)`.
Le site est en ligne en une à deux minutes sur **https://sqlvaultgateway.github.io** (HTTPS inclus).

## Ajouter un nom de domaine (plus tard)

1. Acheter le domaine (par exemple `sqlvaultgateway.com` ou `sqlvaultgateway.io`).
2. Chez le vendeur, ajouter les enregistrements DNS :

| Type | Nom | Valeur |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| AAAA | @ | 2606:50c0:8000::153 |
| AAAA | @ | 2606:50c0:8001::153 |
| AAAA | @ | 2606:50c0:8002::153 |
| AAAA | @ | 2606:50c0:8003::153 |
| CNAME | www | sqlvaultgateway.github.io |

3. Dépôt → **Settings → Pages → Custom domain** : saisir le domaine, enregistrer (GitHub crée le fichier `CNAME`), puis cocher **Enforce HTTPS**.
4. Remplacer `https://sqlvaultgateway.github.io` par la nouvelle adresse dans `index.html`, `sitemap.xml` et `robots.txt`.
5. Organisation GitHub → **Settings → Pages → Add a domain** : ajouter l'enregistrement **TXT** fourni, qui empêche quiconque d'utiliser votre domaine ailleurs.

L'ancienne adresse `sqlvaultgateway.github.io` redirigera alors automatiquement vers le nouveau domaine.

## Mettre à jour
- Textes : `index.html`. Couleurs et mise en page : `assets/style.css`.
- Documents : remplacer les PDF de `assets/docs/` en gardant les mêmes noms.
- Adresse de contact : rechercher `mbodjiousseynou94@gmail.com` dans `index.html` (5 occurrences) le jour où une adresse `contact@sqlvaultgateway.io` existe.
- Après chaque modification : `git add . && git commit -m "…" && git push`. Le site se met à jour en une à deux minutes.
