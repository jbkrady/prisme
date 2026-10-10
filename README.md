# Prisme

L'essentiel de l'IA pour les Product Managers, en 2 minutes, chaque matin à 8 h 30.

Prisme est un agent autonome : chaque matin, sans personne, il lit l'actualité du jour, écarte le bruit, choisit 5 nouveautés au maximum, note leur impact pour un PM et les rédige en deux phrases. Le mail suit toujours le même gabarit.

## Comment ça marche

```
6 h 00   n8n · Collecte     lit les flux de 14 sources, garde les 48 dernières heures,
                            écarte le déjà envoyé, range les candidats dans un tableau
7 h 30   Routine Claude     lit les candidats (connecteur n8n), les confie à l'agent prisme,
                            renvoie l'édition à n8n (connecteur n8n)
         n8n · Réception    vérifie l'édition et la met de côté
8 h 30   n8n · Envoi        met en page avec le gabarit Prisme et envoie
         n8n · Votes        reçoit les clics « Utile / Pas utile »
```

Les circuits n8n sont exportés dans [`n8n/`](n8n/). Depuis la fin de l'essai n8n Cloud (octobre 2026), n8n est auto-hébergé sur un VPS Hostinger et les mails partent par Resend ; les liens publics passent par `prisme.krady.fr/api/...` (`worker.js`), pour ne plus dépendre de l'adresse de n8n.

## Skill et agent : qui fait quoi

| | Rôle | Fichier |
|---|---|---|
| **Skill `grille-prisme`** | La méthode : écarter, classer, choisir, rédiger, rendre un JSON strict. | `.claude/skills/grille-prisme/SKILL.md` |
| **Agent `prisme`** | L'employé qui applique la méthode. Il n'a accès ni au web, ni à n8n, ni aux mails : il lit des textes venus d'internet, donc il ne peut rien faire d'autre que rédiger. | `.claude/agents/prisme.md` |
| **Routine** | Le chef d'orchestre : lit les candidats, appelle l'agent, renvoie l'édition. Ses seuls droits : lire un tableau et lancer un circuit n8n. | sur claude.ai/code/routines |

Chacun n'a que les droits de son rôle.

## Ce qui a changé depuis la v1

La v1 (« Lancer la routine », septembre 2026) cherchait elle-même sur le web. Douze jours d'usage ont montré :

- un mail qui changeait de forme chaque jour ;
- des articles vieux de 3 à 4 jours en moyenne ;
- les mêmes articles d'un jour à l'autre ;
- des pages presque jamais ouvertes, puis plus aucun article quand le réseau de la routine les a bloquées.

La v2 répond à chaque constat : sources fixes collectées par n8n, fenêtre de 48 h, mémoire des articles envoyés, gabarit de mail imposé par n8n et non par l'IA.

## Licence

Le code est sous licence MIT. Le nom Prisme, la mascotte Tri et les visuels (mascotte, images du site et des mails, carte de partage, icônes) restent la propriété de Jean-Baptiste Krady, tous droits réservés : ils ne sont pas publiés dans ce dépôt (voir [`LICENSE-VISUELS`](LICENSE-VISUELS)).
