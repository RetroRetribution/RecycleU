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
    if (level) {
        level.textContent = levelMap[stage] || 1;
    }

    currentPercent = clamped;
    currentStage = stage;
}

function setStage(stage) {
    const ring = document.getElementById("ring");
    if (ring) {
        ring.setAttribute("data-stage", stage);
    }
}

function addVisualPoints(amount) {
    let newPercent = currentPercent + amount;
    let newStage = currentStage;

    if (newPercent >= 90) newStage = "tree";
    else if (newPercent >= 40) newStage = "sapling";
    else newStage = "sprout";

    updatePoint(newPercent, newStage);
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('show');
    }, 10);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

document.addEventListener("DOMContentLoaded", () => {

    const ring = document.getElementById("ring");
    if (ring) {
        ring.style.setProperty("--progress", "0deg");
        setTimeout(() => {
            updatePoint(currentPercent, currentStage);
        }, 100);
    }

    // (Moved from HTML)
    document.querySelectorAll('.point-controls button').forEach(btn => {
        btn.addEventListener('click', async function() {
            const points = parseInt(this.getAttribute('data-points'));
            const btnId = this.id;

            const stageMap = {
                'sproutBtn': { stage: 'sprout', percent: 25 },
                'saplingBtn': { stage: 'sapling', percent: 55 },
                'treeBtn': { stage: 'tree', percent: 95 },
                'addBtn': null 
            };

            try {
                const response = await fetch('/donate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ points: points })
                });

                const result = await response.json();

                if (result.success) {
                    if (stageMap[btnId]) {
                        updatePoint(stageMap[btnId].percent, stageMap[btnId].stage);
                    } else {
                        addVisualPoints(points);
                    }
                    
                    showToast(`Donated ${points} points!`, 'success');
                } else {
                    showToast('Error: ' + result.error, 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showToast('Network error occurred', 'error');
            }
        });
    });
});