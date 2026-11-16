# Dr Marmech Ilias — Cabinet d’ophtalmologie

Site vitrine français / arabe du cabinet à Casablanca, avec les photographies et le logo fournis.

- Site : https://drmarmech.pages.dev/
- Arabe : https://drmarmech.pages.dev/ar.html
- Sources : https://github.com/hadisql/dr-marmech, branche `main` ; fichiers publiés dans `dist/`.
- Hébergement : Cloudflare Pages, projet Direct Upload `drmarmech`.
- GitHub Pages reste désactivé ; ne pas republier `gh-pages`.

Le site utilise HTML, CSS et JavaScript. Il ne nécessite aucun VPS, base de données, API Google ni service payant pour les avis. Les dépendances Node servent uniquement aux vérifications et à la publication. Les images et les polices système sont locales. Les avis sont intégrés aux sources ; la carte de localisation est un cadre Google Maps chargé à proximité de son affichage, sans clé API ni compte de facturation Google. Elle pointe sur la fiche exacte du cabinet et s’affiche en français ou en arabe selon la page.

## Prévisualiser

```sh
python3 -m http.server 4173 --bind 0.0.0.0 --directory dist
```

Ouvrir http://localhost:4173 ; depuis le mobile connecté au même Tailscale, http://100.64.0.4:4173 si le pare-feu autorise Python.

Pour les vérifications :

```sh
npm ci
npm run build
```

Le build reconstruit la version arabe, vérifie les références locales et exécute les tests du carrousel en français et en arabe. Il ne publie rien.

## Modifier les informations

`dist/config.js` regroupe l’identité, la présentation, l’adresse, les téléphones, l’e-mail, les horaires et les liens Maps / WhatsApp. Les champs terminés par `Ar` sont en arabe.

Les coordonnées de la carte de visite sont conservées. La façade affiche d’autres numéros, non repris à la demande du commanditaire. Les horaires et le lien WhatsApp proviennent de la fiche Maps consultée le 16 novembre 2026 ; les horaires des jours fériés restent à confirmer. Aucun diplôme ni qualification supplémentaire n’est déduit de Google Maps. La présentation est rédigée à partir des informations confirmées ; le descriptif professionnel complet de la fiche n’a pas été accessible.

Après modification du français dans `dist/index.html`, adapter `tools/generate-ar.py` et lancer `npm run build`. Le générateur signale tout texte ou libellé accessible non traduit. La page arabe utilise `lang="ar"`, `dir="rtl"` et conserve les coordonnées numériques de gauche à droite.

## Mettre à jour les avis

`dist/reviews-data.js` contient la sélection manuelle, la date du relevé et les textes originaux, avec traduction arabe facultative. Les avis, notes et liens ont été fournis par le commanditaire le 16 novembre 2026. Quatre avis distincts ont été retenus ; le texte attribué à fati fleur elhalouani était identique à celui de Salim dans le relevé fourni et n’a pas été repris deux fois.

Pour ajouter un avis, renseigner :

- `author.name` : nom public, à conserver tel qu’affiché ; `author.profileUrl` est facultatif.
- `rating` : note vérifiée de 4 ou 5 étoiles.
- `text` : extrait original, sans modification du sens ; `textAr` : traduction du site, signalée comme telle.
- `sourceUrl` : lien individuel de partage Google Maps.
- `publishedLabel` et `publishedLabelAr` : indication relative au moment du relevé. Utiliser `publishTime` uniquement si la date exacte est connue.
- `selectedOn` : date de consultation de la sélection, au format `YYYY-MM-DD`.

Le carrousel conserve l’ordre des entrées. Il montre deux cartes sur ordinateur et une sur mobile, sans défilement automatique, avec commandes tactiles et clavier. Les avis inférieurs à quatre étoiles sont exclus. La date du relevé reste dans les sources ; aucune note globale ni compteur Google n’est figé. Les indications de sélection et de maintenance ne sont pas affichées dans le carrousel. En arabe, le texte français original reste accessible. Sans JavaScript, le lien vers tous les avis reste utilisable.

Les avis ne se synchronisent pas : une nouvelle sélection demande une modification du fichier, puis une publication validée. Les données synthétiques des tests sont hors de `dist/` et ne sont jamais publiées.

## Publication automatique après validation

Le workflow `.github/workflows/deploy.yml` vérifie chaque pull request et chaque push sur `main`. La publication Cloudflare ne peut partir que de `main`, après validation de `hadisql` dans l’environnement protégé `production`. Le déploiement publie automatiquement `dist/` avec Wrangler, sans ZIP.

La configuration initiale du jeton Cloudflare est décrite dans [docs/cloudflare-github.md](docs/cloudflare-github.md). Aucun secret ne doit apparaître dans les fichiers versionnés. Les protections de l’environnement GitHub sont configurées à distance et doivent être conservées.

## Photographies

Le portrait n’apparaît qu’une fois en ouverture. La photo au bloc accompagne le médecin ; cinq vues intérieures composent la galerie ; la façade sert de repère près de l’adresse. Les images peuvent être agrandies, avec légendes et textes alternatifs bilingues. Aucun avis ni photo de profil n’est récupéré automatiquement depuis Google.
