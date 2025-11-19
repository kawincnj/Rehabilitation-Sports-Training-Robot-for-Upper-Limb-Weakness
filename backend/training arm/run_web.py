import uvicorn
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# Assuming game_processor.py is in the same directory
from game_processor import GameProcessor 

# Initialize FastAPI application
app = FastAPI()

# --- Global GameProcessor Instance ---
# We'll initialize this when the app starts up
game_processor: GameProcessor = None 

# --- CORS Middleware (Required for web communication) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Application Startup Event ---
@app.on_event("startup")
async def startup_event():
    """Initializes the GameProcessor when the FastAPI application starts."""
    global game_processor
    try:
        # Initialize GameProcessor with desired parameters
        game_processor = GameProcessor(
            game_mode='pingpong', # Choose your mode
            is_show_skeleton=True
        )
        print("GameProcessor initialized successfully.")
    except Exception as e:
        # If initialization fails, log the error and raise an exception to halt startup
        print(f"ERROR: Failed to initialize GameProcessor: {e}")
        # Consider a more detailed exception handling based on the actual GameProcessor needs
        raise Exception("GameProcessor could not be initialized. Check dependencies.")

# --- API Endpoint for Frame Processing ---
@app.post("/process_frame")
async def process_frame(file: UploadFile = File(...)):
    """
    Receives an image file, processes it using the GameProcessor, and returns the modified image.
    """
    global game_processor
    
    # Safety check: Ensure the processor is initialized
    if game_processor is None:
        raise HTTPException(status_code=503, detail="Game processor is not ready.")

    try:
        # --- 1. Read and Decode Image Data ---
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            raise ValueError("Could not decode image.")

        # --- 2. OpenCV Processing using GameProcessor ---
        # This is where your custom logic replaces the simple cv2.rectangle()
        processed_frame, score = game_processor.process_frame(frame)
        
        # Optionally, you can log the score or include it in the response header/body
        # For simplicity, we'll only return the image here, but the score is available.
        # print(f"Current Frame Score: {score}") 

        # --- 3. Encode and Return Processed Image ---
        
        # Encode the processed OpenCV image back into PNG format
        is_success, buffer = cv2.imencode(".png", processed_frame)
        
        if not is_success:
            raise RuntimeError("Could not encode processed image.")
            
        # Return the byte array directly
        return Response(content=buffer.tobytes(), media_type="image/png")

    except ValueError as e:
        return Response(status_code=400, content=f"Bad Request: {e}")
    except RuntimeError as e:
        return Response(status_code=500, content=f"Server Error during encoding: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return Response(status_code=500, content=f"Internal Server Error: {e}")

# --- Run the server ---
if __name__ == "__main__":
    # The server will run on htttp://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)