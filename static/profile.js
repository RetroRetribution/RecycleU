document.addEventListener("DOMContentLoaded", async () => {
    const el = document.getElementById("profilePoints");
    if (!el) return;
  
    try {
      const res = await fetch("/api/points");
      const data = await res.json();
      el.textContent = String(data.total ?? 0);
    } catch (e) {
      console.error("Failed to load points:", e);
    }
  });
  