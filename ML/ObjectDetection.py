import cv2
import numpy as np
from ultralytics import YOLO
import easyocr
import winsound 
import time
import re

PHONE_IP_URL = "GIVEN LINK"  #LINK for the video 
CONF_THRESHOLD = 0.5

# --- 1. SETUP (Runs once at start) ---
print("⏳ Loading OCR Engine (this takes 10 seconds)...")
reader = easyocr.Reader(['en'], gpu=False)  # Reads text

print("🚀 Loading AI Model...")
model = YOLO("yolo11n.pt")  # Detects objects

print("🎥 Connecting to Camera...")
cap = cv2.VideoCapture(PHONE_IP_URL)

frame_count = 0

# --- 2. MAIN LOOP (Runs 30 times per second) ---
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Signal Lost! Reconnecting...")
        cap = cv2.VideoCapture(PHONE_IP_URL)
        continue

    # Resize to make it run fast
    frame = cv2.resize(frame, (1024, 600))
    frame_count += 1

    # --- PART A: RUN YOLO (Fast) ---
    # We track everything every single frame
    results = model(frame, stream=True, verbose=False)

    riders = []
    bikes = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Class 0 = Person
            if cls == 0:
                riders.append([x1, y1, x2, y2])
            
            # Class 3 = Motorcycle
            elif cls == 3:
                bikes.append([x1, y1, x2, y2])
                
                # --- PART B: RUN OCR (Slow - Only every 10th frame) ---
                if frame_count % 10 == 0:
                    try:
                        # Crop the bike area
                        plate_roi = frame[y1:y2, x1:x2]
                        
                        # Read text
                        ocr_out = reader.readtext(plate_roi)
                        
                        for (bbox, text, prob) in ocr_out:
                            # Filter for Plate-like text (Alphanumeric & >4 chars)
                            clean_text = re.sub(r'[^A-Z0-9]', '', text.upper())
                            if len(clean_text) > 4 and prob > 0.4:
                                # Draw Plate on screen
                                cv2.putText(frame, f"PLATE: {clean_text}", (x1, y2-10),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                                print(f"📝 Plate Found: {clean_text}")
                    except:
                        pass

    # --- PART C: VIOLATION LOGIC ---
    # Check if a Rider is inside a Bike box
    for rx1, ry1, rx2, ry2 in riders:
        rider_center = ((rx1+rx2)//2, (ry1+ry2)//2)
        
        is_riding = False
        for bx1, by1, bx2, by2 in bikes:
            if bx1 < rider_center[0] < bx2 and by1 < rider_center[1] < by2:
                is_riding = True
                #Green Box on the Bike
                cv2.rectangle(frame, (bx1, by1), (bx2, by2), (0, 255, 0), 2)
                break
        
        if is_riding:
            
            # Draw RED Box on Rider
            cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (0, 0, 255), 3)
            cv2.putText(frame, "NO HELMET", (rx1, ry1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # Beep (every 30 frames) 
            if frame_count % 30 == 0:
                winsound.Beep(1000, 200)

    # PART D: DISPLAY 
    cv2.imshow("Trinetra Dashboard", frame)
    
    # Press 'q' to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()