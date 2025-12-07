const API_BASE = 'http://127.0.0.1:5000';


document.addEventListener('DOMContentLoaded', () => {
    fetchProfileData();
});

function fetchProfileData() {
    const profileContent = document.getElementById('profile-content');
    if (!profileContent) return;

    profileContent.innerHTML = '<p>Loading profile...</p>';

    fetch(`${API_BASE}/api/profile`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            displayProfileData(data, profileContent);
        })
        .catch(error => {
            profileContent.innerHTML = `<p style="color: red;">Error fetching profile: ${error.message}</p>`;
            console.error('Fetch error:', error);
        });
}

function displayProfileData(data, container) {
    let html = `
        <div class="profile-box">
            <h3>User Profile</h3>
            <p><strong>Name:</strong> ${data.name}</p>
            <p><strong>Email:</strong> ${data.email}</p>
            <p><strong>Joined:</strong> ${data.joined}</p>
            <p><strong>Total Points:</strong> ${data.total_points}</p>
            
            <h4>Badges:</h4>
            <ul>
                ${data.badges.map(badge => `
                    <li>${badge.name} (Earned: ${badge.earned})</li>
                `).join('')}
            </ul>
        </div>
    `;
    container.innerHTML = html;
}

function handleLogin() {
    const emailInput = document.getElementById('email-input');
    const passwordInput = document.getElementById('password-input');

    if (!emailInput.value || !passwordInput.value) {
        alert('Please enter email and password');
        return;
    }


    alert(`Login successful as ${emailInput.value}`);
    console.log('Login attempt with:', emailInput.value);
}


function fetchIndexData() {
    fetch(`${API_BASE}/api/status`)
        .then(response => response.json())
        .then(data => {
            console.log('API Status:', data);
        })
        .catch(error => console.error('Error fetching status:', error));
}

function registerUser() {
    const nameInput = document.getElementById('name-input');
    const emailInput = document.getElementById('email-input');
    const passwordInput = document.getElementById('password-input');

    if (!nameInput || !emailInput || !passwordInput) {
        alert('Missing form elements');
        return;
    }

    const payload = {
        name: nameInput.value.trim(),
        email: emailInput.value.trim(),
        password: passwordInput.value
    };

    if (!payload.name || !payload.email || !payload.password) {
        alert('Please fill name, email and password to register');
        return;
    }

    fetch(`${API_BASE}/api/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(async res => {
        const body = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(body.error || `Status ${res.status}`);
        return body;
    })
    .then(data => {
        alert('Registration successful!');
        // Optionally refresh profile area
        fetchProfileData();
    })
    .catch(err => {
        console.error('Register error', err);
        alert('Registration failed: ' + err.message);
    });
}
