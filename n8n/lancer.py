# Lance à la main un circuit planifié : copie temporaire avec un webhook secret à la place du déclencheur horaire,
# appel, attente de la fin, suppression de la copie. Usage : python3 -I lancer.py <workflow_id>
import json, os, sys, time, secrets, urllib.request
B = 'https://n8n.krady.fr/api/v1'; K = os.environ['N8N_API_KEY']
def api(method, path, body=None):
    req = urllib.request.Request(B + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={'X-N8N-API-KEY': K, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r: return json.loads(r.read() or b'{}')
wf = api('GET', '/workflows/' + sys.argv[1])
chemin = 'test-' + secrets.token_hex(12)
for n in wf['nodes']:
    if n['type'].endswith('scheduleTrigger'):
        n.update(type='n8n-nodes-base.webhook', typeVersion=2, parameters={'httpMethod': 'POST', 'path': chemin, 'responseMode': 'onReceived', 'options': {}})
        n['webhookId'] = secrets.token_hex(16)
copie = api('POST', '/workflows', {'name': wf['name'] + ' (test manuel)', 'nodes': wf['nodes'], 'connections': wf['connections'], 'settings': wf.get('settings', {})})
try:
    api('POST', '/workflows/%s/activate' % copie['id'])
    time.sleep(2)
    urllib.request.urlopen(urllib.request.Request('https://n8n.krady.fr/webhook/' + chemin, data=b'{}', method='POST', headers={'Content-Type': 'application/json'})).read()
    for _ in range(90):
        time.sleep(3)
        ex = api('GET', '/executions?workflowId=%s&limit=1&includeData=true' % copie['id']).get('data', [])
        if ex and ex[0].get('finished') is not None and ex[0].get('status') not in ('running', 'new', 'waiting'):
            e = ex[0]; print('statut', e['status'], 'début', e.get('startedAt'), 'fin', e.get('stoppedAt'))
            rd = (e.get('data') or {}).get('resultData', {})
            if rd.get('error'): print('erreur:', rd['error'].get('message'), '| nœud:', (rd['error'].get('node') or {}).get('name'))
            for nom, runs in rd.get('runData', {}).items():
                items = sum(len(o or []) for r in runs for o in (r.get('data', {}).get('main') or []))
                err = runs[-1].get('error', {}).get('message') if runs[-1].get('error') else ''
                print('  %-40s %4d éléments %s' % (nom, items, err))
            break
    else: print('pas fini après 4 min 30')
finally:
    api('POST', '/workflows/%s/deactivate' % copie['id']); api('DELETE', '/workflows/' + copie['id']); print('copie supprimée')
