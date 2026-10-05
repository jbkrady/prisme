# Les circuits n8n de Prisme

Export des 8 circuits tels qu'ils tournaient sur n8n Cloud (`jbkrady.app.n8n.cloud`) jusqu'au 2 octobre 2026, à la fin de l'essai. Ils servent de sauvegarde et de base pour la réinstallation sur un n8n auto-hébergé (`n8n.krady.fr`, VPS Hostinger).

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

- **Les identifiants** (Gmail) : à recréer sur la nouvelle instance.
- **Les données** : les 6 data tables sont à recréer (colonnes ci-dessous). Les abonnés ne passent jamais par ce dépôt.
- **L'adresse de JB** : remplacée par `ADRESSE_DE_JB` dans le nœud « Prévenir : pas d'édition » d'`envoi.json`.

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
2. Les adresses `https://jbkrady.app.n8n.cloud/webhook/...` écrites dans les nœuds (« Mettre en page » d'Envoi, « Préparer l'abonné » d'Inscription, mail de bienvenue de Confirmation) : remplacer par `https://prisme.krady.fr/api/...`. Le Worker du site (`worker.js`) relaie vers n8n.
3. Les nœuds Gmail : nouvel identifiant (SMTP Gmail avec mot de passe d'application, ou client OAuth Google à soi).
4. `ADRESSE_DE_JB` : remettre la vraie adresse, sur l'instance seulement.

Pour importer à la main : dans n8n, « Import from File » sur chaque fichier.
