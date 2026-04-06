import uvicorn
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import io


# Initialize FastAPI application
app = FastAPI()

# --- CORS Middleware ---
# This is crucial for the HTML file running on one port (e.g., file:// or a different server)
# to communicate with the FastAPI server running on port 8000.
app.add_middleware(
    CORSMiddleware,
    # Allows all origins for development. Be more restrictive in production.
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process_frame")
async def process_frame(file: UploadFile = File(...)):
    """
    Receives an image file, processes it with OpenCV, and returns the modified image.
    """
    try:
        # --- 1. Read Image Data ---
        # Read the uploaded file contents into a byte string
        contents = await file.read()
        # Convert the byte string into a numpy array (for OpenCV)
        nparr = np.frombuffer(contents, np.uint8)
        # Decode the numpy array into an OpenCV image (BGR format)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return Response(status_code=400, content="Could not decode image.")

        # --- 2. OpenCV Processing (Draw a Rectangle) ---
        
        # Define the coordinates for the top-left rectangle
        # (x_start, y_start), (x_end, y_end)
        start_point = (10, 10)
        end_point = (150, 100)
        # BGR color for green
        color = (0, 255, 0) 
        # Thickness of the rectangle border (in pixels)
        thickness = 2 
        
        # Draw the rectangle on the frame
        cv2.rectangle(frame, start_point, end_point, color, thickness)
        
        # Optionally, add some text
        cv2.putText(
            frame, 
            'Processed by FastAPI', 
            (10, 130), # Position
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.7, # Scale
            color, 
            2 # Thickness
        )

        # --- 3. Encode and Return Processed Image ---
        
        # Encode the processed OpenCV image back into a standard format (e.g., PNG)
        # `imencode` returns a tuple: (status, buffer)
        is_success, buffer = cv2.imencode(".png", frame)
        
        if not is_success:
            return Response(status_code=500, content="Could not encode processed image.")
            
        # Convert the buffer to a bytes object
        image_bytes = io.BytesIO(buffer).read()
        
        # Return the image as a FastAPI Response
        return Response(content=image_bytes, media_type="image/png")

    except Exception as e:
        print(f"An error occurred: {e}")
        return Response(status_code=500, content=f"Internal Server Error: {e}")

# --- Run the server ---
if __name__ == "__main__":
    # The server will run on http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=5500)