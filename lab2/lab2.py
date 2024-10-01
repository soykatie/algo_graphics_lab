from PIL import Image, ImageDraw
import random

def create_polygon_image(sides, color, size=(200, 200)):
    """Создает изображение с закрашенным неправильным многоугольником.

    Args:
        sides (int): Количество сторон многоугольника.
        color (tuple): Цвет многоугольника в формате RGB (например, (255, 0, 0) для красного).
        size (tuple, optional): Размер изображения в пикселях. Defaults to (200, 200).

    Returns:
        Image: Изображение с закрашенным неправильным многоугольником.
    """
    img = Image.new("RGB", size, (255, 255, 255)) # Белый фон
    draw = ImageDraw.Draw(img)

    # Генерируем случайные координаты вершин 
    vertices = [(random.randint(0, size[0]), random.randint(0, size[1])) 
                for _ in range(sides)] 

    # Закрашиваем многоугольник
    draw.polygon(vertices, fill=color)

    return img

# Пример использования:
sides = random.randint(3, 8) # Случайное количество сторон от 3 до 8
color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) # Случайный цвет
polygon_image = create_polygon_image(sides, color)

# Отображаем изображение
polygon_image.show()
