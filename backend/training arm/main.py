import cv2 as cv
from game_processor import GameProcessor 

def main():
    cap = cv.VideoCapture(0)
    
    game_processor = GameProcessor(game_mode='football', is_show_skeleton = False) # 'football', 'badminton', 'ball', 'pingpong
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        processed_frame, score = game_processor.process_frame(frame)
        print(score)
        
        cv.imshow('Hand Detection and Game', processed_frame)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()