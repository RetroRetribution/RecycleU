// Hardcoded demo drop points (stable IDs that match /drop-point/<id>)
const DROP_POINTS = [
  { id: 1, name: "Millennium City Mall", lat: 48.2108, lng: 16.3725, address: "Central Vienna", hours: "09:00–18:00" },
  { id: 2, name: "Central Station",      lat: 48.1850, lng: 16.3747, address: "Hbf Area",      hours: "10:00–16:00" },
  { id: 3, name: "Riverside Park",       lat: 48.2167, lng: 16.3950, address: "Danube Side",   hours: "Always open" }
];

function haversineKm(a, b) {
  const R = 6371;
  const toRad = d => (d * Math.PI) / 180;
  const dLat = toRad(b.lat - a.lat);
  const dLng = toRad(b.lng - a.lng);
  const lat1 = toRad(a.lat);
  const lat2 = toRad(b.lat);

  const x =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLng / 2) ** 2;

  return 2 * R * Math.asin(Math.sqrt(x));
}

function setNearestUI(point, distKm) {
  const nameEl = document.getElementById("nearestName");
  const metaEl = document.getElementById("nearestMeta");
  const btnEl = document.getElementById("nearestBtn");

  if (nameEl) nameEl.textContent = point.name;
  if (metaEl) metaEl.textContent = `${point.address} • ${point.hours} • ~${distKm.toFixed(1)} km away`;
  if (btnEl) btnEl.href = `/drop-point/${point.id}`;
}

document.addEventListener("DOMContentLoaded", () => {
  // Center on Vienna-ish by default
  const map = L.map("map").setView([48.2082, 16.3738], 13);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap'
  }).addTo(map);

  // Add markers
  DROP_POINTS.forEach(p => {
    const m = L.marker([p.lat, p.lng]).addTo(map);
    m.bindPopup(`<b>${p.name}</b><br>${p.address}<br><a href="/drop-point/${p.id}">Open drop point</a>`);
    m.on("click", () => {
      // clicking marker should take you to the drop point page
      window.location.href = `/drop-point/${p.id}`;
    });
  });

  // Find nearest using geolocation
  if (!navigator.geolocation) {
    document.getElementById("nearestName").textContent = "Geolocation not available";
    setNearestUI(DROP_POINTS[0], 0);
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const user = { lat: pos.coords.latitude, lng: pos.coords.longitude };
      let best = DROP_POINTS[0];
      let bestD = haversineKm(user, best);

      for (const p of DROP_POINTS) {
        const d = haversineKm(user, p);
        if (d < bestD) {
          best = p;
          bestD = d;
        }
      }

      // show user pin + nearest info
      L.circleMarker([user.lat, user.lng], { radius: 7 }).addTo(map).bindPopup("You are here");
      map.setView([user.lat, user.lng], 13);

      setNearestUI(best, bestD);
    },
    (err) => {
      console.warn("Geolocation failed:", err);
      document.getElementById("nearestName").textContent = "Location permission denied";
      setNearestUI(DROP_POINTS[0], 0);
    },
    { enableHighAccuracy: true, timeout: 8000 }
  );
});
