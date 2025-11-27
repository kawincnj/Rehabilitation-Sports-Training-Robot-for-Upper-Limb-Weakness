/* ================================================================
   Global Variables & Configuration
================================================================
*/
let stream = null; // Webcam stream
let socket = null; // WebSocket connection
let isProcessing = false; // Flag to control the loop
const FPS = 30; // Limit frames sent to Python to save bandwidth

/* ================================================================
   1. Initialization & Authentication
================================================================
*/
window.onload = function () {
  // Check login status
  const isLoggedIn = localStorage.getItem("isLoggedIn");
  if (!isLoggedIn || isLoggedIn !== "true") {
    window.location.href = "login.html";
    return;
  }

  // Load selected activity
  const selectedActivity = localStorage.getItem("selectedActivity");
  let gameMode = "ball"; // Default mode

  if (selectedActivity) {
    const activity = JSON.parse(selectedActivity);
    console.log("Starting training:", activity.activity_name);

    // Map the activity title to Python game_mode keys if necessary
    // Example: If title is "Football Training", send "football"
    if (activity.activity_name.toLowerCase().includes("football"))
      gameMode = "football";
    else if (activity.activity_name.toLowerCase().includes("badminton"))
      gameMode = "badminton";
    else if (activity.activity_name.toLowerCase().includes("pingpong"))
      gameMode = "pingpong";
    else gameMode = "ball";
  }

  // Initialize the system
  initializeTraining(gameMode);
};

/* ================================================================
   2. Core Logic: Webcam & WebSocket
================================================================
*/
async function initializeTraining(gameMode) {
  console.log("Training initialized - Starting Webcam...");
  const videoElement = document.getElementById("webcamFeed");

  // Check browser support
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    try {
      // Request camera access
      // Note: We use 640x480 to ensure fast transmission over WebSocket
      stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: 640,
          height: 480,
          facingMode: "user",
        },
        audio: false,
      });

      // Assign stream to hidden video element
      videoElement.srcObject = stream;

      // Wait for video to load metadata before connecting socket
      videoElement.onloadedmetadata = () => {
        console.log("Webcam started successfully");
        connectWebSocket(gameMode);
      };
    } catch (error) {
      console.error("Error accessing webcam:", error);
      alert(
        "Unable to access camera. Please ensure you have granted permission."
      );
    }
  } else {
    console.error("getUserMedia is not supported in this browser");
  }
}

function connectWebSocket(gameMode) {
  // Connect to FastAPI WebSocket
  const url = `ws://localhost:8000/ws/${gameMode}`;
  console.log(`Connecting to: ${url}`);

  socket = new WebSocket(url);

  socket.onopen = () => {
    console.log("Connected to Python Game Server");
    isProcessing = true;
    processVideoFrames(); // Start the loop
  };

  socket.onmessage = (event) => {
    // Receive data from Python
    const data = JSON.parse(event.data);

    // 1. Update the displayed image (Process Feed)
    const processedImg = document.getElementById("processedFeed");
    if (processedImg) {
      processedImg.src = data.image;
    }

    // 2. Update Score
    const scoreBoard = document.getElementById("scoreBoard");
    if (scoreBoard) {
      scoreBoard.innerText = `Score: ${data.score}`;
      // Save current score to dataset for when we finish
      scoreBoard.dataset.currentScore = data.score;
    }
  };

  socket.onclose = () => {
    console.log("Disconnected from server");
    isProcessing = false;
  };

  socket.onerror = (error) => {
    console.error("WebSocket Error:", error);
  };
}

/* ================================================================
   3. Frame Processing Loop
================================================================
*/
function processVideoFrames() {
  if (!isProcessing) return;

  const video = document.getElementById("webcamFeed");
  const canvas = document.getElementById("inputCanvas");
  const ctx = canvas.getContext("2d");

  // Ensure video is ready
  if (video.videoWidth > 0 && video.videoHeight > 0) {
    // Match canvas size to video size
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw video frame to canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert to Base64 (JPEG quality 0.7 for speed/compression)
    const frameData = canvas.toDataURL("image/jpeg", 0.7);

    // Send to Python if socket is open
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(frameData);
    }
  }

  // Throttle the loop to specific FPS
  setTimeout(() => {
    requestAnimationFrame(processVideoFrames);
  }, 1000 / FPS);
}

/* ================================================================
   4. Navigation & User Actions
================================================================
*/

// Function to go back to training page
function goBack() {
  cleanup();
  window.location.href = "training.html";
}

// Function to finish training and go to results
function finishTraining() {
  // Get the final score from the scoreboard
  const scoreBoard = document.getElementById("scoreBoard");
  const finalScore = scoreBoard
    ? parseInt(scoreBoard.dataset.currentScore || "0")
    : 0;

  // Save training results to localStorage
  const trainingData = {
    score: finalScore,
    timestamp: new Date().toISOString(),
    // You can add other metrics here if your Python backend sends them
  };

  localStorage.setItem("lastTrainingResult", JSON.stringify(trainingData));

  // Clean up and Navigate
  cleanup();
  window.location.href = "session-complete.html";
}

/* ================================================================
   5. Cleanup
================================================================
*/
function cleanup() {
  isProcessing = false;

  // Close WebSocket
  if (socket) {
    socket.close();
    socket = null;
  }

  // Stop Webcam
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
    stream = null;
    console.log("Webcam stopped");
  }
}

// Trigger cleanup on page unload (refresh/close tab)
window.addEventListener("beforeunload", cleanup);
