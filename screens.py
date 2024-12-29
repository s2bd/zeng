from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from algorithms import drawLine, drawCircle, drawFilledCircle, drawFilledRectangle, drawText
from userinferface import Button
from character import drawCharacter
from shared import showScreen, buttons, W_Width, W_Height
from game import game_screen

try:
    windowConfigFile = open('window.config','r')
except:
    print("window.config file not found!")
windowConfig = windowConfigFile.readlines()
windowConfigFile.close()
W_Width, W_Height = int(windowConfig[0]),int(windowConfig[1])
buttons = []
hovered_button_index, pressed_button_index = -1, -1

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

    back_button_x = (W_Width - 180) // 2 - 100
    buttons.append(Button(back_button_x, 50, 80, 100, "<", label_offset=-20))

    for button in buttons:
        button.draw()

    glutSwapBuffers()