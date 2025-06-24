import cv2
import numpy as np
from pycoral.utils.edgetpu import make_interpreter
from pycoral.adapters import common

# Load model
model_path = 'models/deeplabv3_mnv2_dm05_pascal_quant_edgetpu.tflite'
interpreter = make_interpreter(model_path)
interpreter.allocate_tensors()

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame to model input size
    size = common.input_size(interpreter)
    resized = cv2.resize(frame, size)

    # Set input tensor and invoke interpreter
    common.set_input(interpreter, resized)
    interpreter.invoke()

    # Get raw output tensor
    output_details = interpreter.get_output_details()[0]
    output_data = interpreter.tensor(output_details['index'])()[0]

    # output_data shape might be (257, 257, 1) or (1, 257, 257, 1)
    # Convert to 2D if needed:
    mask = output_data.squeeze()
    # mask is an int array with class IDs per pixel, e.g. person = 15 in PASCAL VOC

    # Create a boolean mask for person class (15)
    person_mask = (mask == 15)

    # Resize mask back to original frame size
    person_mask_resized = cv2.resize(person_mask.astype(np.uint8), (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)

    # Create green mask overlay
    green_mask = np.zeros_like(frame)
    green_mask[:, :, 1] = 255  # green channel

    # Overlay the mask on original frame
    output = cv2.addWeighted(frame, 1.0, green_mask, 0.5, 0, mask=person_mask_resized)

    cv2.imshow('Person Segmentation', output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
