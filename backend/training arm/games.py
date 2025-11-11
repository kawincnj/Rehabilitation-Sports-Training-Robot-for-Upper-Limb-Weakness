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


def badminton(frame, close_hand, badminton_rac, shuttlecock ,x_y_index, pos, w, on_catch_ball, score):
    
    # SETUP
    top_line = 40
    bottom_line = 210

    if (close_hand):
        badminton_face_mid_pos = (pos[0], pos[1] - 240)
        is_above_top_line = not (badminton_face_mid_pos[1] - top_line) > 0
        is_above_bottom_line = not (badminton_face_mid_pos[1] - bottom_line) > 0

        frame = overlay_img(frame, badminton_rac, pos, 0.15,1,0,-150) #add badminton rac

        if (is_above_top_line) :
            on_catch_ball = True
            if(on_catch_ball): frame = overlay_img(frame, shuttlecock, badminton_face_mid_pos, 0.02)
        elif (on_catch_ball):
            frame = overlay_img(frame, shuttlecock, badminton_face_mid_pos, 0.02)
            if(not is_above_bottom_line):
                score += 1
                on_catch_ball = False
        else:
            pass

    else: on_catch_ball = False

    cv.line(frame, (0,top_line), (w, top_line), (255,0,0),2)
    cv.line(frame, (0,bottom_line), (w, bottom_line), (255,0,0),2)

    return frame, on_catch_ball, score

def squezz_ball(frame, close_hand, ball_normal, ball_squeez, pos, score, lock_bug_score, ball_size = 0.14):

    if (close_hand):
        frame = overlay_img(frame, ball_squeez, pos, ball_size)
        lock_bug_score = True
    else:
        frame = overlay_img(frame, ball_normal, pos, ball_size)
        if(lock_bug_score):
            score += 1
            lock_bug_score = False

    return frame, score, lock_bug_score

def pingpong(frame, score):
    return frame, score