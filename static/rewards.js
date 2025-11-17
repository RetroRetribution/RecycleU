document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('rewards-list');
    if (!container) return;

    container.innerHTML = '<p>Loading rewards...</p>';

    fetch('/api/rewards')
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            const rewards = data.rewards || [];

            if (rewards.length === 0) {
                container.innerHTML = '<p>No rewards available.</p>';
                return;
            }

            container.innerHTML = rewards.map(reward => `
                <div class="reward-item">
                    <div class="semi-reward-card">
                        <div class="price"><h2>${reward.cost} pts</h2></div>
                        <div class="item-name">${reward.name}</div>
                        <div class="stock">
                            ${reward.stock > 0 ? reward.stock + ' in stock' : 'Out of stock'}
                        </div>
                    </div>
                </div>
            `).join('');
        })
        .catch(error => {
            container.innerHTML = `<p style="color:red;">Error loading rewards: ${error.message}</p>`;
            console.error(error);
        });
});
