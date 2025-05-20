self.addEventListener('install', (event) => {
  console.log('[VitalAssist] Service Worker Installed');
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  console.log('[VitalAssist] Service Worker Activated');
});

self.addEventListener('fetch', function (event) {
  event.respondWith(fetch(event.request));
});
