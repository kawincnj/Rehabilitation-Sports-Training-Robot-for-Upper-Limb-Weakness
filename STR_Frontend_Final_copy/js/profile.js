// load profile data
window.onload = function() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (!isLoggedIn || isLoggedIn !== 'true') {
        window.location.href = 'login.html';
        return;
    }
    
    // show username
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
        document.getElementById('displayName').textContent = currentUser;
    }
}