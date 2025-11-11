from tools import *

def catch_ball_game(frame, close_hand, x_y_index_knuckle, score, on_catch_ball, lock_bug_score, ball, w, pos):
    """
    Handles the game state: catching the ball and scoring.
    """
    # SETUP
    first_ball_pos = [w- 80, 430]
    final_ball_pos = [w -209, 290]
    get_ball_dist = 40 # Increased distance tolerance slightly
    dist_to_start = distance(x_y_index_knuckle[0], x_y_index_knuckle[1], first_ball_pos[0], first_ball_pos[1])
    dist_to_goal = distance(x_y_index_knuckle[0], x_y_index_knuckle[1], final_ball_pos[0], final_ball_pos[1])
    
    # LOGIC
    # 1. Catch the ball
    if close_hand and dist_to_start <= get_ball_dist:
        on_catch_ball = True
        lock_bug_score = False # Allow scoring next time
    # 2. Score the goal
    elif on_catch_ball and not close_hand and dist_to_goal <= get_ball_dist and not lock_bug_score:
        score += 1
        on_catch_ball = False
        lock_bug_score = True # Prevent re-scoring immediately
    # 3. Drop the ball
    elif not close_hand:
        on_catch_ball = False
    
    # DRAWING (Only draw the ball on the hand if caught)
    if on_catch_ball:
        # Overlay the image (THIS LINE NOW UPDATES THE FRAME)
        frame = overlay_img(frame, ball, pos)
    
    # Draw Start and Goal targets
    color_first_ball = (255, 0, 0) if dist_to_start >= (get_ball_dist) else (255, 0, 255)
    color_final_ball = (0, 255, 0) if dist_to_goal <= get_ball_dist else (0, 0, 255)
    cv.circle(frame, first_ball_pos, 40, color_first_ball, 5) # Reduced circle thickness
    cv.circle(frame, final_ball_pos, 40, color_final_ball, 5) # Reduced circle thickness
    
    # Return the score, state variables, AND THE MODIFIED FRAME
    return score, on_catch_ball, lock_bug_score, frame


def badminton(frame, close_hand, badminton_rac, shuttlecock ,x_y_index_knuckle, pos):

    if (close_hand):
        frame = overlay_img(frame, badminton_rac, pos, 0.15,1,0,-150)
    return frame