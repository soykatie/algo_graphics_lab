import numpy as np
import matplotlib.pyplot as plt

# Полином Эрмита для интерполяции между двумя точками с производными
def hermite_interpolate(x0, x1, y0, y1, dy0, dy1, x):
    t = (x - x0) / (x1 - x0)  # нормализуем переменную
    h_00 = (1 + 2 * t) * (1 - t)**2  # h_00(t) для y0
    h_10 = t * (1 - t)**2            # h_10(t) для dy0
    h_01 = t**2 * (3 - 2 * t)        # h_01(t) для y1
    h_11 = t**2 * (t - 1)            # h_11(t) для dy1
    
    # Полином Эрмита
    H_x = h_00 * y0 + h_10 * (x1 - x0) * dy0 + h_01 * y1 + h_11 * (x1 - x0) * dy1
    return H_x

# Исходные данные (точки для интерполяции)
points = np.array([
    (0.0, 0.0),  # начальная точка
    (0.5, 1.5),  # опорная точка 1
    (1.0, 0.5),  # опорная точка 2
    (1.5, 1.0),  # опорная точка 3
    (2.0, 0.0),  # опорная точка 4
    (2.5, -1.0), # опорная точка 5
    (3.0, 0.5),  # опорная точка 6
    (3.5, -0.5), # опорная точка 7
    (4.0, 0.0),  # конечная точка
])

# Рассчитаем производные как касательные к отрезкам между соседними точками
def compute_tangents(points):
    tangents = []
    for i in range(1, len(points) - 1):
        dy = (points[i + 1][1] - points[i - 1][1]) / (points[i + 1][0] - points[i - 1][0])  # центральная разностная производная
        tangents.append(dy)
    # Добавляем производные в начальной и конечной точках (используя ближайшие точки)
    dy0 = (points[1][1] - points[0][1]) / (points[1][0] - points[0][0])
    dy_last = (points[-1][1] - points[-2][1]) / (points[-1][0] - points[-2][0])
    tangents.insert(0, dy0)
    tangents.append(dy_last)
    return tangents

# Получаем производные для всех точек
tangents = compute_tangents(points)

# Построим кривую Эрмита для каждого сегмента между точками
plt.figure(figsize=(12, 6))

# Перебираем точки по парам
for i in range(len(points) - 1):
    x0, y0 = points[i]
    x1, y1 = points[i + 1]
    dy0 = tangents[i]
    dy1 = tangents[i + 1]
    
    # Генерируем значения x и y для текущего сегмента
    x_vals = np.linspace(x0, x1, 100)
    y_vals = [hermite_interpolate(x0, x1, y0, y1, dy0, dy1, x) for x in x_vals]
    
    # Построение сегмента
    plt.plot(x_vals, y_vals, color="orange")
    
# Отмечаем исходные точки
plt.scatter(points[:, 0], points[:, 1], color="purple", label="Опорные точки")
plt.plot(points[:, 0], points[:, 1], 'k--', label="Соединяющие линии")  # соединяем опорные точки

# Оформление графика
plt.xlabel("x")
plt.ylabel("H(x)")
plt.legend()
plt.title("Аппроксимация Эрмита")
plt.grid(True)
plt.show()
