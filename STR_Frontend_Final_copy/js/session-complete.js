let soundEnabled = false;

// Check login status
window.onload = function() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    
    if (!isLoggedIn || isLoggedIn !== 'true') {
        window.location.href = 'login.html';
        return;
    }
    
    // Load selected activity data if needed
    const selectedActivity = localStorage.getItem('selectedActivity');
    if (selectedActivity) {
        const activity = JSON.parse(selectedActivity);
        console.log('Completed activity:', activity.title);
    }
}

function toggleProfileMenu() {
    const dropdown = document.getElementById('profileDropdown');
    dropdown.classList.toggle('active');
}

function closeProfileMenu() {
    document.getElementById('profileDropdown').classList.remove('active');
}

function showSettingModal() {
    closeProfileMenu();
    document.getElementById('modalOverlay').classList.add('active');
    document.getElementById('settingModal').classList.add('active');
}

function closeSettingModal() {
    document.getElementById('modalOverlay').classList.remove('active');
    document.getElementById('settingModal').classList.remove('active');
}

function toggleSound() {
    soundEnabled = !soundEnabled;
    const toggle = document.getElementById('soundToggle');
    if (soundEnabled) {
        toggle.classList.add('active');
    } else {
        toggle.classList.remove('active');
    }
}

function logout() {
    closeSettingModal();
    
    // delete data session
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('currentUser');
    localStorage.removeItem('deviceConnected');
    localStorage.removeItem('selectedActivity');
    
    // back to landing page
    window.location.href = 'index.html';
}

// close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('profileDropdown');
    const profileBtn = document.getElementById('profileMenuBtn');
    
    if (dropdown && profileBtn) {
        if (!dropdown.contains(event.target) && !profileBtn.contains(event.target)) {
            closeProfileMenu();
        }
    }
});