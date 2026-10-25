
import math
import sys

NAME = "Maria"
SURNAME = "Vovk"
GROUP = "І-23"

# Розміри кімнати в метрах
LENGTH = 4.2
WIDTH = 3.5
HEIGHT = 2.7

# Розміри дверей і вікна
DOOR_WIDTH = 0.9
DOOR_HEIGHT = 2.0
WINDOW_WIDTH = 1.4
WINDOW_HEIGHT = 1.5

# Розміри плитки та ціна за одну плитку
TILE_LENGTH = 0.3
TILE_WIDTH = 0.3
TILE_PRICE = 42.30

print(f"{NAME} {SURNAME}, {GROUP}")

# Перевірка розмірів
if min(
    LENGTH, WIDTH, HEIGHT,
    DOOR_WIDTH, DOOR_HEIGHT,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    TILE_LENGTH, TILE_WIDTH, TILE_PRICE
) <= 0:
    print("Помилка: значення мають бути більшими за 0",
          file=sys.stderr)
    sys.exit(1)

# Обчислюємо площу підлоги та стін
floor_area = LENGTH * WIDTH

wall_area = (
    2 * LENGTH * HEIGHT
    + 2 * WIDTH * HEIGHT
    - DOOR_WIDTH * DOOR_HEIGHT
    - WINDOW_WIDTH * WINDOW_HEIGHT
)

# Обчислюємо діагоналі
floor_diagonal = math.hypot(LENGTH, WIDTH)

room_diagonal = math.dist(
    (0, 0, 0),
    (LENGTH, WIDTH, HEIGHT)
)

# Обчислюємо кількість плиток
tile_area = TILE_LENGTH * TILE_WIDTH
tiles_exact = floor_area / tile_area

tiles_round = round(tiles_exact)
tiles_floor = math.floor(tiles_exact)
tiles_ceil = math.ceil(tiles_exact)

# Додаємо 10% запасу
tiles_to_buy = math.ceil(tiles_exact * 1.10)

# Обчислюємо кількість фарби
paint_liters = wall_area * 2 / 10
paint_cans = math.ceil(paint_liters / 2.5)

# Обчислюємо вартість плитки двома способами
cost_mul = tiles_to_buy * TILE_PRICE

cost_sum = 0.0
for _ in range(tiles_to_buy):
    cost_sum += TILE_PRICE

# Виводимо результати
print(f"room:          {LENGTH} x {WIDTH} x {HEIGHT} m")
print(f"floor area:    {floor_area:.2f} m2")
print(f"wall area:     {wall_area:.2f} m2")
print(f"floor diag:    {floor_diagonal:.2f} m")
print(f"room diag:     {room_diagonal:.2f} m")

print()
print(f"tiles exact:   {tiles_exact:.2f}")
print(f"  round:       {tiles_round}")
print(f"  floor:       {tiles_floor}")
print(f"  ceil:        {tiles_ceil}")
print(f"tiles to buy:  {tiles_to_buy} (+10% spare)")
print(f"paint:         {paint_liters:.2f} l -> "
      f"{paint_cans} cans of 2.5 l")

print()
print(f"tiles cost:    {cost_mul:.2f} UAH")
print(f"sum == mul:    {cost_sum == cost_mul}")
print(f"isclose:       {math.isclose(cost_sum, cost_mul)}")
print(f"difference:    {abs(cost_sum - cost_mul)}")
