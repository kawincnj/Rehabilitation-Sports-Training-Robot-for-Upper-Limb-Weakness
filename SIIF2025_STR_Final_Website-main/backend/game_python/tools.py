import numpy as np
import cv2 as cv

def get_finger_coor(finger, w,h, number):
    return [int(finger.landmark[number].x * w), int(finger.landmark[number].y * h)]

def distance(x1, y1, x2, y2):
    """Calculates the Euclidean distance between two points."""
    return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

def calculate_angle(a, b, c):
    """
    Calculates the angle in degrees between three normalized points A, B, and C,
    with B as the vertex. This is direction-independent using 3D coordinates.
    """
    # Use the 3D coordinates (x, y, z) provided by MediaPipe
    a_pt = np.array([a.x, a.y, a.z])
    b_pt = np.array([b.x, b.y, b.z])
    c_pt = np.array([c.x, c.y, c.z])
    
    # Calculate vectors BA and BC
    ba = a_pt - b_pt
    bc = c_pt - b_pt
    
    # Calculate cosine of angle using dot product formula
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    
    # Clamp the value to avoid math domain error for arccos
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    
    angle = np.arccos(cosine_angle)
    
    return np.degrees(angle)

def is_close_hand(hand_landmarks):

    FINGER_JOINTS = [
        # Thumb
        (hand_landmarks.landmark[4], hand_landmarks.landmark[3], hand_landmarks.landmark[2]),
        # Index
        (hand_landmarks.landmark[8], hand_landmarks.landmark[7], hand_landmarks.landmark[5]),
        # Middle
        (hand_landmarks.landmark[12], hand_landmarks.landmark[11], hand_landmarks.landmark[9]),
        # Ring
        (hand_landmarks.landmark[16], hand_landmarks.landmark[15], hand_landmarks.landmark[13]),
        # Pinky
        (hand_landmarks.landmark[20], hand_landmarks.landmark[19], hand_landmarks.landmark[17]),
    ]
    
    closed_fingers = 0

    ANGLE_THRESHOLD = 150
    for tip, vertex, base in FINGER_JOINTS:
        angle = calculate_angle(tip, vertex, base)
        
        if angle < ANGLE_THRESHOLD: 
            closed_fingers += 1

    return closed_fingers >= 4 

def overlay_img(frame, png, pos, resize_scale = 0.1, rotated_img = -1, offsetX = 0, offsetY = 0):
    """Overlays a transparent PNG image onto the frame at a specified position."""
    if (rotated_img > -1):
        rot = [cv.ROTATE_90_CLOCKWISE, cv.ROTATE_90_COUNTERCLOCKWISE, cv.ROTATE_180]
        png = cv.rotate(png, rot[rotated_img])
    png = cv.resize(png, (0, 0), fx=resize_scale, fy=resize_scale)
    bg = frame.copy()
    b, g, r, a = cv.split(png)
    overlay_color = cv.merge((b, g, r))
    # Normalize alpha channel to 0-1 for blending
    mask = a / 255.0
    mask = cv.merge((mask, mask, mask))
    
    # Choose position (center the image on the specified point 'pos')
    x_center, y_center = pos[0] + offsetX, pos[1] + offsetY
    h_img, w_img = overlay_color.shape[:2]
    
    # Calculate top-left corner
    x = x_center - w_img // 2
    y = y_center - h_img // 2
    
    # --- Prevent out-of-frame errors ---
    h_frame, w_frame = bg.shape[:2]
    
    # Define ROI boundaries
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(w_frame, x + w_img)
    y2 = min(h_frame, y + h_img)
    
    # Calculate the size of the actual visible part of the image
    w_roi = x2 - x1
    h_roi = y2 - y1
    
    if w_roi <= 0 or h_roi <= 0:
        return frame # Skip overlay if outside bounds

    # Calculate image slice indices (for the mask and overlay_color)
    img_x1 = x1 - x
    img_y1 = y1 - y
    img_x2 = img_x1 + w_roi
    img_y2 = img_y1 + h_roi

    # Slice ROI from background, overlay_color, and mask
    roi = bg[y1:y2, x1:x2]
    overlay_roi = overlay_color[img_y1:img_y2, img_x1:img_x2]
    mask_roi = mask[img_y1:img_y2, img_x1:img_x2]

    # Blend using alpha mask
    blended_roi = (roi * (1 - mask_roi) + overlay_roi * mask_roi).astype(np.uint8)
    
    # Place back into the background frame
    bg[y1:y2, x1:x2] = blended_roi
    
    return bg