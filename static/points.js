let currentPercent = 55;
let currentStage = "sapling";

function updatePoint(percent, stage) {
    const ring = document.getElementById("ring");
    const level = document.getElementById("level");

    const clamped = Math.max(0, Math.min(100, percent));
    const deg = (clamped / 100) * 360;

    ring.style.setProperty("--progress", deg + "deg");
    setStage(stage);

    const levelMap = { sprout: 1, sapling: 2, tree: 3 };
    level.textContent = levelMap[stage] || 1;

    currentPercent = clamped;
    currentStage = stage;
}

function setStage(stage) {
    const ring = document.getElementById("ring");
    ring.setAttribute("data-stage", stage);
}

function addPoints(amount) {
    let newPercent = currentPercent + amount;
    let newStage = currentStage;

    if (newPercent >= 75) newStage = "tree";
    else if (newPercent >= 40) newStage = "sapling";
    else newStage = "sprout";

    updatePoint(newPercent, newStage);
}

document.addEventListener("DOMContentLoaded", () => {
    const ring = document.getElementById("ring");
    ring.style.setProperty("--progress", "0deg");
    setTimeout(() => {
        updatePoint(currentPercent, currentStage);
    }, 100);
});

document.addEventListener("DOMContentLoaded", () => {
    const ring = document.getElementById("ring");
    ring.style.setProperty("--progress", "0deg");
    setTimeout(() => {
        updatePoint(currentPercent, currentStage);
    }, 100);

    // Button bindings
    document.getElementById("sproutBtn").addEventListener("click", () => {
        updatePoint(10, "sprout");
    });

    document.getElementById("saplingBtn").addEventListener("click", () => {
        updatePoint(50, "sapling");
    });

    document.getElementById("treeBtn").addEventListener("click", () => {
        updatePoint(90, "tree");
    });

    document.getElementById("addBtn").addEventListener("click", () => {
        addPoints(10);
    });
});
