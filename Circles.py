import math
import os
import random
from PIL import Image

OUTER_CIRCLE_RADIUS = 100
CIRCLE_COUNT = 3
BREAK_CHANCE = 0.125

# Monitor proportions
INIT_WIDTH = 1920
INIT_HEIGHT = 1028

COLOURS = (
    (27, 28, 23), # BLACK
    (218, 205, 199), # WHITE
    (224, 53, 43), # RED
    (78, 88, 139), # BLUE 
    (215, 168, 64) # YELLOW
    #(150, 154, 165) # GREY
)
BG_COLOUR = COLOURS[0]  

def fit(v, base):
    return base * round(v / base)

def generate_circle_points(r):
    quadrants = [[] for _ in range(4)]
    boundaries = (
        (( 0, r), (-r, 0)),
        ((-r, 0), (-r, 0)),
        ((-r, 0), ( 0, r)),
        (( 0, r), ( 0, r))
    )
    
    for i, ((x_start, x_end), (y_start, y_end)) in enumerate(boundaries):
        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                d = math.sqrt((x + 0.5) ** 2 + (y + 0.5) ** 2)
                if d <= r:
                    quadrants[i].append((x, y))
                
    return quadrants

def generate():
    image = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOUR)
    pixels = image.load()

    for y1 in range(OUTER_CIRCLE_RADIUS, HEIGHT - OUTER_CIRCLE_RADIUS, OUTER_CIRCLE_RADIUS):
        for x1 in range(OUTER_CIRCLE_RADIUS, WIDTH - OUTER_CIRCLE_RADIUS, OUTER_CIRCLE_RADIUS):

            colour = random.choice(COLOURS)
            if colour == BG_COLOUR:
                continue

            for y2 in range(y1, y1 + OUTER_CIRCLE_RADIUS):
                for x2 in range(x1, x1 + OUTER_CIRCLE_RADIUS):
                    if 0 <= x2 < WIDTH and 0 <= y2 < HEIGHT:
                        pixels[x2, y2] = colour
                    
    for y1 in range(OUTER_CIRCLE_RADIUS, HEIGHT, OUTER_CIRCLE_DIAMETER):
        for x1 in range(OUTER_CIRCLE_RADIUS, WIDTH, OUTER_CIRCLE_DIAMETER):
            for circle_points in CIRCLE_POINTS:
                i1 = random.randrange(len(QUADRANT_SETS))
                
                for i2 in (0, 1):
                    colour = random.choice(COLOURS)
                    
                    for i3 in QUADRANT_SETS[i1][i2]:
                        if random.random() <= BREAK_CHANCE:
                            continue
                        
                        for (x_offset, y_offset) in circle_points[i3]:
                            x2 = x1 + x_offset 
                            y2 = y1 + y_offset
                            if 0 <= x2 < WIDTH and 0 <= y2 < HEIGHT:
                                pixels[x2, y2] = colour
            
    os.makedirs(r'.\Art\Generated Images', exist_ok=True)   
    image.save(r'.\Art\Generated Images\Circles 2.png')
    image.show()
    
OUTER_CIRCLE_DIAMETER = OUTER_CIRCLE_RADIUS * 2

WIDTH = fit(INIT_WIDTH, OUTER_CIRCLE_DIAMETER)
HEIGHT = fit(INIT_HEIGHT, OUTER_CIRCLE_DIAMETER)

CIRCLE_POINTS = tuple(
    generate_circle_points(OUTER_CIRCLE_RADIUS // o) for o in range(1, CIRCLE_COUNT + 1)
)

QUADRANT_SETS = [
    (qp, tuple(
        (q + 2) % 4 for q in qp)
    ) for qp in
        ((q, (q + 1) % 4) for q in range(4))
]

QUADRANT_SETS.extend(
    (qp, tuple(
        (q + 1) % 4 for q in qp)
    ) for qp in ((q, (q + 2) % 4) for q in range(0, 4, 2))
)

if __name__ == '__main__':
    generate()
