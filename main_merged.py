# Midpoint Line drawing and Midpoint Circle drawing algorithms
# To be used for the Zen G group project

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Read window configuration
try:
    windowConfigFile = open('window.config', 'r')
except:
    print("window.config file not found!")
windowConfig = windowConfigFile.readlines()
windowConfigFile.close()

'''Global variables/constants'''
W_Width, W_Height = int(windowConfig[0]), int(windowConfig[1])
mouse_x, mouse_y = 0, 0
character_x, character_y = W_Width // 2, W_Height // 2
player_health = 100
max_health = 100
bullets = []
recoil = 0.0
buttons = []
hovered_button_index, pressed_button_index = -1, -1
current_screen = 0  # 0: Menu, 1: Help, 2: Shop, 3: Game
score = 0
zombies = []

try:
    saveFile = open('game.save', 'r')
    saveInfo = saveFile.readlines()
    saveFile.close()
except:
    saveFile = open('game.save', 'w')
    saveFile.write(str('0'))
    saveFile.close
    saveFile = open('game.save', 'r')
    saveInfo = saveFile.readlines()
    saveFile.close()

highestScore = saveInfo[0]

def drawLine(x1, y1, x2, y2, color):
    glColor3f(*color)
    glPointSize(2)
    glBegin(GL_POINTS)

    zone = find_zone(x1, y1, x2, y2)
    x1n, y1n = zone_N_to_0(x1, y1, zone)
    x2n, y2n = zone_N_to_0(x2, y2, zone)
    dx, dy = x2n - x1n, y2n - y1n
    d = 2 * dy - dx
    incE, incNE = 2 * dy, 2 * (dy - dx)
    x, y = x1n, y1n

    while x <= x2n:
        glVertex2f(*zone_0_to_N(x, y, zone))
        if d <= 0:
            d += incE
        else:
            d += incNE
            y += 1
        x += 1
    glEnd()

