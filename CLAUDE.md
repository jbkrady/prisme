# Prisme — règles du projet

> Lu automatiquement par Claude Code. Garder à jour quand une décision change.
> Dépôt **public** : aucun secret, aucun jeton, aucune adresse d'abonné ici.

## Le produit

L'essentiel de l'IA pour les Product Managers, chaque matin à 8 h 30. Un agent lit l'actualité, garde 5 nouveautés au plus et dit ce qu'elles changent pour un PM. Bêta avec des PM de la promo 35 formés par Noé, puis ouverture à tous les PM. Ton : tutoiement, sans emoji. Mascotte : **Tri** (palette « Holo »).

## Comment ça tourne (heure de Paris)

| Heure | Où | Quoi |
|---|---|---|
| 6 h | n8n · Prisme · Collecte | lit 14 sources (flux RSS + Google Actualités), garde 48 h, écarte le déjà envoyé → table `prisme_candidats` |
| 7 h 30 | Routine Claude « Prisme · édition du matin » | lit les candidats (connecteur n8n), les confie à l'agent `prisme` (skill `grille-prisme`), renvoie le JSON → n8n · Prisme · Réception → `prisme_editions` |
| 8 h 30 | n8n · Prisme · Envoi | met en page (gabarit mail v2, nœud « Mettre en page »), envoie à chaque abonné actif de `prisme_abonnes`, archive la version en ligne dans `prisme_pages` |

Autres circuits n8n : Inscription, Confirmation, Désinscription, Votes, Numéro en ligne (« Voir dans le navigateur »). Ils ont un filtre anti-robots : tester avec un user-agent de navigateur, pas un curl brut.

**Où tourne n8n.** L'essai n8n Cloud (`jbkrady.app.n8n.cloud`) a pris fin le 3 octobre 2026. n8n est auto-hébergé sur un VPS Hostinger KVM 2 (`n8n.krady.fr`, Docker, fuseau `Europe/Paris`, historique des exécutions purgé à 14 jours). Les liens publics (site, mails) passent par `prisme.krady.fr/api/<circuit>`, que le Worker relaie vers n8n : changer d'hébergeur, c'est changer une ligne de `worker.js`. La routine parle à n8n par le connecteur MCP de l'instance (`n8n.krady.fr/mcp-server/http`) ; ses identifiants de tableau et de circuit sont écrits dans son texte : les mettre à jour si on recrée un tableau ou un circuit.

**Envoi des mails.** Par Resend (offre gratuite : 100 mails par jour, 3 000 par mois), en SMTP depuis `Prisme <prisme@krady.fr>`, réponses vers l'adresse @krady.fr de JB (iCloud). Plus de Google pour Prisme. Au-delà d'environ 90 abonnés, passer à Brevo gratuit (300 par jour, activation par leur support à demander à l'avance) ou à Resend payant : seul l'identifiant SMTP change dans n8n.

**Le serveur.** VPS Hostinger (Düsseldorf), système « Ubuntu 24.04 with Docker and Traefik » et application n8n du gestionnaire Docker de Hostinger. n8n : `/docker/n8n-hsgw/docker-compose.yml` (adapté : domaine `n8n.krady.fr`, port 5678 fermé au public, cookie sécurisé, purge à 14 jours ; l'original Hostinger est gardé à côté en `.hostinger-origine`). Traefik (`/docker/traefik`) sert le HTTPS (Let's Encrypt). Pare-feu Hostinger : 22, 80, 443. Accès SSH de Claude : clé `~/.ssh/prisme_vps` sur le Mac de JB (`ssh -i ~/.ssh/prisme_vps root@n8n.krady.fr`). Clé API n8n : `~/.config/prisme/n8n.env` sur le Mac (jamais dans le dépôt ni dans le chat). Le webhook de Réception a une adresse secrète, sur l'instance seulement : la routine l'appelle par l'identifiant du circuit (MCP), pas par l'adresse.

**Entretien du serveur.** Mettre n8n à jour chaque mois (failles graves en 2026) : `cd /docker/n8n-hsgw && docker compose pull && docker compose up -d`, de préférence l'après-midi. Ne pas utiliser le bouton « mettre à jour » de l'application dans hPanel : il pourrait remettre le fichier d'origine de Hostinger. Le bouton « Ouvrir l'application » de hPanel ouvre bien https://n8n.krady.fr (vérifié le 8 octobre 2026). Si Hermes s'installe sur le même VPS : conteneur séparé, sans accès au dossier de n8n ni au socket Docker, mémoire plafonnée, rien de lourd entre 6 h et 8 h 45.

## Le dépôt

- `.claude/skills/grille-prisme/SKILL.md` : la méthode (écarter, classer, rédiger, JSON strict). La routine la relit à chaque passage : un push sur `main` suffit pour la changer.
- `.claude/agents/prisme.md` : le rédacteur, sans aucun outil (il lit du contenu web : chacun n'a que les droits de son rôle).
- `site/` : prisme.krady.fr (page d'inscription, `img/` pour Tri, `mail/` pour les images des mails, `apercu/` pour l'exemple de numéro). Design : projet Claude Design « Lancer la routine », fichiers « Prisme Site v2 » et « Prisme Mail ».
- `design/mascotte/` : le kit de Tri (5 expressions, 1x et 2x).
- `n8n/` : l'export des 8 circuits (sauvegarde, base de réinstallation) et la liste des tables. Sans identifiants ni données.
- `worker.js` : sert `site/` et relaie `/api/*` vers les webhooks n8n (liste blanche des circuits publics).

## Publier

- Site : `npx wrangler deploy` depuis ce dossier (Worker Cloudflare `prisme`, domaine prisme.krady.fr, pas d'adresse workers.dev).
- Le gabarit du mail vit dans n8n (nœud « Mettre en page » de Prisme · Envoi) : le modifier là, puis republier le circuit, puis réexporter dans `n8n/`.
- Depuis une session Claude Code dans le cloud, `wrangler deploy` ne peut publier que `worker.js` : l'envoi des fichiers de `site/` y est refusé. Un changement de `site/` se publie depuis le Mac.

## Règles

- Ne jamais renvoyer un mail aux abonnés pour un test : tester à blanc ou vers JB seul.
- Jamais de secret ni d'adresse d'abonné dans le dépôt ou le chat.
- Chaque changement du skill part d'un constat d'usage (votes, retours, numéros reçus) : c'est la boucle racontée dans le cas Prisme du portfolio.
