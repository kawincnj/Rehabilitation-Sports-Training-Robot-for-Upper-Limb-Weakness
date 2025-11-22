let selectedRole = 'patient';
let screenHistory = ['landing'];
let currentScreen = 'landing';
let soundEnabled = false;
let currentUsername = '';

function showScreen(screenName) {
    if (screenName !== currentScreen) {
        screenHistory.push(screenName);
        currentScreen = screenName;
    }

    const screens = document.querySelectorAll('.screen');
    screens.forEach(screen => screen.classList.remove('active'));
    document.getElementById(screenName).classList.add('active');

    if (screenName === 'login') {
        document.getElementById('loginTitle').textContent = 
            selectedRole.charAt(0).toUpperCase() + selectedRole.slice(1);
    }

    updateBackButton();
    closeProfileMenu();
    closeSettingModal();
}

function updateBackButton() {
    const backBtn = document.getElementById('backBtn');
    if (currentScreen === 'landing' || currentScreen === 'dashboard' || currentScreen === 'profile') {
        backBtn.classList.add('hidden');
    } else {
        backBtn.classList.remove('hidden');
    }
}

function goBack() {
    if (screenHistory.length > 1) {
        screenHistory.pop();
        const previousScreen = screenHistory[screenHistory.length - 1];
        currentScreen = previousScreen;
        
        const screens = document.querySelectorAll('.screen');
        screens.forEach(screen => screen.classList.remove('active'));
        document.getElementById(previousScreen).classList.add('active');
        
        updateBackButton();
    }
}

function selectRole(role) {
    selectedRole = role;
    document.querySelectorAll('.role-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    document.getElementById(role + 'Btn').classList.add('selected');
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
    document.getElementById('mainHeader').style.display = 'flex';
    document.getElementById('dashboardHeader').style.display = 'none';
    
    const screens = document.querySelectorAll('.screen');
    screens.forEach(screen => screen.classList.remove('active'));
    document.getElementById('landing').classList.add('active');
    
    screenHistory = ['landing'];
    currentScreen = 'landing';
    currentUsername = '';
    
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
}

document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('profileDropdown');
    const profileBtn = document.getElementById('profileMenuBtn');
    
    if (dropdown && profileBtn) {
        if (!dropdown.contains(event.target) && !profileBtn.contains(event.target)) {
            closeProfileMenu();
        }
    }   
});

selectRole('patient');