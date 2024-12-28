'''Import statements for dependencies'''
# Essential OpenGL modules
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
# Built-in Python modules
from time import sleep
# Project-specific custom modules
from algorithms import drawLine, drawCircle, drawFilledCircle, drawFilledRectangle, drawText
from userinferface import Button
from character import drawCharacter

'''Global variables/constants'''
W_Width, W_Height = 450,750
buttons = []
hovered_button_index, pressed_button_index = -1, -1

def setup_buttons():
    global buttons
    y_position = 50

    '''Button(left, bottom, width, height, label, labelsize=0.55)'''

    # "Play" button
    play_button_x = (W_Width - 180) // 2
    buttons.append(Button(play_button_x, y_position, 180, 100, "Play", label_offset=-55))

    # Left button
    left_button_x = play_button_x - 100
    buttons.append(Button(left_button_x, y_position, 80, 100, "?", label_offset=-20))

    # Right button
    right_button_x = play_button_x + 200
    buttons.append(Button(right_button_x, y_position, 80, 100, "$", label_offset=-20))


def iterate():
    glViewport(0, 0, W_Width, W_Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_Width, 0.0, W_Height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global buttons, W_Width, W_Height
    glClearColor(0.08, 0.08, 0.08, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    drawText("ZenG", W_Width//2 -150, W_Height//2 +250, (0.1,1.0,0.1), 1.00) # Title
    drawText("423 Group12", W_Width//2 -70, W_Height//2 +280, (0.5,0.5,0.5), 0.15) # Subtitle

    drawCharacter(W_Width//2,W_Height//2)
   
    # Rendering the buttons
    for button in buttons:
        button.draw()
    
    glutSwapBuffers()

def passiveMouseListener(x, y):
    global buttons, hovered_button_index
    y = W_Height - y  # Invert y-coordinate for OpenGL
    hovered_button_index = -1

    for index, button in enumerate(buttons):
        if button.left <= x <= button.left + button.width and button.bottom <= y <= button.bottom + button.height:
            button.is_hovered = True
            hovered_button_index = index
        else:
            button.is_hovered = False
    glutPostRedisplay()

'''I/O related functions'''
def mouseListener(button, state, x, y):
    global buttons, pressed_button_index
    y = W_Height - y  # Invert y-coordinate for OpenGL

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            for index, button_obj in enumerate(buttons):
                if button_obj.left <= x <= button_obj.left + button_obj.width and \
                        button_obj.bottom <= y <= button_obj.bottom + button_obj.height:
                    button_obj.is_pressed = True
                    pressed_button_index = index
                    print(f"Button '{button_obj.label}' pressed!")
        elif state == GLUT_UP:
            if pressed_button_index != -1:
                buttons[pressed_button_index].is_pressed = False
                print(f"Button '{buttons[pressed_button_index].label}' released!")
                pressed_button_index = -1

    glutPostRedisplay()


'''GLUT default initialization, do not touch'''
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
window = glutCreateWindow(b"Zen G - CSE423 Project Group 12")

setup_buttons()
glutDisplayFunc(showScreen)
glutMouseFunc(mouseListener)
glutPassiveMotionFunc(passiveMouseListener)

# Where it all begins
glutMainLoop()