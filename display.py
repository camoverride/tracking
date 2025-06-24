import cv2
import numpy as np
from pycoral.adapters import common, segmentation
from pycoral.utils.edgetpu import make_interpreter



# Load model
model_path = 'models/deeplabv3_mnv2_dm05_pascal_quant_edgetpu.tflite'
interpreter = make_interpreter(model_path)
interpreter.allocate_tensors()

# Open webcam (0)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame to model input size
    size = common.input_size(interpreter)
    resized_frame = cv2.resize(frame, size)

    # Set input tensor
    common.set_input(interpreter, resized_frame)

    # Run inference
    interpreter.invoke()

    # Get segmentation mask
    seg_map = segmentation.get_output(interpreter)

    # Create a color mask for person class (usually class 15 in PASCAL VOC)
    # You can adjust colors as you like
    person_mask = seg_map == 15  # person class index
    mask_color = np.array([0, 255, 0], dtype=np.uint8)  # green mask

    # Create colored mask
    colored_mask = np.zeros_like(frame, dtype=np.uint8)
    colored_mask[person_mask] = mask_color

    # Overlay mask on original frame
    output = cv2.addWeighted(frame, 1.0, colored_mask, 0.5, 0)

    # Show output
    cv2.imshow('Person Segmentation', output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
