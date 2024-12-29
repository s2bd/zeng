from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
from shared import W_Width, W_Height, showScreen, buttons
from character import drawCharacter
from algorithms import drawText, drawCircle, drawLine, drawFilledCircle

# Game state
mouse_x, mouse_y = 0, 0
character_x, character_y = W_Width // 2, W_Height // 2
bullets = []  # List to store active bullets

# Function to update and render the game screen
def game_screen():
    global bullets
    
    buttons.clear()

    # Draw character facing the mouse
    dx = mouse_x - character_x
    dy = mouse_y - character_y
    angle = math.atan2(dy, dx)

    drawCharacter(character_x, character_y)

    # Draw cursor at the mouse position
    drawCircle(mouse_x, mouse_y, 5, (1.0, 1.0, 0.0))

    # Update and draw bullets
    new_bullets = []
    for bx, by, tx, ty in bullets:
        bullet_speed = 15
        direction_x = tx - bx
        direction_y = ty - by
        distance = math.sqrt(direction_x**2 + direction_y**2)
        direction_x /= distance
        direction_y /= distance

        bx += direction_x * bullet_speed
        by += direction_y * bullet_speed

        # If the bullet is within the screen bounds, keep it
        if 0 <= bx <= W_Width and 0 <= by <= W_Height:
            new_bullets.append((bx, by, tx, ty))

            # Draw the bullet
            drawFilledCircle(bx, by, 5, (1.0, 1.0, 0.0))

            # Draw the gun flash effect (optional)
            if bx == character_x and by == character_y:
                drawFilledCircle(character_x - 40, character_y, 10, (1.0, 0.5, 0.0))

    bullets = new_bullets

    # Draw the score
    drawText(f"Score: {len(bullets)}", 10, W_Height - 30, (1.0, 1.0, 1.0), 0.2)

    glutSwapBuffers()
