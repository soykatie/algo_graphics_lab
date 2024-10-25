import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def load_image(image_path):
    return Image.open(image_path)

def convert_to_grayscale(image):
    return image.convert('L')

def binarize_image(gray_image, threshold=128):
    return gray_image.point(lambda p: 255 if p > threshold else 0)

def mean_filter(image_array, kernel_size=3):
    """Применяет средний фильтр к изображению."""
    pad_size = kernel_size // 2
    padded_image = np.pad(image_array, pad_size, mode='edge')
    filtered_image = np.zeros_like(image_array)

    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            # извлечение региона изображения
            region = padded_image[i:i + kernel_size, j:j + kernel_size]
            # вычисление среднего значения
            filtered_image[i, j] = np.mean(region)

    return filtered_image

def display_images(gray, binary, cleaned_binary, cleaned_gray):
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
    plt.imshow(cleaned_gray, cmap='gray')
    plt.title('Устранение шумов на полутоновом изображении')
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.imshow(cleaned_binary, cmap='gray')
    plt.title('Устранение шумов на бинарном изображении')
    plt.axis('off')

    plt.tight_layout(pad=3.0)
    plt.show()

image_path = 'source/pic_2.jpg'

# загрузка и обработка изображения
image = load_image(image_path)  
gray_image = convert_to_grayscale(image)  
binary_image = binarize_image(gray_image) 

# устранение шумов, ядро = 3 либо 6
cleaned_binary = mean_filter(np.array(binary_image), kernel_size=6)
cleaned_gray = mean_filter(np.array(gray_image), kernel_size=6)

# преобразование очищенных массивов обратно в изображения
cleaned_binary_image = Image.fromarray(cleaned_binary)
cleaned_gray_image = Image.fromarray(cleaned_gray)

display_images(gray_image, binary_image, cleaned_binary_image, cleaned_gray_image)