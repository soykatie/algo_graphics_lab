import cv2
import numpy as np

# ф-я распознавания объектов
def recognize_objects(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Ошибка загрузки изображения")
        return

    # преобразование в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # применение гауссового размытия 
    # для уменьшения шума и деталей в изображении,
    # что делает контуры более четкими при поиске
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # бинаризация изображения
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)

    # нахождение контуров
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # рисование контуров на исходном изображении
    for contour in contours:
        # игнорирование маленьких контуров
        if cv2.contourArea(contour) > 100:
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

    cv2.imshow("Исходное изображение", image)
    cv2.imshow("Бинаризированное изображение", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image_path = 'source/img2.jpg'
recognize_objects(image_path)
