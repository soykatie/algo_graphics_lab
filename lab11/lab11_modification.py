import cv2
import numpy as np

weights_path = 'yolov4/yolov4.weights' 
config_path = 'yolov4/yolov4.cfg'
names_path = 'yolov4/coco.names'

with open(names_path, 'r') as f:
    classes = f.read().strip().split('\n')

net = cv2.dnn.readNet(weights_path, config_path)

target_classes = ['wine glass', 'bottle']
target_class_ids = [classes.index(cls) for cls in target_classes if cls in classes]

def recognize_objects(image_path, confidence_threshold):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    outputs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold and class_id in target_class_ids:  # Уровень уверенности
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    detected_labels = []

    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            detected_labels.append(label)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    print(f"Image: {image_path} - Confidence: {confidence_threshold:.2f}")
    print(f"Detected Labels: {detected_labels}")

    output_image_path = f'output_{confidence_threshold:.2f}.jpg'
    cv2.imwrite(output_image_path, image)
    print(f"Output saved as: {output_image_path}\n")

image_path = 'source/img10.jpg'
confidence_threshold = 0.5
recognize_objects(image_path, confidence_threshold)