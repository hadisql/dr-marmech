# Dr Marmech Ilias — Cabinet d’ophtalmologie

Site vitrine bilingue français / arabe, avec les photographies et le logo fournis pour le cabinet à Casablanca.

- Site : https://drmarmech.pages.dev/
- Version arabe : https://drmarmech.pages.dev/ar.html
- Hébergement : Cloudflare Pages, projet `drmarmech`, publication par import direct.
- GitHub Pages : publication à désactiver ; ne pas republier la branche `gh-pages`.
- Source : branche `main`, fichiers du site dans `dist/`.

Le site utilise uniquement HTML, CSS et JavaScript, sans dépendance à installer, compilation, VPS, base de données, formulaire patient ni suivi publicitaire. Les photos et les polices système sont locales.

## Consulter et modifier le site

Ouvrir `dist/index.html` ou lancer depuis ce dossier :

```sh
python3 -m http.server 4173 --directory dist
```

Puis ouvrir http://localhost:4173.

`dist/config.js` regroupe le nom, la présentation, l’adresse, les deux téléphones, l’e-mail, les horaires et les liens externes. Les champs terminés par `Ar` contiennent leur version arabe. Les horaires sont volontairement indiqués comme restant à confirmer auprès du cabinet.

Les coordonnées de la carte de visite sont conservées. La photo de façade comporte d’autres numéros ; ils n’ont pas été repris dans les liens d’appel, conformément au choix du commanditaire.

## Maintenir la traduction arabe

1. Modifier le contenu français dans `dist/index.html`.
2. Adapter les traductions dans `tools/generate-ar.py`.
3. Lancer `python3 tools/generate-ar.py` : le script reconstruit `dist/ar.html` et signale tout texte non traduit.

Le sélecteur de langue conserve la section visitée. La page arabe utilise `lang="ar"` et `dir="rtl"`, avec une mise en page adaptée, tout en conservant le sens de lecture des numéros et de l’e-mail.

## Publier une mise à jour

Après modification des sources sur `main` :

```sh
python3 tools/generate-ar.py
node --check dist/app.js
node --check dist/config.js
git add README.md dist tools .gitignore
git commit -m "Mettre à jour le site"
git push origin main
```

Dans Cloudflare : ouvrir **Workers & Pages → drmarmech → Create deployment**, choisir la production, puis déposer le contenu du dossier `dist/` ou un ZIP contenant directement `index.html` à sa racine. Le projet utilise Direct Upload : un simple push GitHub ne le redéploie pas automatiquement.

Le dépôt GitHub sert à conserver les sources. GitHub Pages ne doit plus servir le site ; ne pas envoyer de nouvelle version vers `gh-pages`.

## Photographies et vérifications

Le portrait n’apparaît qu’une fois en ouverture. La photo au bloc accompagne la présentation du médecin ; les cinq vues intérieures composent la galerie ; la façade sert de repère près de l’adresse. Les images peuvent être agrandies et disposent de légendes et de textes alternatifs dans les deux langues.

Les coordonnées, le nom arabe et les pratiques proviennent des éléments fournis. Aucun diplôme ni témoignage n’a été ajouté. La galerie, la navigation et les versions française et arabe ont été vérifiées dans le navigateur sur ordinateur et mobile. Les photos ne sont pas retournées en mode arabe.
