document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("qrFile");
    const result = document.getElementById("scanResult");
  
    function setStatus(msg, isError = false) {
      result.textContent = msg;
      result.style.color = isError ? "#b00020" : "#1b5e20";
      result.style.opacity = "1";
    }
  
    fileInput.addEventListener("change", () => {
      const file = fileInput.files?.[0];
      if (!file) return;
  
      setStatus("Processing image…");
  
      // Simulated scan delay
      setTimeout(() => {
        const fakeCode = "RECYCLEU-QR-50PTS";
        setStatus(`QR detected ✔  +50 points`);
  
        // Optional future flow:
        // window.location.href = `/points?code=${fakeCode}`;
      }, 700);
    });
  
    setStatus("Upload a QR image to scan.");
  });
  