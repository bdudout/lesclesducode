// Service worker : met toute l'appli en cache pour jouer sans connexion.
// Changer VERSION à chaque mise en ligne pour que les tablettes récupèrent la mise à jour.

const VERSION = 'cdc-v4';

const FICHIERS = [
  './', 'index.html', 'jeu.html', 'referents.html', 'enseignants.html', 'manifest.webmanifest',
  'css/app.css',
  'js/data.js', 'js/audio.js', 'js/appui-long.js', 'js/natif.js', 'js/series.js', 'js/menu.js', 'js/jeu.js', 'js/pwa.js',
  'js/moteur-association.js', 'js/moteur-ecriture.js',
  'data/referentiel.json', 'data/jeux.json', 'img/images.json', 'son/sons.json',
  'fonts/andika-400.woff2', 'fonts/andika-700.woff2', 'fonts/playwrite-fr-moderne.woff',
  'img/icone.svg', 'img/icone-192.png', 'img/icone-512.png', 'img/icone-180.png',
];

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(VERSION);
    await cache.addAll(FICHIERS);
    // dessins et sons déposés : listés dans leurs index respectifs
    const images = await (await fetch('img/images.json')).json();
    const sons = await (await fetch('son/sons.json')).json();
    await cache.addAll([...images.map(f => `img/referents/${f}`), ...sons.map(f => `son/${f}`)]);
    self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    for (const cle of await caches.keys()) if (cle !== VERSION) await caches.delete(cle);
    self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  event.respondWith((async () => {
    const enCache = await caches.match(event.request, { ignoreSearch: true });
    return enCache || fetch(event.request);
  })());
});
