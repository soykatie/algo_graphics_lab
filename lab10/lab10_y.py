import cv2
import numpy as np

weights_path = 'yolo3/yolov3.weights' 
config_path = 'yolo3/yolov3.cfg'
names_path = 'yolo3/coco.names'

# загрузка классов
with open(names_path, 'r') as f:
    classes = f.read().strip().split('\n')

# загрузка сети YOLO
net = cv2.dnn.readNet(weights_path, config_path)

# ф-я распознавания объектов
def recognize_objects(image_path):
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
            if confidence > 0.5:  # уровень уверенности
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

    # проверка результата NMS
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = (0, 255, 0)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image, label, (x, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Распознавание объектов", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image_path = 'source/img3.jpg'
recognize_objects(image_path)
