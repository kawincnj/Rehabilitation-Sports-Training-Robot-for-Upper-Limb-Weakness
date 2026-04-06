import cv2 as cv

def test_cameras():
    print("Searching for available cameras...")
    available_indices = []
    
    for i in range(10):  # Test indices 0 to 9
        cap = cv.VideoCapture(i)
        if cap.isOpened():
            # Try to grab one frame to verify it's a real video stream
            ret, frame = cap.read()
            if ret:
                w = cap.get(cv.CAP_PROP_FRAME_WIDTH)
                h = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
                print(f"✅ Camera found at index {i} ({int(w)}x{int(h)})")
                available_indices.append(i)
            else:
                print(f"⚠️  Index {i} opened but failed to provide a frame.")
            cap.release()
        else:
            # Silence the common warning logs for closed ports
            pass

    if not available_indices:
        print("❌ No working cameras found.")
    else:
        print(f"\nUse index {available_indices[0]} in your main.py code.")

if __name__ == "__main__":
    test_cameras()