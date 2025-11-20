// Training Activities Data
const activities = [
    {
        id: 1,
        title: "Ball Gripping",
        difficulty: "beginner",
        imagePath: "png/ball.png"
    },
    {
        id: 2,
        title: "Badminton",
        difficulty: "easy",
        imagePath: "png/badminton.png"
    },
    {
        id: 3,
        title: "Table Tennis",
        difficulty: "medium",
        imagePath: "png/table_tennis.png"
    },
    {
        id: 4,
        title: "Soccer",
        difficulty: "medium",
        imagePath: "png/soccer.png"
    }
];

let currentPage = 0;
const cardsPerPage = 3;

// Check login and device connection status
window.onload = function() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    const isConnected = localStorage.getItem('deviceConnected');
    
    if (!isLoggedIn || isLoggedIn !== 'true') {
        window.location.href = 'login.html';
        return;
    }
    
    // Mark device as connected when reaching training page
    if (!isConnected) {
        localStorage.setItem('deviceConnected', 'true');
    }
    
    renderActivities();
    updateNavigationButtons();
}

// Render activity cards
function renderActivities() {
    const slider = document.getElementById('activitiesSlider');
    slider.innerHTML = '';
    
    const startIndex = currentPage * cardsPerPage;
    const endIndex = Math.min(startIndex + cardsPerPage, activities.length);
    const visibleActivities = activities.slice(startIndex, endIndex);
    
    visibleActivities.forEach(activity => {
        const card = createActivityCard(activity);
        slider.appendChild(card);
    });
}

// Create activity card element
function createActivityCard(activity) {
    const card = document.createElement('div');
    card.className = 'activity-card';
    
    const difficultyClass = `difficulty-${activity.difficulty}`;
    
    card.innerHTML = `
        <div class="difficulty-badge ${difficultyClass}">${activity.difficulty}</div>
        <div class="activity-icon-area">
            <img src="${activity.imagePath}" alt="${activity.title}" class="activity-image">
        </div>
        <h3 class="activity-title">${activity.title}</h3>
        <button class="btn-start-activity" onclick="startActivity(${activity.id})">
            Start training
        </button>
    `;
    
    return card;
}

// Update navigation button states
function updateNavigationButtons() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    const totalPages = Math.ceil(activities.length / cardsPerPage);
    
    if (currentPage === 0) {
        prevBtn.classList.add('disabled');
    } else {
        prevBtn.classList.remove('disabled');
    }
    
    if (currentPage >= totalPages - 1) {
        nextBtn.classList.add('disabled');
    } else {
        nextBtn.classList.remove('disabled');
    }
}

// Navigate to previous page
function previousActivity() {
    if (currentPage > 0) {
        currentPage--;
        renderActivities();
        updateNavigationButtons();
    }
}

// Navigate to next page
function nextActivity() {
    const totalPages = Math.ceil(activities.length / cardsPerPage);
    if (currentPage < totalPages - 1) {
        currentPage++;
        renderActivities();
        updateNavigationButtons();
    }
}

// Start selected activity
function startActivity(activityId) {
    const activity = activities.find(a => a.id === activityId);
    
    if (activity) {
        // Save selected activity
        localStorage.setItem('selectedActivity', JSON.stringify(activity));
        
        // ไปหน้า session complete
        window.location.href = 'session-complete.html';
    }
}

// Handle window resize
let resizeTimer;
window.addEventListener('resize', function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {
        // Adjust cards per page based on screen width
        if (window.innerWidth < 968) {
            if (cardsPerPage !== 1) {
                currentPage = 0;
                renderActivities();
                updateNavigationButtons();
            }
        }
    }, 250);
});