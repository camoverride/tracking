import cv2
import mediapipe as mp
import numpy as np
import yaml



with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)


# Initialize MediaPipe Selfie Segmentation
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segment = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# Open webcam
cap = cv2.VideoCapture(0)

# Define the overlay color (RGBA) - Green with alpha
overlay_color = (0, 255, 0, 100)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize for faster processing (optional)
    small_frame = cv2.resize(frame, (320, 240))
    rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Get segmentation mask
    results = segment.process(rgb)
    mask = results.segmentation_mask
    mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))

    # Create binary mask (people = 1, background = 0)
    condition = mask > 0.5
    condition = condition.astype(np.uint8)

    # Create colored transparent overlay
    overlay = np.zeros_like(frame, dtype=np.uint8)
    overlay[:] = overlay_color[:3]
    mask_3ch = cv2.merge([condition]*3)

    # Blend original with overlay using the alpha channel
    alpha = overlay_color[3] / 255.0
    blended = np.where(mask_3ch == 1, cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0), frame)

    # display_im = cv2.resize(blended, (config["monitor_width"], config["monitor_height"]))

    # Show the result
    cv2.imshow('Person Segmentation', blended)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
