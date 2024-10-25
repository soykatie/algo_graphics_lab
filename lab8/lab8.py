import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def load_image(image_path):
    return Image.open(image_path)

def convert_to_grayscale(image):
    return image.convert('L')

def binarize_image(gray_image, threshold=128):
    return gray_image.point(lambda p: 255 if p > threshold else 0)

def find_edges(image_array):
    """Находит границы объектов в изображении."""
    # используем 2D массив для хранения границ
    edges = np.zeros_like(image_array, dtype=np.uint8)
    
    # создаем смещение для доступа к соседям (8 соседей, ядро 3х3)
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    # получаем размеры изображения
    height, width = image_array.shape
    
    # проходим по каждому пикселю изображения
    for i in range(height):
        for j in range(width):
            current_pixel = image_array[i, j]
            # проверяем соседей
            for dx, dy in offsets:
                ni, nj = i + dx, j + dy
                # проверяем границы изображения
                if 0 <= ni < height and 0 <= nj < width:
                    neighbor_pixel = image_array[ni, nj]
                    if neighbor_pixel != current_pixel:
                        edges[i, j] = 0  # черный пиксель
                        break
            else:
                edges[i, j] = 255  # белый пиксель

    return edges

def display_images(gray, binary, edges_gray, edges_binary):
    plt.figure(figsize=(15, 10))

    plt.subplot(2, 2, 1)
    plt.imshow(gray, cmap='gray')
    plt.title('Полутоновое изображение')
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.imshow(binary, cmap='gray')
    plt.title('Бинаризованное изображение')
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.imshow(edges_gray, cmap='gray')
    plt.title('Границы на полутоновом изображении')
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.imshow(edges_binary, cmap='gray')
    plt.title('Границы на бинарном изображении')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

image_path = 'source/pic.jpg'

# загрузка и обработка изображения
image = load_image(image_path)  
gray_image = convert_to_grayscale(image) 
binary_image = binarize_image(gray_image)

# выделение границ
edges_gray = find_edges(np.array(gray_image))  # границы на полутоновом изображении
edges_binary = find_edges(np.array(binary_image))  # границы на бинарном изображении

display_images(gray_image, binary_image, edges_gray, edges_binary)