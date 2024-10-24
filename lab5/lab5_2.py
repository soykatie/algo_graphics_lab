import matplotlib.pyplot as plt
import os

def load_image(image_path):
    """Загрузка изображения из файла."""
    # Используем PIL для загрузки изображения
    from PIL import Image
    return Image.open(image_path)

def image_to_gray(image):
    """Преобразование изображения в оттенки серого."""
    return image.convert('L')

def calculate_histogram(gray_image):
    """Подсчет гистограммы для изображения."""
    histogram = [0] * 256  # 256 уровней серого
    pixels = list(gray_image.getdata())
    
    for pixel in pixels:
        histogram[pixel] += 1

    return histogram

def plot_histogram(histogram):
    """Построение гистограммы с градиентным заполнением."""
    plt.figure(figsize=(10, 5))

    colors = [plt.cm.viridis(i / len(histogram)) for i in range(len(histogram))]

    for i in range(len(histogram) - 1):
        plt.fill_between([i, i + 1], [histogram[i], histogram[i + 1]], color=colors[i], alpha=0.7)

    plt.title('Гистограмма изображения')
    plt.xlabel('Интенсивность пикселей (от черного к белому)')
    plt.ylabel('Число пикселей')
    plt.xlim([0, 256])
    plt.grid()
    plt.show()

image_path = 'source/pic_3.jpg'

# проверка наличия файла
if os.path.exists(image_path):
    image = load_image(image_path)  # загрузка изображения
    gray_image = image_to_gray(image)  # преобразование в оттенки серого
    histogram = calculate_histogram(gray_image)  # подсчет гистограммы
    plot_histogram(histogram)  # построение гистограммы
else:
    print(f"Файл {image_path} не найден.")