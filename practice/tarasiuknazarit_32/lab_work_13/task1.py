from math import hypot, dist, floor, ceil, isclose
import sys

print("Nazar Tarasiuk, I-23")

LENGTH = 4.2
WIDTH = 3.5
HEIGHT = 2.7

DOOR_WIDTH = 0.9
DOOR_HEIGHT = 2.0
WINDOW_WIDTH = 1.4
WINDOW_HEIGHT = 1.5

TILE_WIDTH = 0.30
TILE_LENGTH = 0.30
TILE_PRICE = 42.30

try:
    values = [
        LENGTH, WIDTH, HEIGHT,
        DOOR_WIDTH, DOOR_HEIGHT,
        WINDOW_WIDTH, WINDOW_HEIGHT,
        TILE_WIDTH, TILE_LENGTH, TILE_PRICE
    ]

    if any(value <= 0 for value in values):
        raise ValueError("All dimensions and prices must be positive")

    floor_area = LENGTH * WIDTH
    wall_area = (
        2 * LENGTH * HEIGHT
        + 2 * WIDTH * HEIGHT
        - DOOR_WIDTH * DOOR_HEIGHT
        - WINDOW_WIDTH * WINDOW_HEIGHT
    )

    if wall_area <= 0:
        raise ValueError("Invalid door/window dimensions")

    floor_diagonal = hypot(LENGTH, WIDTH)
    room_diagonal = dist(
        (0, 0, 0),
        (LENGTH, WIDTH, HEIGHT)
    )

    tile_area = TILE_WIDTH * TILE_LENGTH
    tiles_exact = floor_area / tile_area

    tiles_round = round(tiles_exact)
    tiles_floor = floor(tiles_exact)
    tiles_ceil = ceil(tiles_exact)

    tiles_to_buy = ceil(tiles_exact * 1.10)

    paint_liters = wall_area * 2 / 10
    paint_cans = ceil(paint_liters / 2.5)

    cost_mul = tiles_to_buy * TILE_PRICE

    cost_sum = 0.0
    for _ in range(tiles_to_buy):
        cost_sum += TILE_PRICE

    print(f"room:          {LENGTH} x {WIDTH} x {HEIGHT} m")
    print(f"floor area:    {floor_area:.2f} m2")
    print(f"wall area:     {wall_area:.2f} m2")
    print(f"floor diag:    {floor_diagonal:.2f} m")
    print(f"room diag:     {room_diagonal:.2f} m")
    print(f"tiles exact:   {tiles_exact:.2f}")
    print(f"  round:       {tiles_round}")
    print(f"  floor:       {tiles_floor}")
    print(f"  ceil:        {tiles_ceil}")
    print(f"tiles to buy:  {tiles_to_buy} (+10% spare)")
    print(f"paint:         {paint_liters:.2f} l -> {paint_cans} cans")
    print(f"tiles cost:    {cost_mul:.2f} UAH")
    print(f"sum == mul:    {cost_sum == cost_mul}")
    print(f"isclose:       {isclose(cost_sum, cost_mul)}")
    print(f"difference:    {abs(cost_sum - cost_mul)}")

except (ValueError, OverflowError) as error:
    print(f"error: {error}", file=sys.stderr)
    sys.exit(1)