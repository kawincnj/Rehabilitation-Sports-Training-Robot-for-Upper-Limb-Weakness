// show role in title
window.onload = function() {
    const selectedRole = localStorage.getItem('selectedRole') || 'patient';
    document.getElementById('loginTitle').textContent = 
        selectedRole.charAt(0).toUpperCase() + selectedRole.slice(1);
}

function handleLogin() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // check empty fields
    if (!username || !password) {
        alert('Please fill in Username and Password');
        return;
    }
    
    // check password (for demo purpose, password is '1234')
    if (password === '1234') {
        // บันทึกข้อมูล user ใน localStorage
        localStorage.setItem('currentUser', username);
        localStorage.setItem('isLoggedIn', 'true');
        
        // go to home page
        window.location.href = 'home.html';
    } else {
        alert('Wrong password');
    }
}