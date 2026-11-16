# Relier GitHub à Cloudflare Pages

Le site reste intégralement statique. Aucune API Google, aucune facturation Google et aucun serveur ne sont nécessaires.

Pour que GitHub publie sur le compte Cloudflare, il lui faut une autorisation de déploiement. Ce jeton Cloudflare est distinct d’une clé Google et ne nécessite pas de renseigner un moyen de paiement.

## Une seule configuration manuelle

1. Ouvrir https://dash.cloudflare.com/profile/api-tokens puis **Create Token → Create Custom Token**.
2. Nom : `GitHub drmarmech Pages`. Permission : **Account → Cloudflare Pages → Edit**. Dans **Account Resources**, sélectionner uniquement le compte contenant `drmarmech` (identifiant `26e47291c4cca8e3aa10b8f2b4d9db52`). Ne pas ajouter de permission DNS, Zone ou de gestion du compte. Cette permission porte sur Pages dans ce compte ; Cloudflare ne permet pas de la limiter à un seul projet Pages.
3. Créer le jeton et copier sa valeur. Ne pas l’envoyer dans le chat, ni l’enregistrer dans les sources du site.
4. Ouvrir https://github.com/hadisql/dr-marmech/settings/environments puis **production → Environment secrets → Add environment secret**.
5. Nom exact : `CLOUDFLARE_API_TOKEN`. Coller la valeur dans le champ secret et enregistrer. L’identifiant de compte `CLOUDFLARE_ACCOUNT_ID` est déjà configuré dans cet environnement.

Enregistrer ce secret n’entraîne aucune publication. Les déploiements attendront toujours la validation de `hadisql`.

## Ce qui est déjà configuré

- Environnement GitHub `production`, limité à la branche `main`.
- Validation obligatoire par `hadisql` ; contournement par les administrateurs désactivé.
- Workflow `.github/workflows/deploy.yml` : contrôles des deux langues, tests du carrousel, puis publication par Wrangler après validation.
- Le projet Cloudflare Direct Upload et l’adresse https://drmarmech.pages.dev/ sont conservés.
- GitHub Pages reste désactivé.

La configuration distante de l’environnement est indépendante du fichier YAML : ne pas supprimer sa protection dans les paramètres du dépôt.

## Publier une version validée

Fusionner la proposition sur `main`. Dans **Actions**, ouvrir l’exécution **Vérifier et publier sur Cloudflare**, vérifier le commit puis utiliser **Review deployments → production → Approve and deploy**. GitHub lance alors automatiquement la publication. Aucun export ZIP n’est nécessaire.

Sans jeton Cloudflare, la publication échoue avec un message explicite. Aucune étape de publication ne s’exécute sur une pull request.

Documentation officielle : https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/
