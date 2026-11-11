#!/usr/bin/env python3
"""Build the installable VocalPrep web app.

Usage:  python3 build.py      (uses the newest app/vocalprep_vNN.html)

Writes site/: index.html, sw.js (offline cache), manifest.webmanifest, icons/ (drawn here). Needs Pillow.
"""
import glob, os, re, hashlib, datetime, math

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, 'site')

SW = """/* VocalPrep offline cache, build __BUILD__ */
const CACHE = 'vocalprep-__BUILD__';
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'icons/icon-180.png', 'icons/icon-192.png', 'icons/icon-512.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('vocalprep-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
// Use what's on the iPad straight away; fetch a fresh copy in the background when online.
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  const key = req.mode === 'navigate' ? 'index.html' : req;
  e.respondWith(caches.open(CACHE).then(async c => {
    const hit = await c.match(key, { ignoreSearch: true });
    const net = fetch(req).then(r => { if (r && r.ok) c.put(key, r.clone()); return r; }).catch(() => null);
    if (hit) { e.waitUntil(net); return hit; }
    return (await net) || new Response('Offline and not yet saved on this iPad. Open the app once while online.', { status: 503, headers: { 'Content-Type': 'text/plain' } });
  }));
});
"""

MANIFEST = """{
  "name": "VocalPrep",
  "short_name": "VocalPrep",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#f2ede2",
  "theme_color": "#f2ede2",
  "icons": [
    { "src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
"""

def make_icons(out):
    # Parchment square, a near-black waveform, two markers and a region lifted out below.
    from PIL import Image, ImageDraw
    N = 1024
    im = Image.new('RGB', (N, N), (242, 237, 226)); d = ImageDraw.Draw(im)
    mid = 420
    for i in range(60):
        x = 132 + i * 12.8
        a = (0.22 + 0.78 * abs(math.sin(i * 0.37) * math.sin(i * 0.11 + 1))) * 200
        d.rounded_rectangle([x, mid - a, x + 7, mid + a], radius=3, fill=(61, 58, 54))
    for mx in (360, 664):
        d.rectangle([mx - 5, 150, mx + 5, 690], fill=(30, 29, 27)); d.rectangle([mx - 5, 130, mx + 74, 186], fill=(30, 29, 27))
    d.rounded_rectangle([360, 760, 664, 890], radius=24, fill=(30, 29, 27))
    for i in range(22):
        x = 384 + i * 12; a = (0.3 + 0.7 * abs(math.sin(i * 0.5))) * 44
        d.rectangle([x, 825 - a, x + 6, 825 + a], fill=(242, 237, 226))
    os.makedirs(os.path.join(out, 'icons'), exist_ok=True)
    for n in (180, 192, 512):
        im.resize((n, n), Image.LANCZOS).save(os.path.join(out, 'icons', f'icon-{n}.png'))

def main():
    files = glob.glob(os.path.join(HERE, 'app', 'vocalprep_v*.html'))
    def ver(p):
        m = re.search(r'_v(\d+)\.html$', p)
        return int(m.group(1)) if m else -1
    assert files, 'no app/vocalprep_vNN.html found'
    src = max(files, key=ver)
    html = open(src, encoding='utf-8').read()
    build = f'v{ver(src)}-' + datetime.datetime.now().strftime('%Y%m%d-%H%M') + '-' + hashlib.sha1(html.encode()).hexdigest()[:6]
    os.makedirs(SITE, exist_ok=True)
    open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8').write(html)
    open(os.path.join(SITE, 'sw.js'), 'w', encoding='utf-8').write(SW.replace('__BUILD__', build))
    open(os.path.join(SITE, 'manifest.webmanifest'), 'w', encoding='utf-8').write(MANIFEST)
    open(os.path.join(SITE, '.nojekyll'), 'w').write('')
    make_icons(SITE)
    print('built', build, 'from', os.path.basename(src))

if __name__ == '__main__':
    main()
