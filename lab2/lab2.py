from PIL import Image, ImageDraw
import math
import random

def create_polygon_image(sides, color, size=(200, 200)):
    img = Image.new("RGB", size, (255, 255, 255)) # белый фон
    draw = ImageDraw.Draw(img)

    # генерация случайных координат вершин многоугольника
    vertices = []
    center_x = size[0] // 2
    center_y = size[1] // 2
    radius = min(center_x, center_y) * 0.8 # радиус генерации вершин
    for i in range(sides):
        angle = i * 2 * 3.14159 / sides
        x = center_x + int(radius * math.cos(angle))
        y = center_y + int(radius * math.sin(angle))
        vertices.append((x, y))

    """"
    # если неправильный многоугольник, то генерируем случайные координаты вершин 
    vertices = [(random.randint(0, size[0]), random.randint(0, size[1])) 
                for _ in range(sides)] 
    """

    # закрашиваем многоугольник
    draw.polygon(vertices, fill=color)

    return img # возвращаем изображение с закрашенным многоугольником

# использование
sides = random.randint(3, 12) # случайное количество сторон от 3 до 12
color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) # случайный цвет (RGB)
polygon_image = create_polygon_image(sides, color)

# отображение
polygon_image.show()
