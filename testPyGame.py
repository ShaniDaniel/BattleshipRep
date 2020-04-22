# Example of UI using pygame package- creating a cube the changes it's color when pressing the space key
# and can be moved around the screen without leaving it's borders.

import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False
is_pink = True
x = 30
y = 30
clock = pygame.time.Clock()

# Setting screen height and width, and setting parameters for future use
# (clock function delays the programs response so it wont move too fast, and will be activated at the end of the code).

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # Sets that pressing X at the screen corner will quit the program

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_pink = not is_pink
        # Pressing the space key will change the cube's color

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] and y > 0:
        y -= 4
    if pressed[pygame.K_DOWN] and y < 240:
        y += 4
    if pressed[pygame.K_RIGHT] and x < 340:
        x += 4
    if pressed[pygame.K_LEFT] and x > 0:
        x -= 4
    # Pressing the keyboard arrow keys accordingly will move the cube.

    screen.fill((0, 0, 0))
    # Setting the screen black

    if is_pink:
        color = (160, 0, 90)
    else:
        color = (200, 170, 0)
    # Setting the cube's color to change between pink and yellow (RGB values).

    pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
    # Creating the cube and it's shape and size, positioned at x and y coordinates so it will move accordingly.

    pygame.display.flip()
    clock.tick(60)
    # will block execution until 1/60 seconds have passed
    # since the previous time clock.tick was called.
