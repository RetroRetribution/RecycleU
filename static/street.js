// Leaflet map init
// Vienna center (adjust as you like)
const VIENNA_CENTER = [48.2082, 16.3738];

// Create map
const map = L.map("map", {
  zoomControl: true,
  scrollWheelZoom: true
}).setView(VIENNA_CENTER, 13);

// Add OpenStreetMap tiles (free)
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Demo drop points (replace/extend later, Mongo can feed these)
const dropPoints = [
  {
    id: 1,
    name: "Millennium City Mall",
    lat: 48.2432,
    lng: 16.3857,
    note: "Recycling station near entrance"
  },
  {
    id: 2,
    name: "Central Station",
    lat: 48.1850,
    lng: 16.3766,
    note: "Drop bins by the main exit"
  },
  {
    id: 3,
    name: "Riverside Park",
    lat: 48.2168,
    lng: 16.4016,
    note: "Glass + plastic collection"
  }
];

// Create markers
dropPoints.forEach((p) => {
  const marker = L.marker([p.lat, p.lng]).addTo(map);

  // Popup with a button-like link
  const popupHtml = `
    <div style="min-width:180px">
      <strong>${p.name}</strong><br/>
      <span style="opacity:0.85">${p.note}</span><br/><br/>
      <a href="/drop-point/${p.id}" style="text-decoration:none;font-weight:700;">
        Open drop point →
      </a>
    </div>
  `;

  marker.bindPopup(popupHtml);

  // Direct redirect on marker click (fast UX)
  marker.on("click", () => {
    window.location.href = `/drop-point/${p.id}`;
  });
});
