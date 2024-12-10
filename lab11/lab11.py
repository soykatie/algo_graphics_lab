import cv2
import numpy as np

weights_path = 'yolov4/yolov4.weights' 
config_path = 'yolov4/yolov4.cfg'
names_path = 'yolov4/coco.names'

# загрузка классов
with open(names_path, 'r') as f:
    classes = f.read().strip().split('\n')

# загрузка сети YOLO
net = cv2.dnn.readNet(weights_path, config_path)

# Функция для распознавания объектов
def recognize_objects(image_path, confidence_threshold):
    # загрузка изображения
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

    # создание blob из изображения
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)

    # получение выходных слоев
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # прямой проход по сети
    outputs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    # обработка выходных данных
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold:  # уровень уверенности
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # удаление дубликатов
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Подсчет TP, FP и FN
    TP = 0
    FP = 0
    FN = 0 

    detected_labels = []

    # Проверка результата NMS
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            detected_labels.append(label)
            TP += 1

    # подсчет FN (истинные метки не установлены, поэтому считается просто как количество классов)
    FN = len(classes) - TP  # предполагается, что если класс не обнаружен, он остается незасечённым

    # остальные обнаруженные объекты считаем FP
    FP = len(detected_labels) - TP

    # вычисление precision и recall
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0

    # ограничение precision не более 1
    precision = min(precision, 1)

    print(f"Image: {image_path} - Confidence: {confidence_threshold:.2f}")
    print(f"Detected Labels: {detected_labels}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}\n")

# обработка изображений с разными уровнями уверенности
for i in range(1, 11):
    image_path = f'source/img{i}.jpg'
    for confidence in np.arange(0.3, 1.0, 0.2):
        recognize_objects(image_path, confidence)
