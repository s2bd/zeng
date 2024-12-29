from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from algorithms import drawText
from character import drawCharacter
from userinferface import Button

# Read window configuration
try:
    windowConfigFile = open('window.config', 'r')
except:
    print("window.config file not found!")
windowConfig = windowConfigFile.readlines()
windowConfigFile.close()

'''Global variables/constants'''
W_Width, W_Height = int(windowConfig[0]), int(windowConfig[1])
buttons = []
hovered_button_index, pressed_button_index = -1, -1
current_screen = 0  # 0: Menu, 1: Help, 2: Shop, 3: Game


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
