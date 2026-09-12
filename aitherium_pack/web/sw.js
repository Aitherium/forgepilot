const CACHE = 'forgepilot-agents-everywhere-v3';
const BASE = new URL('./', self.location).pathname;
const SHELL = [BASE, new URL('./index.html', self.location).pathname, new URL('./manifest.webmanifest', self.location).pathname, new URL('./icon.svg', self.location).pathname, new URL('./config.js', self.location).pathname];
self.addEventListener('install', event => event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(SHELL))));
self.addEventListener('activate', event => event.waitUntil(self.clients.claim()));
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  event.respondWith(caches.match(event.request).then(cached => cached || fetch(event.request)));
});
