let soundEnabled = false;

// login checking
window.onload = function() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (!isLoggedIn || isLoggedIn !== 'true') {
        // back to login
        window.location.href = 'login.html';
    }
    
    // รีเซ็ตประวัติเพจเมื่อกลับมาหน้า home
    localStorage.setItem('pageHistory', JSON.stringify(['home.html']));
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
    localStorage.removeItem('deviceConnected'); // Also remove device connection status
    
    // back to landing page
    window.location.href = 'index.html';
}

function startTraining() {
    // Check if device is already connected
    // const isConnected = localStorage.getItem('deviceConnected');
    
    // if (isConnected === 'true') {
    //     // Device already connected, go directly to training page
    //     window.location.href = 'training.html';
    // } 
    // else {
        // Device not connected, go to connecting page first
        window.location.href = 'connecting.html';
    
}


// Function for "Your session" button
function goToSession() {
    startTraining(); // Use the same logic as Start Training
}

// close dropdown
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('profileDropdown');
    const profileBtn = document.getElementById('profileMenuBtn');
    
    if (dropdown && profileBtn) {
        if (!dropdown.contains(event.target) && !profileBtn.contains(event.target)) {
            closeProfileMenu();
        }
    }
});