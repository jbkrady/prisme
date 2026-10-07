# Les circuits n8n de Prisme

Les 8 circuits de Prisme, exportés de n8n Cloud (`jbkrady.app.n8n.cloud`) à la fin de l'essai (3 octobre 2026), puis adaptés au n8n auto-hébergé (`n8n.krady.fr`, VPS Hostinger) : liens par `prisme.krady.fr/api/...`, envoi par Resend en SMTP, numérotation qui part du 8 octobre 2026 (N° 1).

| Fichier | Circuit | Déclencheur |
|---|---|---|
| `collecte.json` | Prisme · Collecte | 6 h, lit les 14 sources → `prisme_candidats` |
| `reception.json` | Prisme · Réception | webhook `prisme-edition`, appelé par la routine Claude → `prisme_editions` |
| `envoi.json` | Prisme · Envoi | 8 h 30, gabarit du mail (nœud « Mettre en page ») |
| `inscription.json` | Prisme · Inscription | webhook `prisme-inscription` (formulaire du site) |
| `confirmation.json` | Prisme · Confirmation | webhook `prisme-confirmer` (double opt-in) |
| `desinscription.json` | Prisme · Désinscription | webhook `prisme-desinscription` |
| `votes.json` | Prisme · Votes | webhook `prisme-vote` |
| `numero-en-ligne.json` | Prisme · Numéro en ligne | webhook `prisme-numero` (« Voir dans le navigateur ») |

## Ce que l'export ne contient pas

- **Les identifiants** : l'identifiant SMTP « Prisme Resend » se crée sur l'instance (clé Resend, jamais dans le dépôt). Sur n8n.krady.fr, il s'appelle « SMTP account » : seul son identifiant compte.
- **Les données** : les 6 data tables sont à recréer (colonnes ci-dessous). Les abonnés ne passent jamais par ce dépôt.
- **L'adresse de JB** : remplacée par `ADRESSE_DE_JB` (destinataire de « Prévenir : pas d'édition », adresse de réponse des mails aux abonnés).

| Table | Colonnes (texte sauf mention) |
|---|---|
| `prisme_candidats` | date_edition, cid, titre, source, url, date_pub, extrait |
| `prisme_editions` | date_edition, statut, nb_articles (nombre), contenu |
| `prisme_envoyes` | url, date_edition |
| `prisme_pages` | date_edition, html |
| `prisme_votes` | date_edition, vote, jeton |
| `prisme_abonnes` | email, jeton, statut, confirme_le |

## À changer en réinstallant

1. Les identifiants de tables (`dataTableId`) : remplacer par ceux de la nouvelle instance.
2. Les 4 nœuds d'envoi (« Send Email ») : choisir l'identifiant SMTP « Prisme Resend ».
3. `ADRESSE_DE_JB` : remettre la vraie adresse, sur l'instance seulement.
4. Rendre « Prisme · Réception » disponible en MCP, puis mettre à jour dans le texte de la routine les identifiants du tableau `prisme_candidats`, du projet et du circuit Réception.

Les adresses publiques ne changent plus : elles passent toutes par `prisme.krady.fr/api/...` et `worker.js` relaie vers n8n.

Pour importer à la main : dans n8n, « Import from File » sur chaque fichier. La réinstallation du 8 octobre 2026 s'est faite par l'API publique de n8n (`POST /api/v1/data-tables`, `POST /api/v1/workflows`, puis `/activate`), avec une copie des fichiers adaptée hors du dépôt.

## Lancer à la main un circuit planifié

Collecte et Envoi n'ont qu'un déclencheur horaire : ni l'API publique ni `n8n execute` ne savent les lancer. `lancer.py` en fait une copie temporaire déclenchée par un webhook secret, l'appelle, affiche le résultat nœud par nœud, puis supprime la copie :

```
set -a; . ~/.config/prisme/n8n.env; set +a
python3 -I n8n/lancer.py <identifiant du circuit>
```

Attention : un Envoi lancé à la main envoie vraiment le mail à tous les abonnés actifs.

Piège de minuit : la routine Claude ne connaît que la date UTC. Lancée à la main entre minuit à Paris et 2 h (1 h l'hiver), elle cherche les candidats de la veille et dépose une édition vide (que la Réception date du jour, heure de Paris). Tester la routine en journée, ou copier d'abord les candidats sous la date UTC. À 7 h 30, les deux dates coïncident.
