import cv2 as cv
import base64
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json

# Import your existing class
from game_processor import GameProcessor 
from motion_detect import HandMotionDetector

app = FastAPI()

# Allow CORS (Cross-Origin Resource Sharing) for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/{game_mode}")
async def websocket_endpoint(websocket: WebSocket, game_mode: str):
    await websocket.accept()
    
    # Initialize your GameProcessor based on the URL parameter
    # Ensure game_mode matches your class expectations ('ball', 'football', etc.)
    print(f"Client connected. Starting Game Mode: {game_mode}")
    
    try:
        processor = GameProcessor(game_mode=game_mode, is_show_skeleton=True)
        detector = HandMotionDetector(smoothing=0.2, xy_threshold=50, z_threshold=40)
    except Exception as e:
        print(f"Error initializing processor: {e}")
        await websocket.close()
        return

    try:
        while True:
            # 1. Receive Base64 frame from Client
            data = await websocket.receive_text()
            
            # 2. Decode Base64 to OpenCV Image
            # Remove header "data:image/jpeg;base64,"
            if "base64," in data:
                header, encoded = data.split(",", 1)
            else:
                encoded = data
                
            img_bytes = base64.b64decode(encoded)
            nparr = np.frombuffer(img_bytes, np.uint8)
            frame = cv.imdecode(nparr, cv.IMREAD_COLOR)

            if frame is None:
                continue

            # 3. Process Frame (Your Game Logic)
            processed_frame, score, hand_landmark = processor.process_frame(frame)
            if hand_landmark:
                motion_data = detector.process(hand_landmark, 960, 720)
                print(motion_data["velocity"])

            # 4. Encode Processed Frame back to Base64
            _, buffer = cv.imencode('.jpg', processed_frame)
            processed_base64 = base64.b64encode(buffer).decode('utf-8')

            # 5. Send Result back to Client
            response_data = {
                "image": f"data:image/jpeg;base64,{processed_base64}",
                "score": score
            }
            await websocket.send_text(json.dumps(response_data))

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import uvicorn
    # Run the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)