import time
import math

class HandMotionDetector:
    def __init__(self, smoothing=0.2, xy_threshold=50, z_threshold=40):
        """
        Initializes the motion detector.
        :param smoothing: 0.0 to 1.0. Lower = smoother movement.
        :param xy_threshold: Speed threshold for X/Y gestures.
        :param z_threshold: Speed threshold for Z (Push/Pull) gestures.
        """
        self.smoothing = smoothing
        self.xy_thresh = xy_threshold
        self.z_thresh = z_threshold
        
        # State variables
        self.prev_time = 0
        self.prev_pos = None # [x, y, z]
        self.curr_velocity = [0, 0, 0] # [vx, vy, vz]

    def _get_distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def process(self, hand_landmarks, frame_width, frame_height):
        """
        Calculates velocity and detects gestures.
        :param hand_landmarks: MediaPipe hand landmarks object.
        :param frame_width: Width of the camera frame.
        :param frame_height: Height of the camera frame.
        :return: Dictionary containing velocities, text states, and active colors.
        """
        current_time = time.time()
        
        # 1. Get Coordinates
        # Point 0 (Wrist)
        wrist = [
            int(hand_landmarks.landmark[0].x * frame_width),
            int(hand_landmarks.landmark[0].y * frame_height)
        ]
        # Point 9 (Middle Finger MCP/Knuckle)
        middle_mcp = [
            int(hand_landmarks.landmark[9].x * frame_width),
            int(hand_landmarks.landmark[9].y * frame_height)
        ]

        # Calculate Z-Proxy (Depth based on hand size)
        # We multiply by 2 to increase sensitivity
        curr_z = self._get_distance(wrist, middle_mcp) * 2
        
        curr_pos_temp = [wrist[0], wrist[1], curr_z]

        # 2. Handle First Frame or Re-entry
        # If the hand was lost or this is the first run, reset state to prevent velocity spikes
        if self.prev_pos is None or (current_time - self.prev_time) > 1.0:
            self.prev_pos = curr_pos_temp
            self.prev_time = current_time
            self.curr_velocity = [0, 0, 0]
            return {
                "velocity": [0,0,0],
                "states": ["---", "---", "---"],
                "colors": [(200,200,200), (200,200,200), (200,200,200)],
                "wrist_coor": wrist
            }

        # 3. Calculate Time Delta
        dt = current_time - self.prev_time
        if dt == 0: dt = 0.001

        # 4. Calculate Raw Velocity
        raw_vx = (curr_pos_temp[0] - self.prev_pos[0]) / dt
        raw_vy = (curr_pos_temp[1] - self.prev_pos[1]) / dt
        raw_vz = (curr_pos_temp[2] - self.prev_pos[2]) / dt

        # 5. Apply Smoothing
        self.curr_velocity[0] = (self.smoothing * raw_vx) + ((1 - self.smoothing) * self.curr_velocity[0])
        self.curr_velocity[1] = (self.smoothing * raw_vy) + ((1 - self.smoothing) * self.curr_velocity[1])
        self.curr_velocity[2] = (self.smoothing * raw_vz) + ((1 - self.smoothing) * self.curr_velocity[2])

        # 6. Determine States (Logic)
        x_text, y_text, z_text = "---", "---", "---"
        c_x, c_y, c_z = (200,200,200), (200,200,200), (200,200,200)

        # X-Axis
        if self.curr_velocity[0] > self.xy_thresh:
            x_text, c_x = "RIGHT >>", (0, 255, 0)
        elif self.curr_velocity[0] < -self.xy_thresh:
            x_text, c_x = "<< LEFT", (0, 255, 0)

        # Y-Axis
        if self.curr_velocity[1] > self.xy_thresh:
            y_text, c_y = "DOWN v", (0, 0, 255)
        elif self.curr_velocity[1] < -self.xy_thresh:
            y_text, c_y = "UP ^", (0, 0, 255)

        # Z-Axis
        if self.curr_velocity[2] > self.z_thresh:
            z_text, c_z = "PUSHING", (255, 0, 255)
        elif self.curr_velocity[2] < -self.z_thresh:
            z_text, c_z = "PULLING", (255, 0, 255)

        # 7. Update History
        self.prev_pos = curr_pos_temp
        self.prev_time = current_time

        return {
            "velocity": self.curr_velocity,
            "states": [x_text, y_text, z_text], # Text for X, Y, Z
            "colors": [c_x, c_y, c_z],          # Colors for X, Y, Z
            "wrist_coor": wrist                 # Useful for drawing circles
        }

    def reset(self):
        """Manually reset the state (e.g., if hand leaves frame)"""
        self.prev_pos = None
        self.curr_velocity = [0, 0, 0]