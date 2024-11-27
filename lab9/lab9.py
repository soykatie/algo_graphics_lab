import cv2
import numpy as np
import matplotlib.pyplot as plt

def region_growing(image, seed_point, threshold):
    '''Метод роста областей'''
    height, width = image.shape
    segmented_region = np.zeros_like(image, dtype=np.uint8) 
    visited = np.zeros_like(image, dtype=bool)  # массив для отметки посещённых пикселей

    # стек для обработки пикселей
    stack = [seed_point]
    seed_value = image[seed_point]  # значение пикселя в точке отсчета
    visited[seed_point] = True  # отмечаем пиксель как посещенный

    while stack:
        current_point = stack.pop()
        x, y = current_point

        # устанавливаем текущий пиксель как часть сегмента
        segmented_region[x, y] = 255

        # проход по соседям текущего пикселя
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_x, neighbor_y = x + i, y + j

                # проверка границ изображения
                if 0 <= neighbor_x < height and 0 <= neighbor_y < width:
                    # если сосед еще не посещен
                    if not visited[neighbor_x, neighbor_y]:
                        # проверяем разницу значений пикселей
                        if abs(int(image[neighbor_x, neighbor_y]) - int(seed_value)) < threshold:
                            stack.append((neighbor_x, neighbor_y))  # добавляем соседа в стек
                        visited[neighbor_x, neighbor_y] = True  # помечаем как посещенный

    return segmented_region

def split_merge(image, threshold):
    '''Метод разделения и слияния'''
    height, width = image.shape
    segmented = np.zeros_like(image)

    def split(x, y, h, w):
        if h <= 1 or w <= 1:
            return

        region = image[y:y+h, x:x+w]
        mean_value = np.mean(region)

        if np.all(np.abs(region - mean_value) < threshold):
            segmented[y:y+h, x:x+w] = mean_value  # заполняем область средним значением
        else:
            half_h, half_w = h // 2, w // 2
            split(x, y, half_h, half_w)               # верхняя левая
            split(x + half_w, y, half_h, w - half_w)  # верхняя правая
            split(x, y + half_h, h - half_h, half_w)  # нижняя левая
            split(x + half_w, y + half_h, h - half_h, w - half_w)  # нижняя правая

    split(0, 0, height, width)
    return segmented

image = cv2.imread('img.jpg', cv2.IMREAD_GRAYSCALE)

# параметры для сегментации методом роста областей
seed = (150, 200)  # точка отсчета (семени)
threshold_growth = 100   # порог

segmented_growth = region_growing(image, seed, threshold_growth)

# параметры для сегментации методом разделения и слияния
threshold_split_merge = 15  # порог для разделения и слияния

segmented_split_merge = split_merge(image, threshold_split_merge)

plt.figure(figsize=(12, 6))

plt.subplot(1, 3, 1)
plt.title('Исходное изображение')
plt.imshow(image, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title('Сегментация методом роста областей')
plt.imshow(segmented_growth, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title('Сегментация методом разделения и слияния')
plt.imshow(segmented_split_merge, cmap='gray')
plt.axis('off')

plt.show()
