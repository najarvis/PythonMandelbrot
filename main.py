import pygame
import math

def mandel_func(z, c):
    return z**2 + c

def mandel_recursive(z, c, iterations):
    if iterations <= 1:
        return mandel_func(z, c)

    return mandel_recursive(mandel_func(z, c), c, iterations - 1)

def check_modulus(c):
    return c.real * c.real + c.imag * c.imag > 4

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

num_colors = 15
color_stops = ((0, 7, 100),
               (32, 107, 203),
               (237, 255, 255),
               (255, 170, 0),
               (0, 2, 0))

colors = [(lerp(color_stops[i][0], color_stops[i+1][0], t / (num_colors / len(color_stops))),
           lerp(color_stops[i][1], color_stops[i+1][1], t / (num_colors / len(color_stops))),
           lerp(color_stops[i][2], color_stops[i+1][2], t / (num_colors / len(color_stops)))) for i in range(-1, len(color_stops)-1) for t in range(num_colors // len(color_stops))]

def get_color(c, max_iterations):
    i = 0
    curr_z = complex(0)
    while i < max_iterations:
        curr_z = mandel_func(curr_z, c)
        if check_modulus(curr_z):
            return colors[i % len(colors)]
        i += 1

    return (0, 0, 0)

w, h = 512, 512
ratio = w / h
scale = 0.1
s = w * scale
screen = pygame.display.set_mode((w, h))
surf = pygame.Surface((w, h))

def pos_to_complex(x, y, bounds=(-2.5, -1.5, 1, 1.5)):
    min_x, max_x = bounds[0], bounds[2]
    min_y, max_y = bounds[1], bounds[3]

    r = lerp(min_x, max_x, x / w)
    i = lerp(min_y, max_y, y / h)
    return complex(r, i)

def complex_to_pos(r, i, bounds=(-2.5, -1.5, 1, 1.5)):
    min_x, max_x = bounds[0], bounds[2]
    min_y, max_y = bounds[1], bounds[3]

    x = (r * w - w * min_x) / (-min_x + max_x)
    y = (i * h - h * min_y) / (-min_y + max_y)

    return (x, y)

current_bounds = (-2.5, -1.5, 1, 1.5)

surf.lock()
for y in range(h):
    for x in range(w):
        surf.set_at((x, y), get_color(pos_to_complex(x, y, current_bounds), 100))
surf.unlock()
pygame.image.save(surf, "LastImage.png")

c = pygame.time.Clock()
zoom_number = 1

done = False
while not done:
    c.tick(60)
    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos1 = pos_to_complex(pos[0] - s / 2, pos[1] - (s / ratio) / 2, current_bounds)
            pos2 = pos_to_complex(pos[0] + s / 2, pos[1] + (s / ratio) / 2, current_bounds)
            current_bounds = (pos1.real, pos1.imag, pos2.real, pos2.imag)

            pygame.display.set_caption("Working...")
            zoom_number += 1 / scale 
            surf.lock()
            for y in range(h):
                for x in range(w):
                    surf.set_at((x, y), get_color(pos_to_complex(x, y, current_bounds), 100 + 4 * zoom_number))
            surf.unlock()

            pygame.display.set_caption("Done!")

            pygame.image.save(surf, "LastImage.png")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        scale = min(1, scale + 0.01)
        s = w * scale
    if keys[pygame.K_DOWN]:
        scale = max(0.01, scale - 0.01)
        s = w * scale
    if keys[pygame.K_SPACE]:
        print(pos_to_complex(*pos, current_bounds))

    screen.blit(surf, (0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (pos[0] - s / 2, pos[1] - (s / ratio) / 2, s, s / ratio), 1)

    pygame.display.set_caption(str(pos_to_complex(*pygame.mouse.get_pos(), current_bounds)))

    pygame.display.update()

pygame.quit()
