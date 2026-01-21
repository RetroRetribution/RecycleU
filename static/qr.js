document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("qrFile");
  const result = document.getElementById("scanResult");

  function setStatus(msg, isError = false) {
    result.textContent = msg;
    result.style.color = isError ? "#b00020" : "#1b5e20";
    result.style.opacity = "1";
  }

  async function addPoints(delta) {
    // Default location for QR uploads (can be improved later)
    const locationId = 1;

    const res = await fetch("/api/points/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        location_id: locationId,
        delta: delta,
        reason: "qr_upload"
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to add points");

    return data; // { user_id, total }
  }

  fileInput.addEventListener("change", async () => {
    const file = fileInput.files?.[0];
    if (!file) return;

    setStatus("Processing image…");

    try {
      // Simulated scan delay (keeps the UX nice)
      await new Promise(r => setTimeout(r, 450));

      const pointsAwarded = 50;
      const data = await addPoints(pointsAwarded);

      setStatus(`QR accepted ✔  +${pointsAwarded} points (Total: ${data.total})`);

      // allow uploading the same file again later
      fileInput.value = "";
    } catch (err) {
      console.error(err);
      setStatus("Could not award points. Try again.", true);
    }
  });

  setStatus("Upload a QR image to earn points.");
});
