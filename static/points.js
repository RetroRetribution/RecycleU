document.addEventListener("DOMContentLoaded", () => {
    // The container where point info will go
    const summaryBox = document.getElementById("points-summary");
    if (!summaryBox) {
        console.error("points-summary element not found.");
        return;
    }

    summaryBox.innerHTML = "<p>Loading point data...</p>";

    // Fetch the point data from Flask backend
    fetch("/api/points")
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            // Validate structure
            if (!data || typeof data.total === "undefined") {
                throw new Error("Invalid data structure returned from API");
            }

            const total = data.total;
            const earned = data.earned;
            const spent = data.spent;
            const history = data.history || [];

            // Determine progress stage
            const percent = Math.min(100, (total / 2000) * 100);
            let stage = "sprout";
            if (percent >= 80) stage = "tree";
            else if (percent >= 40) stage = "sapling";

            // Call the existing function in point.html
            if (typeof updatePoint === "function") {
                updatePoint(percent, stage);
            }

            // Build history list
            const historyHTML = history
                .map(
                    (entry) => `
                <li>
                    <strong>${entry.date}</strong> — 
                    <span style="color:${entry.change > 0 ? "green" : "red"};">
                        ${entry.change > 0 ? "+" : ""}${entry.change}
                    </span>
                    <em> (${entry.source})</em>
                </li>
            `
                )
                .join("");

            // Render into page
            summaryBox.innerHTML = `
                <h3>Your Points</h3>
                <p><strong>Total:</strong> ${total}</p>
                <p><strong>Earned:</strong> ${earned}</p>
                <p><strong>Spent:</strong> ${spent}</p>

                <h3>History</h3>
                <ul>${historyHTML}</ul>
            `;
        })
        .catch((err) => {
            console.error("Error loading point data:", err);
            summaryBox.innerHTML = `
                <p style="color:red;">
                    Unable to load point data.  
                    (${err.message})
                </p>
            `;
        });
});
