document.addEventListener("DOMContentLoaded", () => {
  const ringEl = document.getElementById("ring");
  const levelEl = document.getElementById("level");

  const locationId = Number(document.body.dataset.locationId);

  if (!Number.isInteger(locationId) || locationId <= 0) {
    console.error("Invalid/missing data-location-id on <body>");
  }

  async function getLocationTotal() {
    try {
      const res = await fetch(`/api/points/location/${locationId}`);
      if (!res.ok) return 0;
      const data = await res.json();
      return data.total || 0;
    } catch (e) {
      console.error("Error fetching location stats:", e);
      return 0;
    }
  }

  async function addWalletPoints(points, reason = "drop_point") {
    const res = await fetch("/api/points/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location_id: locationId, points, reason })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to add points");
    return data; 
  }

  function toast(msg) {
    const c = document.getElementById("toast-container");
    if (!c) return;
    const t = document.createElement("div");
    t.className = "toast";
    t.textContent = msg;
    c.appendChild(t);
    setTimeout(() => t.classList.add("show"), 10);
    setTimeout(() => {
      t.classList.remove("show");
      setTimeout(() => t.remove(), 200);
    }, 2000);
  }

  function computeStageAndLevel(locPoints) {
    if (locPoints >= 150) return { stage: "tree", level: 3 };
    if (locPoints >= 50) return { stage: "sapling", level: 2 };
    return { stage: "sprout", level: 1 };
  }

  function setRingProgress(locPoints) {
    const capped = Math.max(0, Math.min(150, locPoints));
    const deg = Math.round((capped / 150) * 360);
    if (ringEl) ringEl.style.setProperty("--progress", `${deg}deg`);
  }

  async function updateUI() {
    const locPoints = await getLocationTotal();
    
    const { stage, level } = computeStageAndLevel(locPoints);

    if (ringEl) ringEl.dataset.stage = stage;
    if (levelEl) levelEl.textContent = String(level);

    setRingProgress(locPoints);
  }

  async function handleAdd(delta, label) {
    try {
      await addWalletPoints(delta, "drop_point");

      await updateUI();

      toast(`+${delta} points (${label})`);
    } catch (e) {
      console.error(e);
      toast("Could not add points.");
    }
  }

  document.getElementById("sproutBtn")?.addEventListener("click", () => handleAdd(10, "Sprout"));
  document.getElementById("saplingBtn")?.addEventListener("click", () => handleAdd(20, "Sapling"));
  document.getElementById("treeBtn")?.addEventListener("click", () => handleAdd(30, "Tree"));
  document.getElementById("addBtn")?.addEventListener("click", () => handleAdd(10, "+10"));

  updateUI();
});