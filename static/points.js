document.addEventListener("DOMContentLoaded", () => {
    const ringEl = document.getElementById("ring");
    const levelEl = document.getElementById("level");
  
    const locationId = Number(document.body.dataset.locationId);
  
    if (!Number.isInteger(locationId) || locationId <= 0) {
      console.error("Invalid/missing data-location-id on <body>:", document.body.dataset.locationId);
    }
  
    async function getPoints() {
      const res = await fetch("/api/points");
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed to fetch points");
      return data;
    }
  
    async function addPoints(delta, reason = "drop_point") {
      const res = await fetch("/api/points/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ location_id: locationId, delta, reason })
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
  
    // --- Growth logic per location ---
    // Tune these thresholds however you like.
    function computeStageAndLevel(locPoints) {
      // Level by location points
      // 0-49 = sprout (level 1)
      // 50-149 = sapling (level 2)
      // 150+ = tree (level 3)
      if (locPoints >= 150) return { stage: "tree", level: 3 };
      if (locPoints >= 50) return { stage: "sapling", level: 2 };
      return { stage: "sprout", level: 1 };
    }
  
    function setRingProgress(locPoints) {
      // Map 0..150 points to 0..360 degrees (cap at 360)
      const capped = Math.max(0, Math.min(150, locPoints));
      const deg = Math.round((capped / 150) * 360);
      if (ringEl) ringEl.style.setProperty("--progress", `${deg}deg`);
    }
  
    function updateUI(userData) {
      const byLoc = userData.by_location || {};
      const locPoints = Number(byLoc[String(locationId)] || 0);
  
      const { stage, level } = computeStageAndLevel(locPoints);
  
      if (ringEl) ringEl.dataset.stage = stage;
      if (levelEl) levelEl.textContent = String(level);
  
      setRingProgress(locPoints);
    }
  
    async function init() {
      try {
        const user = await getPoints();
        updateUI(user);
      } catch (e) {
        console.error(e);
      }
    }
  
    async function handleAdd(delta, label) {
      try {
        const user = await addPoints(delta, "drop_point");
        updateUI(user);
        toast(`+${delta} points (${label})`);
      } catch (e) {
        console.error(e);
        toast("Could not add points.");
      }
    }
  
    // Buttons (your HTML already uses these IDs)
    document.getElementById("sproutBtn")?.addEventListener("click", () => handleAdd(10, "Sprout"));
    document.getElementById("saplingBtn")?.addEventListener("click", () => handleAdd(20, "Sapling"));
    document.getElementById("treeBtn")?.addEventListener("click", () => handleAdd(30, "Tree"));
    document.getElementById("addBtn")?.addEventListener("click", () => handleAdd(10, "+10"));
  
    init();
  });
  