def find_zone(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if abs(dx) >= abs(dy):
        if   dx > 0  and dy > 0:
            return 0
        elif dx < 0  and dy > 0:
            return 3
        elif dx < 0  and dy < 0:
            return 4
        else:
            return 7
    else:
        if   dx > 0  and dy > 0:
            return 1
        elif dx < 0  and dy > 0:
            return 2
        elif dx < 0  and dy < 0:
            return 5
        else:
            return 6

def zone_N_to_0(x, y, zone):
    if zone == 0:
        return  x,  y
    elif zone == 1:
        return  y,  x
    elif zone == 2:
        return  y, -x
    elif zone == 3:
        return -x,  y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y,  x
    elif zone == 7:
        return  x, -y

def zone_0_to_N(x, y, zone):
    if zone == 0:
        return  x,  y
    elif zone == 1:
        return  y,  x
    elif zone == 2:
        return -y,  x
    elif zone == 3:
        return -x,  y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return  y, -x
    elif zone == 7:
        return  x, -y
    
def drawCircle(xi, yi, r, color):
    glColor3f(*color)
    glPointSize(2)
    glBegin(GL_POINTS)
    x, y = 0, r
    d = 1 - r
    while x <= y:
        glVertex2f( x + xi,  y + yi)
        glVertex2f( x + xi, -y + yi)
        glVertex2f(-x + xi,  y + yi)
        glVertex2f(-x + xi, -y + yi)
        glVertex2f( y + xi,  x + yi)
        glVertex2f( y + xi, -x + yi)
        glVertex2f(-y + xi,  x + yi)
        glVertex2f(-y + xi, -x + yi)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * x - 2 * y + 5
            y -= 1
        x += 1
    glEnd()

# Other derivative algorithms for conveniently drawing other shapes based on the algorithms above

def drawFilledCircle(xi, yi, r, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    for y in range(-r, r + 1):
        # Calculate the x-coordinate range for the current y-level
        x_max = int((r**2 - y**2) ** 0.5)  # x-coordinate based on circle equation x^2 + y^2 = r^2
        for x in range(-x_max, x_max + 1):
            glVertex2f(x + xi, y + yi)
    glEnd()


def drawFilledRectangle(x1, y1, x2, y2, color):
    x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    for y in range(y1, y2 + 1):
        drawLine(x1, y, x2, y, color)

# Other functions that rely on GLUT's built-in ones

def drawText(text, x, y, color=(1, 1, 1), scale=0.1):
    glColor3f(*color)  # Set text color
    glPushMatrix()
    glTranslatef(x, y - (119 * scale) / 2, 0)  # Move to position and center vertically
    glScalef(scale, scale, scale)  # Scale the font size
    for char in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
    glPopMatrix()

# UI component - button
class Button:
    def __init__(self, left, bottom, width, height, label, label_size=0.55, label_offset=0):
        self.left = left
        self.bottom = bottom
        self.width = width
        self.height = height
        self.label = label
        self.label_size = label_size
        self.label_offset = label_offset
        self.is_hovered = False
        self.is_pressed = False

    def draw(self):
        # Calculate colors based on state
        primary_color = (0.0, 0.5, 0.0) if self.is_hovered else (0.0, 1.0, 0.0)
        accent_color = (0.0, 0.2, 0.0) if self.is_hovered else (0.0, 0.5, 0.0)
        text_color = (1.0, 1.0, 1.0) if self.is_pressed else (0.0, 0.0, 0.0)
        
        # Adjust height when pressed
        bottom = self.bottom - 10 if self.is_pressed else self.bottom
        top = self.bottom + self.height - 10 if self.is_pressed else self.bottom + self.height

        # Draw button
        drawFilledRectangle(self.left, bottom, self.left + self.width, top, primary_color)  # Main button
        drawFilledRectangle(self.left, bottom - 10, self.left + self.width, bottom, accent_color)  # Accent

        # Calculate text position for centering
        text_x = self.left + self.width // 2 - (len(self.label) * self.label_size * 6) // 2 + self.label_offset
        text_y = 10 + bottom + self.height // 2 - self.label_size * 10 // 2
        drawText(self.label, text_x, text_y, text_color, self.label_size)

        # Highlighting hover state with additional outline
        if self.is_hovered:
            drawFilledRectangle(self.left - 2, bottom - 2, self.left + self.width + 2, top + 2, (1.0, 1.0, 0.0))  # Outline

        glutPostRedisplay()

# Drawing the player's character sprite
def drawCharacter(x, y, scale=1):
    global recoil
    drawFilledRectangle(x - (20*scale), y + (20*scale), x + (20*scale), y - (25*scale), (1.0, 0.88, 0.74)) # Skin
    drawFilledCircle(x - (12*scale), y + (4*scale), 8*scale, (0.0,0.0,0.0)) # Left Eye outline
    drawFilledCircle(x - (0*scale), y + (4*scale), 8*scale, (0.0,0.0,0.0)) # Right Eye outline
    drawFilledCircle(x - (12*scale), y + (4*scale), 7*scale, (1.0,1.0,1.0)) # Left Eye
    drawFilledCircle(x - (0*scale), y + (4*scale), 7*scale, (1.0,1.0,1.0)) # Right Eye
    drawFilledCircle(x - (12*scale), y + (4*scale), 1*scale, (0.0,0.0,0.0)) # Left Eye pupil
    drawFilledCircle(x - (0*scale), y + (4*scale), 1*scale, (0.0,0.0,0.0)) # Right Eye pupil
    drawFilledRectangle(x - (20*scale), y + (20*scale), x + (20*scale), y + (10*scale), (0.0, 0.0, 0.0)) # Hair
    drawFilledRectangle(x - (20*scale), y + (10*scale), x + (20*scale), y + (9*scale), (0.8, 0.0, 0.0)) # Ribbon
    drawFilledRectangle(x - (20*scale), y - (10*scale), x + (20*scale), y - (25*scale), (0.0, 0.5, 0.0)) # Cloth
    drawFilledRectangle(x - (30*scale) + recoil, y - (7*scale), x + (10*scale) + recoil, y - (20*scale), (0.0, 0.0, 0.0)) # Gun P1
    drawFilledRectangle(x - (35*scale) + recoil, y - (5*scale), x - (30*scale) + recoil, y - (15*scale), (0.0, 0.0, 0.0)) # Gun P2
    drawFilledRectangle(x - (40*scale) + recoil, y - (10*scale), x - (30*scale) + recoil, y - (15*scale), (0.0, 0.0, 0.0)) # Gun P3
    drawFilledRectangle(x + (3*scale) + recoil, y - (10*scale), x + (10*scale) + recoil, y - (17*scale), (1.0, 0.88, 0.74)) # Hand1 P1
    drawFilledRectangle(x + (0*scale) + recoil, y - (10*scale), x + (10*scale) + recoil, y - (12*scale), (1.0, 0.88, 0.74)) # Hand1 P2
    drawFilledRectangle(x - (25*scale) + recoil, y - (10*scale), x - (17*scale) + recoil, y - (17*scale), (1.0, 0.88, 0.74)) # Hand2
    
def drawZombie(x, y, scale=1):
    global recoil
    drawFilledRectangle(x - (20*scale), y + (20*scale), x + (20*scale), y - (25*scale), (0.0, 0.88, 0.04)) # Skin
    drawFilledCircle(x - (12*scale), y + (4*scale), 8*scale, (0.0,0.0,0.0)) # Left Eye outline
    drawFilledCircle(x - (0*scale), y + (4*scale), 8*scale, (0.0,0.0,0.0)) # Right Eye outline
    drawFilledCircle(x - (12*scale), y + (4*scale), 7*scale, (0.0,0.0,0.0)) # Left Eye
    drawFilledCircle(x - (0*scale), y + (4*scale), 7*scale, (0.0,0.0,0.0)) # Right Eye
    drawFilledCircle(x - (12*scale), y + (4*scale), 1*scale, (1.0,0.0,0.0)) # Left Eye pupil
    drawFilledCircle(x - (0*scale), y + (4*scale), 1*scale, (1.0,0.0,0.0)) # Right Eye pupil
    drawFilledRectangle(x - (20*scale), y + (20*scale), x + (20*scale), y + (10*scale), (0.0, 0.0, 0.0)) # Hair
    drawFilledRectangle(x - (20*scale), y + (10*scale), x + (20*scale), y + (9*scale), (0.8, 0.0, 0.0)) # Ribbon
    drawFilledRectangle(x - (20*scale), y - (10*scale), x + (20*scale), y - (25*scale), (0.0, 0.5, 0.0)) # Cloth

'''I/O related functions'''

def mouseListener(button, state, x, y):
    """Handles mouse clicks for all screens."""
    global buttons, pressed_button_index, current_screen, mouse_x, mouse_y, bullets
    y = W_Height - y  # Convert mouse coordinates to OpenGL's system
    mouse_x, mouse_y = x, y

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            # Check if any button is clicked
            for index, button_obj in enumerate(buttons):
                if button_obj.left <= x <= button_obj.left + button_obj.width and \
                   button_obj.bottom <= y <= button_obj.bottom + button_obj.height:
                    button_obj.is_pressed = True
                    pressed_button_index = index
                    print(f"Button '{button_obj.label}' pressed!")

            # If in game screen, handle shooting
            if current_screen == 3:
                bullets.append((character_x, character_y, mouse_x, mouse_y))
            if current_screen == "game_over":
                if pressed_button_index == 0:  # Retry
                    current_screen = 3
                    game_screen()
                elif pressed_button_index == 1:  # OK
                    current_screen = 0
                    showScreen()

        elif state == GLUT_UP:
            # Handle button release actions
            if pressed_button_index != -1:
                buttons[pressed_button_index].is_pressed = False
                print(f"Button '{buttons[pressed_button_index].label}' released!")

                # Perform actions based on screen and button
                if current_screen == 0:  # Menu screen
                    if pressed_button_index == 0:  # Play button
                        current_screen = 3
                        play_action()
                    elif pressed_button_index == 1:  # Help button
                        current_screen = 1
                        help_action()
                    elif pressed_button_index == 2:  # Shop button
                        current_screen = 2
                        shop_action()
                elif current_screen in [1, 2]:  # Help or Shop screen
                    current_screen = 0
                    glutDisplayFunc(showScreen)
                    glutPostRedisplay()

                pressed_button_index = -1

    glutPostRedisplay()


def passiveMouseListener(x, y):
    """Handles mouse hovering for all screens."""
    global buttons, hovered_button_index, mouse_x, mouse_y
    y = W_Height - y  # Convert mouse coordinates to OpenGL's system
    mouse_x, mouse_y = x, y

    new_hovered_button_index = -1

    for index, button in enumerate(buttons):
        # Check if the mouse is within the button's bounds
        if button.left <= x <= button.left + button.width and button.bottom <= y <= button.bottom + button.height:
            button.is_hovered = True
            new_hovered_button_index = index
        else:
            button.is_hovered = False

    # Trigger re-render if hover state changes
    if new_hovered_button_index != hovered_button_index:
        hovered_button_index = new_hovered_button_index
        glutPostRedisplay()


def keyboardListener(key, x, y):
    """Handles keyboard input for all screens."""
    global character_x, character_y

    movement_speed = 10

    # Handle game-specific controls
    if current_screen == 3:
        if key == b'w' and character_y + 25 < W_Height:
            character_y += movement_speed
        elif key == b's' and character_y - 25 > 0:
            character_y -= movement_speed
        elif key == b'a' and character_x - 20 > 0:
            character_x -= movement_speed
        elif key == b'd' and character_x + 20 < W_Width:
            character_x += movement_speed
    else:
        # Handle menu-specific controls if needed
        pass

    glutPostRedisplay()

def drawHealthBar():
    health_ratio = player_health / max_health
    bar_width = 200
    drawFilledRectangle(10, W_Height - 20, 10 + int(bar_width * health_ratio), W_Height - 10, (1.0, 0.0, 0.0))

def drawGameOverScreen():
    drawFilledRectangle(W_Width//4, W_Height//3, 3*W_Width//4, 2*W_Height//3, (0.0, 0.0, 0.0))
    drawText("Game Over", W_Width//2 - 100, W_Height//2 + 50, (1.0, 1.0, 1.0), 0.25)
    
    retry_button = Button(W_Width//2 - 150, W_Height//2 - 50, 100, 50, "Retry",0.25,-20)
    ok_button = Button(W_Width//2 + 50, W_Height//2 - 50, 100, 50, "OK",0.25,-20)

    retry_button.draw()
    ok_button.draw()
    
    buttons.append(retry_button)
    buttons.append(ok_button)


# Function to update and render the game screen
def game_screen():
    global bullets, score, character_x, character_y, player_health, max_health
    zombies = []
    score = 0

    buttons.clear()

    # Draw character facing the mouse
    dx = mouse_x - character_x
    dy = mouse_y - character_y
    angle = math.atan2(dy, dx)

    drawCharacter(character_x, character_y)

    # Draw cursor at the mouse position
    drawCircle(mouse_x, mouse_y, 8, (1.0, 1.0, 0.0))

    # Spawn new zombies at random x-coordinates from the bottom
    if len(zombies) < 10:  # Limit the number of zombies
        spawn_x = random.randint(20, W_Width - 20)  # Ensure zombies spawn within bounds
        zombies.append((spawn_x, 0))  # Bottom of the window

    # Updating zombies
    new_zombies = []
    for zx, zy in zombies:
        zy += 2  # Move zombie upwards
        if zy > W_Height:  # If the zombie crosses the top
            player_health -= 10
        else:
            new_zombies.append((zx, zy))
            drawZombie(zx, zy)
    zombies = new_zombies

    # Player-zombie interaction
    for zx, zy in zombies:
        distance_to_player = math.sqrt((character_x - zx) ** 2 + (character_y - zy) ** 2)
        if distance_to_player < 30:  # Collision radius
            player_health -= 10  # Lose health for each frame of contact

    # Check collisions between bullets and zombies
    new_bullets = []
    updated_zombies = []
    for bx, by, tx, ty in bullets:
        bullet_hit = False
        for zx, zy in zombies:
            distance_to_bullet = math.sqrt((bx - zx) ** 2 + (by - zy) ** 2)
            if distance_to_bullet < 20:  # If the bullet hits the zombie
                bullet_hit = True
                score += 1  # Increase score for killing the zombie
                break
        if not bullet_hit:
            new_bullets.append((bx, by, tx, ty))
    zombies = [zombie for zombie in zombies if zombie not in updated_zombies]
    bullets = new_bullets

    # Draw player
    drawCharacter(character_x, character_y)

    # Update and draw bullets
    for bx, by, tx, ty in bullets:
        drawLine(bx, by, tx, ty, (1.0, 0.0, 0.0))

    # Draw health bar
    def drawHealthBar():
        drawFilledRectangle(W_Width - 100, W_Height - 10, 1 + player_health, W_Height - 15, (1.0, 0.0, 0.0))

    drawHealthBar()

    # Draw score
    drawText(f"Curr: {str(score)}", 10, W_Height - 40, (1.0, 1.0, 1.0), 0.2)
    drawText(f"Best: {str(highestScore)}", 10, W_Height - 65, (1.0, 1.0, 0.0), 0.2)

    # Game over condition
    if player_health <= 0:
        drawGameOverScreen()
        return

    glutSwapBuffers()

def setup_buttons():
    global buttons
    y_position = 50

    '''Button(left, bottom, width, height, label, labelsize=0.55)'''

    # "Play" button
    play_button_x = (W_Width - 180) // 2
    buttons.append(Button(play_button_x, y_position, 180, 100, "Play", label_offset=-55))

    # Help button
    left_button_x = play_button_x - 100
    buttons.append(Button(left_button_x, y_position, 80, 100, "?", label_offset=-20))

    # Shop button
    right_button_x = play_button_x + 200
    buttons.append(Button(right_button_x, y_position, 80, 100, "$", label_offset=-20))

def showScreen():
    global buttons, W_Width, W_Height
    buttons.clear()  # Clear existing buttons
    setup_buttons()  # Reconfigure buttons for the menu screen
    glClearColor(0.18, 0.18, 0.18, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, W_Width, W_Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_Width, 0.0, W_Height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    drawText("ZenG", W_Width//2 - 150, W_Height//2 + 250, (0.1, 1.0, 0.1), 1.00)  # Title
    drawText("423 Group12", W_Width//2 - 70, W_Height//2 + 280, (0.5, 0.5, 0.5), 0.15)  # Subtitle

    drawCharacter(W_Width//2, W_Height//2, 2)

    # Render buttons
    for button in buttons:
        button.draw()

    glutSwapBuffers()

# 3-button actions
def play_action():
    global buttons
    buttons.clear()  # Clear buttons from the menu screen
    glutDisplayFunc(play_screen)
    glutPostRedisplay()

def help_action():
    global buttons
    buttons.clear()  # Clear buttons from the menu screen
    glutDisplayFunc(left_screen)
    glutPostRedisplay()

def shop_action():
    global buttons
    buttons.clear()  # Clear buttons from the menu screen
    glutDisplayFunc(right_screen)
    glutPostRedisplay()


# Help screen
def left_screen():
    global buttons
    buttons.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    drawText("Help", W_Width//2 - 180, W_Height - 50, (1.0, 1.0, 1.0), 0.5)
    drawText("Move using W,A,S,D", W_Width//2 - 180, W_Height - 100, (0.9, 0.9, 0.9), 0.16)
    drawText("Aim & shoot using the mouse", W_Width//2 - 180, W_Height - 120, (0.9, 0.9, 0.9), 0.16)
    drawText("Survive as long as you can!", W_Width//2 - 180, W_Height - 140, (0.9, 0.9, 0.9), 0.16)

    back_button_x = (W_Width - 180) // 2 + 200
    buttons.append(Button(back_button_x, 50, 80, 100, ">", label_offset=-20))

    for button in buttons:
        button.draw()

    glutSwapBuffers()

def play_screen():
    global buttons
    buttons.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    game_screen()
    
    glutSwapBuffers()

# Shop screen
def right_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    drawText("Shop", W_Width//2 - 180, W_Height - 50, (1.0, 1.0, 1.0), 0.5)
    drawText("Coming Soon", W_Width//2 - 150, W_Height//2, (0.9, 0.001, 0.001), 0.25)
    drawText(f"${highestScore}", W_Width - 120, W_Height - 50, (0.9, 0.9, 0.0), 0.5)

    back_button_x = (W_Width - 180) // 2 - 100
    buttons.append(Button(back_button_x, 50, 80, 100, "<", label_offset=-20))

    for button in buttons:
        button.draw()

    glutSwapBuffers()

def iterate():
    glViewport(0, 0, W_Width, W_Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_Width, 0.0, W_Height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def animate():
    glutPostRedisplay()

'''GLUT default initialization, do not touch'''
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
window = glutCreateWindow(b"Zen G - CSE423 Project Group 12")

glutDisplayFunc(showScreen)
glutMouseFunc(mouseListener)
glutPassiveMotionFunc(passiveMouseListener)
glutKeyboardFunc(keyboardListener)
glutIdleFunc(animate)

# Where it all begins
glutMainLoop()