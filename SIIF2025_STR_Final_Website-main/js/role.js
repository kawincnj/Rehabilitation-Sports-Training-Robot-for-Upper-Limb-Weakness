let selectedRole = 'patient';

function selectRole(role) {
    selectedRole = role;
    document.querySelectorAll('.role-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    document.getElementById(role + 'Btn').classList.add('selected');
    
    // save data in localStorage
    localStorage.setItem('selectedRole', role);
}

function goToLogin() {
    // check role selected
    if (!selectedRole) {
        alert('Please select Role');
        return;
    }
    
    window.location.href = 'login.html';
}

// check saved role on load
window.onload = function() {
    const savedRole = localStorage.getItem('selectedRole');
    if (savedRole) {
        selectRole(savedRole);
    }
}