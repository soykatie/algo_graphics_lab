import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = 'source/pic_3.jpg'
image = cv2.imread(image_path)

# преобразование изображения в оттенки серого
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# построение гистограммы
histogram, bins = np.histogram(gray_image.flatten(), bins=256, range=[0, 256])

plt.figure(figsize=(10, 5))

# создание градиентного эффекта
colors = plt.cm.viridis(np.linspace(0, 1, len(histogram)))

for i in range(len(histogram) - 1):
    plt.fill_between(bins[i:i+2], histogram[i:i+2], color=colors[i], alpha=0.7)

plt.title('Гистограмма изображения')
plt.xlabel('Интенсивность пикселей (от черного к белому)')
plt.ylabel('Число пикселей')
plt.xlim([0, 256])
plt.grid()
plt.show()