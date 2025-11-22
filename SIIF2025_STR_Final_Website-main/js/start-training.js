// Check login status
window.onload = function () {
  const isLoggedIn = localStorage.getItem("isLoggedIn");

  if (!isLoggedIn || isLoggedIn !== "true") {
    window.location.href = "login.html";
    return;
  }

  // Load selected activity
  const selectedActivity = localStorage.getItem("selectedActivity");
  if (selectedActivity) {
    const activity = JSON.parse(selectedActivity);
    console.log("Starting training:", activity.activitiy_name);
  }

  // Initialize your backend/game here
  initializeTraining();
};

// Function to go back to training page
function goBack() {
  window.location.href = "training.html";
}

// Function to finish training and go to results
function finishTraining() {
  // Save training results to localStorage if needed
  const trainingData = {
    averageSpeed: 2,
    handEyeSync: 35,
    score: 151,
    bestScore: 156,
    timestamp: new Date().toISOString(),
  };

  localStorage.setItem("lastTrainingResult", JSON.stringify(trainingData));

  // Navigate to session complete page
  window.location.href = "session-complete.html";
}

/*
===========================================
พื้นที่สำหรับโค้ด Backend / Game Logic
===========================================

เพิ่มฟังก์ชันและโค้ดของคุณตรงนี้:
*/

function initializeTraining() {
  // Initialize your backend, game, or visualization here
  console.log("Training initialized");

  // ตัวอย่าง:
  // - Setup canvas
  // - Initialize Three.js scene
  // - Connect to WebSocket
  // - Load game assets
  // - Start animation loop

  // Example: Auto finish after 5 seconds (for testing)
  // setTimeout(() => {
  //     finishTraining();
  // }, 5000);
}

// Example: Game Loop
let animationId;

function gameLoop() {
  // Update game state

  // Render

  // Continue loop
  animationId = requestAnimationFrame(gameLoop);
}

// Example: Stop game loop
function stopGameLoop() {
  if (animationId) {
    cancelAnimationFrame(animationId);
  }
}

// Cleanup on page unload
window.addEventListener("beforeunload", function () {
  stopGameLoop();
  // Cleanup other resources
});
