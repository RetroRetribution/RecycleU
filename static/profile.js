document.addEventListener("DOMContentLoaded", async () => {
    const el = document.getElementById("profilePoints");
    if (!el) return;
  
    try {
      const res = await fetch("/api/points");
      const data = await res.json();
      document.getElementById("profilePoints").textContent = data.total;
      console.log(data.total);
    } catch (e) {
      console.error("Failed to load points:", e);
    }
  });
  
