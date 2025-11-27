import cv2 as cv
import mediapipe as mp
from tools import *
from games import *

class GameProcessor:
    def __init__(self, game_mode='pingpong', is_show_skeleton = False):
        self.score = 0
        self.on_catch_ball = False
        self.lock_bug_score = True
        self.lock_bug_score_squeez = False
        self.game_mode = game_mode
        self.is_show_skeleton = is_show_skeleton

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.05
        )
        self.mp_drawing = mp.solutions.drawing_utils

        self.football = cv.imread('SIIF2025_STR_Final_Website-main/backend/img/football.png', cv.IMREAD_UNCHANGED)
        self.badminton_rac = cv.imread('SIIF2025_STR_Final_Website-main/backend/img/badminton_rac.png', cv.IMREAD_UNCHANGED)
        self.shuttlecock = cv.imread('SIIF2025_STR_Final_Website-main/backend/img/shuttlecock.png', cv.IMREAD_UNCHANGED)
        self.ball_normal = cv.imread('SIIF2025_STR_Final_Website-main/backend/img/ball_normal.png', cv.IMREAD_UNCHANGED)
        self.ball_squeez = cv.imread('SIIF2025_STR_Final_Website-main/backend/img/ball_squeez.png', cv.IMREAD_UNCHANGED)
        self.pingpong_ball = cv.imread('SIIF2025_STR_Final_Website-main/backend/img/pingpong_ball.png', cv.IMREAD_UNCHANGED)
        self.pingpong_rac = cv.imread('SIIF2025_STR_Final_Website-main/backend/img/pingpong_rac.png', cv.IMREAD_UNCHANGED)

    def _get_finger_coor(self, finger, w, h, number):
        return [int(finger.landmark[number].x * w), int(finger.landmark[number].y * h)]

    def process_frame(self, frame):
        h, w, c = frame.shape
        frame = cv.flip(frame, 1)

        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        open_hand = "NO HAND"
        x_y_index = []
        hand_landmarks = {}
        
        if (results.multi_hand_landmarks):
            hand_landmarks = results.multi_hand_landmarks[0]
            
            x_y_index = self._get_finger_coor(hand_landmarks, w, h, 9)
            z_index = hand_landmarks.landmark[9].z
            x_y_pinkey = self._get_finger_coor(hand_landmarks, w, h, 20)
            
            close_hand = is_close_hand(hand_landmarks)
            open_hand = "Close" if close_hand else "Open"
            
            # --- GAME SECTION ---
            if x_y_index:
                match self.game_mode:
                    case "badminton":
                        frame, self.on_catch_ball, self.score = badminton(
                            frame, close_hand, self.badminton_rac, self.shuttlecock, x_y_index, x_y_pinkey,
                            w, self.on_catch_ball, self.score
                        )
                        
                    case 'football':
                        self.score, self.on_catch_ball, self.lock_bug_score, frame = catch_ball_game(
                            frame, close_hand, x_y_index, 
                            self.score, self.on_catch_ball, self.lock_bug_score, 
                            self.football, w, self._get_finger_coor(hand_landmarks, w, h, 12)
                        )
                    
                    case 'ball':
                        frame, self.score, self.lock_bug_score_squeez = squezz_ball(
                            frame, close_hand, self.ball_normal, self.ball_squeez, x_y_index, self.score,
                            self.lock_bug_score_squeez, 0.16
                        )
                    
                    case 'pingpong':
                        frame, self.score, self.on_catch_ball = pingpong(
                            frame, self.score, self.pingpong_rac, self.pingpong_ball,
                            self._get_finger_coor(hand_landmarks, w, h, 12), close_hand, abs(z_index),
                            self.on_catch_ball
                        )
                if (self.is_show_skeleton):
                    self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                    )
                        
        # --- Display Info ---
        text_color = [0,0,255][::-1]
        #cv.putText(frame, open_hand, (w - 170, 50), cv.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv.LINE_AA)
        #cv.putText(frame, f"Score: {self.score}", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv.LINE_AA)
        
        return frame, self.score, hand_landmarks