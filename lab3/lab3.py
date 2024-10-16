import matplotlib.pyplot as plt
import random

# ф-я для генерации случайного многоугольника
def generate_random_polygon(num_points, x_range, y_range):
    polygon = [(random.randint(*x_range), random.randint(*y_range)) for _ in range(num_points)]
    return polygon

# ф-я для отсечения многоугольника
def clip_polygon(polygon, clip_window):
    def inside(p, edge):
        if edge == "LEFT":
            return p[0] >= clip_window[0][0]
        elif edge == "RIGHT":
            return p[0] <= clip_window[1][0]
        elif edge == "BOTTOM":
            return p[1] >= clip_window[0][1]
        elif edge == "TOP":
            return p[1] <= clip_window[1][1]
    
    def compute_intersection(p1, p2, edge):
        x1, y1 = p1
        x2, y2 = p2
        if edge == "LEFT":
            x_edge = clip_window[0][0]
            y = y1 + (y2 - y1) * (x_edge - x1) / (x2 - x1)
            return (x_edge, y)
        elif edge == "RIGHT":
            x_edge = clip_window[1][0]
            y = y1 + (y2 - y1) * (x_edge - x1) / (x2 - x1)
            return (x_edge, y)
        elif edge == "BOTTOM":
            y_edge = clip_window[0][1]
            x = x1 + (x2 - x1) * (y_edge - y1) / (y2 - y1)
            return (x, y_edge)
        elif edge == "TOP":
            y_edge = clip_window[1][1]
            x = x1 + (x2 - x1) * (y_edge - y1) / (y2 - y1)
            return (x, y_edge)
    
    def clip_polygon_by_edge(polygon, edge):
        new_polygon = []
        for i in range(len(polygon)):
            current_point = polygon[i]
            prev_point = polygon[i - 1]

            if inside(current_point, edge):
                if not inside(prev_point, edge):
                    intersection = compute_intersection(prev_point, current_point, edge)
                    new_polygon.append(intersection)
                new_polygon.append(current_point)
            elif inside(prev_point, edge):
                intersection = compute_intersection(prev_point, current_point, edge)
                new_polygon.append(intersection)
        
        return new_polygon
    
    edges = ["LEFT", "RIGHT", "BOTTOM", "TOP"]
    output_polygon = polygon
    
    for edge in edges:
        output_polygon = clip_polygon_by_edge(output_polygon, edge)
    
    return output_polygon

# параметры генерации окна отсечения
x_min = random.randint(50, 150)
y_min = random.randint(50, 150)
x_max = random.randint(x_min + 50, x_min + 150)  # минимальная ширина 50, максимальная 150
y_max = random.randint(y_min + 50, y_min + 150)  # минимальная высота 50, максимальная 150
clip_window = [(x_min, y_min), (x_max, y_max)]

# генерация случайного мн-ка
num_points = random.randint(3, 7)  # количество вершин от 3 до 7
polygon = generate_random_polygon(num_points, (0, 250), (0, 250))

# отсечение мн-ка
clipped_polygon = clip_polygon(polygon, clip_window)

# визуализация
plt.figure(figsize=(8, 8))
plt.plot(*zip(*polygon, polygon[0]), marker='o', color='orange', linewidth=2, label='Исходный многоугольник')
if clipped_polygon:
    plt.plot(*zip(*clipped_polygon, clipped_polygon[0]), marker='o', color='purple', linewidth=2, label='Отсечённый многоугольник')
    plt.fill(*zip(*clipped_polygon, clipped_polygon[0]), color='purple', alpha=0.7)

# окно отсечения
plt.axhline(clip_window[0][1], color='green', linestyle='--')
plt.axhline(clip_window[1][1], color='green', linestyle='--')
plt.axvline(clip_window[0][0], color='green', linestyle='--')
plt.axvline(clip_window[1][0], color='green', linestyle='--')
plt.fill_between([clip_window[0][0], clip_window[1][0]], clip_window[0][1], clip_window[1][1], color='lightgreen', alpha=0.5)

# настройки графика
plt.xlim(0, 300)
plt.ylim(0, 300)
plt.legend()
plt.title('Отсечение случайного многоугольника')
plt.grid()
plt.show()
