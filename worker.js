// Worker de prisme.krady.fr : sert les fichiers de site/ et relaie /api/* vers les webhooks n8n.
// Les liens des mails et du site passent par prisme.krady.fr/api/... : changer d'hébergeur n8n,
// c'est changer N8N ci-dessous, sans casser un seul lien déjà envoyé.
const N8N = 'https://n8n.krady.fr/webhook';

// Seuls les circuits ouverts au public passent (pas la Réception, appelée par la routine).
const CIRCUITS = new Set([
  'prisme-inscription',
  'prisme-confirmer',
  'prisme-desinscription',
  'prisme-vote',
  'prisme-numero',
]);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (!url.pathname.startsWith('/api/')) return env.ASSETS.fetch(request);

    const circuit = url.pathname.slice('/api/'.length);
    if (!CIRCUITS.has(circuit)) return new Response('Introuvable', { status: 404 });

    // Même méthode, en-têtes (user-agent compris, pour le filtre anti-robots) et corps.
    try {
      return await fetch(new Request(N8N + '/' + circuit + url.search, request));
    } catch {
      return new Response('Prisme ne répond pas pour le moment. Réessaie dans quelques minutes.', {
        status: 502,
        headers: { 'Content-Type': 'text/plain; charset=utf-8' },
      });
    }
  },
};
