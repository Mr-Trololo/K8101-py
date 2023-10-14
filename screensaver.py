import random
import time
import k8101

# Display dimensions
WIDTH = 128
HEIGHT = 64

# Box properties
box_size = 2
box_x = random.randint(box_size, WIDTH - box_size)
box_y = random.randint(box_size, HEIGHT - box_size)
box_speed_x = 2
box_speed_y = 2

while True:
    k8101.clearAll()
    k8101.backlight(10)
    # Draw the box
    for y in range(max(0, box_y - box_size), min(HEIGHT, box_y + box_size)):
        for x in range(max(0, box_x - box_size), min(WIDTH, box_x + box_size)):
            k8101.drawPixel(x, y)

    # Update the box's position
    box_x += box_speed_x
    box_y += box_speed_y

    # Bounce the box off the walls
    if box_x - box_size < 0 or box_x + box_size >= WIDTH:
        box_speed_x = -box_speed_x
    if box_y - box_size < 0 or box_y + box_size >= HEIGHT:
        box_speed_y = -box_speed_y

    # Delay for a while to control the animation speed
    time.sleep(1)
