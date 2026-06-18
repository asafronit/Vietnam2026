/* Vietnam 2026 — Service Worker
 * Offline strategy:
 *   - Precache (cache-first): app shell + Leaflet lib + fonts + icons. Guaranteed offline.
 *   - HTML pages: stale-while-revalidate. Instant from cache, refreshed in background when online.
 *   - Map tiles (CartoDB): stale-while-revalidate, capped. "Warm the cache before you fly."
 *   - Google Fonts (gstatic): cache-first, so the Inter font works offline once seen.
 * Bump VERSION to force clients to refetch precached assets.
 */
const VERSION = "v3";
const PRECACHE = `vietnam2026-precache-${VERSION}`;
const RUNTIME = `vietnam2026-runtime-${VERSION}`;
const TILES = `vietnam2026-tiles-${VERSION}`;
const TILE_MAX_ENTRIES = 300;

const PRECACHE_URLS = [
  "/",
  "/index.html",
  "/design_1_map.html",
  "/itinerary.html",
  "/manifest.webmanifest",
  "/icons/icon-192.png",
  "/icons/icon-512.png",
  "/icons/icon-512-maskable.png",
  "/icons/apple-touch-icon.png",
  "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
  "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
  "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap",
];

const isTile = (url) => url.hostname.endsWith(".basemaps.cartocdn.com");
const isFont = (url) =>
  url.hostname === "fonts.gstatic.com" || url.hostname === "fonts.googleapis.com";

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(PRECACHE)
      // Per-item so one failed cross-origin asset doesn't abort the whole install.
      .then((cache) => Promise.allSettled(PRECACHE_URLS.map((u) => cache.add(u))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  const keep = new Set([PRECACHE, RUNTIME, TILES]);
  event.waitUntil(
    caches
      .keys()
      .then((names) => Promise.all(names.filter((n) => !keep.has(n)).map((n) => caches.delete(n))))
      .then(() => self.clients.claim())
  );
});

async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  const network = fetch(request)
    .then((response) => {
      if (response && (response.ok || response.type === "opaque")) {
        cache.put(request, response.clone());
      }
      return response;
    })
    .catch(() => null);
  // Offline fallback: search ALL caches (the pages live in PRECACHE), then index as last resort.
  return cached || (await network) || (await caches.match(request)) || caches.match("/index.html");
}

async function cacheFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  if (cached) return cached;
  const response = await fetch(request);
  if (response && (response.ok || response.type === "opaque")) {
    cache.put(request, response.clone());
  }
  return response;
}

async function tileCache(request) {
  const cache = await caches.open(TILES);
  const cached = await cache.match(request);
  const network = fetch(request)
    .then((response) => {
      if (response && (response.ok || response.type === "opaque")) {
        cache.put(request, response.clone()).then(() => trimCache(TILES, TILE_MAX_ENTRIES));
      }
      return response;
    })
    .catch(() => null);
  return cached || (await network);
}

async function trimCache(cacheName, maxEntries) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();
  // Evict oldest-inserted entries (keys() preserves insertion order).
  for (let i = 0; i < keys.length - maxEntries; i++) {
    await cache.delete(keys[i]);
  }
}

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  const url = new URL(request.url);

  // App pages: stale-while-revalidate, offline-fallback to cached index.
  if (request.mode === "navigate") {
    event.respondWith(staleWhileRevalidate(request, RUNTIME));
    return;
  }
  if (isTile(url)) {
    event.respondWith(tileCache(request));
    return;
  }
  if (isFont(url)) {
    event.respondWith(cacheFirst(request, RUNTIME));
    return;
  }
  // Same-origin assets + Leaflet: cache-first (they're versioned/static).
  if (url.origin === self.location.origin || url.hostname === "unpkg.com") {
    event.respondWith(cacheFirst(request, PRECACHE));
    return;
  }
  // Everything else (external links, APIs): straight to network, no caching.
});
