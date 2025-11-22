function startTraining() {
            // Mark device as connected
            localStorage.setItem('deviceConnected', 'true');
            
            // Go to training page
            window.location.href = 'training.html';
        }