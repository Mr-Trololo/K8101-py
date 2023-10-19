import time
import K8101

# Display dimensions
WIDTH = 128
HEIGHT = 64

# Box properties
box_size = 8
box_x = 64
box_y = 32
box_speed_x = 2
box_speed_y = 2

K8101.connect()
K8101.backlight(255)

while True:
    K8101.clearAll()
    
    # Draw the box
    K8101.drawFilledRectangle(box_x, box_y, box_size, box_size)

    # Update the box's position
    box_x += box_speed_x
    box_y += box_speed_y

    # Bounce the box off the walls
    if box_x - box_size < 0 or box_x + box_size >= WIDTH:
        box_speed_x = -box_speed_x
    if box_y - box_size < 0 or box_y + box_size >= HEIGHT: 
        box_speed_y = -box_speed_y

    # Delay for a while to control the animation speed
    time.sleep(.1)

