document.addEventListener("DOMContentLoaded", () => {
  const ringEl = document.getElementById("ring");
  const levelEl = document.getElementById("level");

  const locationId = Number(document.body.dataset.locationId);

  if (!Number.isInteger(locationId) || locationId <= 0) {
    console.error("Invalid/missing data-location-id on <body>:", document.body.dataset.locationId);
  }

  const storageKey = `drop_loc_points_${locationId}`;

  function getLocPoints() {
    const v = Number(localStorage.getItem(storageKey) || 0);
    return Number.isFinite(v) ? v : 0;
  }

  function setLocPoints(v) {
    localStorage.setItem(storageKey, String(v));
  }

  async function addWalletPoints(delta, reason = "drop_point") {
    const res = await fetch("/api/points/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location_id: locationId, delta, reason })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to add points");
    return data; // { user_id, total }
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
    // 0-49 sprout, 50-149 sapling, 150+ tree
    if (locPoints >= 150) return { stage: "tree", level: 3 };
    if (locPoints >= 50) return { stage: "sapling", level: 2 };
    return { stage: "sprout", level: 1 };
  }

  function setRingProgress(locPoints) {
    // 0..150 -> 0..360deg (cap)
    const capped = Math.max(0, Math.min(150, locPoints));
    const deg = Math.round((capped / 150) * 360);
    ringEl?.style.setProperty("--progress", `${deg}deg`);
  }

  function updateUI() {
    const locPoints = getLocPoints();
    const { stage, level } = computeStageAndLevel(locPoints);

    if (ringEl) ringEl.dataset.stage = stage;
    if (levelEl) levelEl.textContent = String(level);

    setRingProgress(locPoints);
  }

  async function handleAdd(delta, label) {
    try {
      // 1) Update Mongo wallet total (global points)
      await addWalletPoints(delta, "drop_point");

      // 2) Update local growth points (per drop point)
      const newLocPoints = getLocPoints() + delta;
      setLocPoints(newLocPoints);

      updateUI();
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
