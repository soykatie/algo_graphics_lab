import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def load_image(image_path):
    """Загружает изображение из файла."""
    return Image.open(image_path)

def convert_to_grayscale(image):
    """Преобразует цветное изображение в полутоновое (оттенки серого)."""
    return image.convert('L')

def binarize_image(gray_image, threshold=128):
    """Бинаризует полутоновое изображение по заданному порогу."""
    # Применяем пороговую фильтрацию
    binary_image = gray_image.point(lambda p: 255 if p > threshold else 0)
    return binary_image

def display_images(original, gray, binary):
    """Отображает оригинальное, полутоновое и бинаризованное изображения."""
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(original)
    plt.title('Оригинальное изображение')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(gray, cmap='gray')
    plt.title('Полутоновое изображение')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(binary, cmap='gray')
    plt.title('Бинаризованное изображение')
    plt.axis('off')

    plt.show()

# Основная программа
image_path = 'source/pic_1.jpg'  # Укажите путь к вашему изображению

# Загрузка и обработка изображения
image = load_image(image_path)  # Загрузка изображения
gray_image = convert_to_grayscale(image)  # Преобразование в полутоновое
binary_image = binarize_image(gray_image)  # Бинаризация изображения

# Отображение результатов
display_images(image, gray_image, binary_image)