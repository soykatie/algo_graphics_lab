from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

# ф-я для создания изображения с фигурой и подписью
def create_figure_img(figure_type, color, text, image_size=(200, 200)):
    img = Image.new("RGB", image_size, (255, 255, 255))  # белый фон
    draw = ImageDraw.Draw(img)
    
    if figure_type == 'line':
        draw.line((50, 100, 150, 100), fill=color, width=3)
    elif figure_type == 'circle':
        draw.ellipse((50, 50, 150, 150), outline=color, width=3)
    elif figure_type == 'ellipse':
        draw.ellipse((50, 50, 150, 100), outline=color, width=3)
    
    draw.text((10, 10), text, fill=(0, 0, 0), font=ImageFont.truetype("arial.ttf", 10))  # подпись

    return img

# создание изображений для каждой фигуры
line_image = create_figure_img('line', (255, 0, 0), "Отрезок")
circle_image = create_figure_img('circle', (0, 255, 0), "Окружность")
ellipse_image = create_figure_img('ellipse', (0, 0, 255), "Эллипс")

# отображение изображений в виде таблицы
fig, axs = plt.subplots(1, 3, figsize=(10, 5))

# отображаем каждую фигуру в отдельной ячейке (+ убираем оси)
axs[0].imshow(line_image)
axs[0].axis('off') 

axs[1].imshow(circle_image)
axs[1].axis('off')

axs[2].imshow(ellipse_image)
axs[2].axis('off')

plt.tight_layout()
plt.show()