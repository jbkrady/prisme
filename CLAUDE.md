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

## Le dépôt

- `.claude/skills/grille-prisme/SKILL.md` : la méthode (écarter, classer, rédiger, JSON strict). La routine la relit à chaque passage : un push sur `main` suffit pour la changer.
- `.claude/agents/prisme.md` : le rédacteur, sans aucun outil (il lit du contenu web : chacun n'a que les droits de son rôle).
- `site/` : prisme.krady.fr (page d'inscription, `img/` pour Tri, `mail/` pour les images des mails, `apercu/` pour l'exemple de numéro). Design : projet Claude Design « Lancer la routine », fichiers « Prisme Site v2 » et « Prisme Mail ».
- `design/mascotte/` : le kit de Tri (5 expressions, 1x et 2x).

## Publier

- Site : `npx wrangler deploy` depuis ce dossier (Worker Cloudflare `prisme`, domaine prisme.krady.fr, pas d'adresse workers.dev).
- Le gabarit du mail vit dans n8n (nœud « Mettre en page » de Prisme · Envoi) : le modifier là, puis republier le circuit.

## Règles

- Ne jamais renvoyer un mail aux abonnés pour un test : tester à blanc (Gmail simulé) ou vers JB seul.
- Jamais de secret ni d'adresse d'abonné dans le dépôt ou le chat.
- Chaque changement du skill part d'un constat d'usage (votes, retours, numéros reçus) : c'est la boucle racontée dans le cas Prisme du portfolio.
