let soundEnabled = false;

// Training Activities Data
const activities = [
  {
    id: 1,
    title: "Ball Gripping",
    difficulty: "beginner",
    imagePath: "png/ball.png",
    activitiy_name: "ball",
  },
  {
    id: 2,
    title: "Badminton",
    difficulty: "easy",
    imagePath: "png/badminton.png",
    activitiy_name: "badminton",
  },
  {
    id: 3,
    title: "Table Tennis",
    difficulty: "medium",
    imagePath: "png/table_tennis.png",
    activitiy_name: "pingpong",
  },
  {
    id: 4,
    title: "Soccer",
    difficulty: "medium",
    imagePath: "png/soccer.png",
    activitiy_name: "football",
  },
];

let currentPage = 0;
let cardsPerPage = 3;

// Check login and device connection status
window.onload = function () {
  const isLoggedIn = localStorage.getItem("isLoggedIn");
  const isConnected = localStorage.getItem("deviceConnected");

  if (!isLoggedIn || isLoggedIn !== "true") {
    window.location.href = "login.html";
    return;
  }

  // Mark device as connected when reaching training page
  if (!isConnected) {
    localStorage.setItem("deviceConnected", "true");
  }

  // Set cards per page based on screen size
  updateCardsPerPage();
  renderActivities();
  updateNavigationButtons();
};

// Function to go back to previous page
function goBack() {
  // Check if there's a referrer and it's from the same site
  if (
    document.referrer &&
    document.referrer.indexOf(window.location.host) !== -1
  ) {
    window.history.back();
  } else {
    // Default to home if no referrer
    window.location.href = "home.html";
  }
}

// Update cards per page based on screen width
function updateCardsPerPage() {
  const width = window.innerWidth;

  // iPad / Tablet: 769px - 1024px → 2 การ์ด
  if (width >= 820 && width <= 1180) {
    cardsPerPage = 2;
  }
  // Desktop: > 1024px → 3 การ์ด
  else if (width > 1180) {
    cardsPerPage = 3;
  }
  // Mobile: < 769px → 1 การ์ด
  else {
    cardsPerPage = 4;
  }
}

// Render activity cards
function renderActivities() {
  const slider = document.getElementById("activitiesSlider");
  slider.innerHTML = "";

  const startIndex = currentPage * cardsPerPage;
  const endIndex = Math.min(startIndex + cardsPerPage, activities.length);
  const visibleActivities = activities.slice(startIndex, endIndex);

  visibleActivities.forEach((activity) => {
    const card = createActivityCard(activity);
    slider.appendChild(card);
  });
}

// Create activity card element
function createActivityCard(activity) {
  const card = document.createElement("div");
  card.className = "activity-card";

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
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  const totalPages = Math.ceil(activities.length / cardsPerPage);

  if (currentPage === 0) {
    prevBtn.classList.add("disabled");
  } else {
    prevBtn.classList.remove("disabled");
  }

  if (currentPage >= totalPages - 1) {
    nextBtn.classList.add("disabled");
  } else {
    nextBtn.classList.remove("disabled");
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
  const activity = activities.find((a) => a.id === activityId);

  if (activity) {
    // Save selected activity
    localStorage.setItem("selectedActivity", JSON.stringify(activity));

    // ไปหน้า start-training (หน้าว่างสำหรับใส่ backend)
    window.location.href = "start-training.html";
  }
}

// Handle window resize
let resizeTimer;
window.addEventListener("resize", function () {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(function () {
    const oldCardsPerPage = cardsPerPage;
    updateCardsPerPage();

    // Reset to first page if cards per page changed
    if (oldCardsPerPage !== cardsPerPage) {
      currentPage = 0;
      renderActivities();
      updateNavigationButtons();
    }
  }, 250);
});

function toggleProfileMenu() {
  const dropdown = document.getElementById("profileDropdown");
  dropdown.classList.toggle("active");
}

function closeProfileMenu() {
  document.getElementById("profileDropdown").classList.remove("active");
}

function showSettingModal() {
  closeProfileMenu();
  document.getElementById("modalOverlay").classList.add("active");
  document.getElementById("settingModal").classList.add("active");
}

function closeSettingModal() {
  document.getElementById("modalOverlay").classList.remove("active");
  document.getElementById("settingModal").classList.remove("active");
}

function toggleSound() {
  soundEnabled = !soundEnabled;
  const toggle = document.getElementById("soundToggle");
  if (soundEnabled) {
    toggle.classList.add("active");
  } else {
    toggle.classList.remove("active");
  }
}

function logout() {
  closeSettingModal();

  // delete data session
  localStorage.removeItem("isLoggedIn");
  localStorage.removeItem("currentUser");
  localStorage.removeItem("deviceConnected"); // Also remove device connection status

  // back to landing page
  window.location.href = "index.html";
}
