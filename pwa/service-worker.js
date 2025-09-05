
// Simple service worker stub - caching static assets
const CACHE_NAME = 'cores-fragrancias-cache-v1';
const urlsToCache = ['/', '/assets/icon.png', '/pwa/manifest.json'];

self.addEventListener('install', function(event) {
  event.waitUntil(caches.open(CACHE_NAME).then(function(cache) {
    return cache.addAll(urlsToCache);
  }));
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});
