'''Import statements for dependencies'''
# Essential OpenGL modules
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
# Project-specific custom modules
from algorithms import drawLine, drawCircle, drawFilledCircle, drawFilledRectangle, drawText
from userinferface import Button
from screens import play_action, help_action, shop_action
from shared import buttons, showScreen, W_Width, W_Height, current_screen
from character import drawCharacter

'''Global variables/constants'''
hovered_button_index, pressed_button_index = -1, -1

def iterate():
    glViewport(0, 0, W_Width, W_Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_Width, 0.0, W_Height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

'''I/O related functions'''
def mouseListener(button, state, x, y):
    global buttons, pressed_button_index, current_screen
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

                # Handle actions based on the current screen
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
    global buttons, hovered_button_index
    y = W_Height - y  # Invert y-coordinate for OpenGL
    new_hovered_button_index = -1

    for index, button in enumerate(buttons):
        # Check if the mouse is within the button's bounds
        if button.left <= x <= button.left + button.width and button.bottom <= y <= button.bottom + button.height:
            button.is_hovered = True
            new_hovered_button_index = index
        else:
            button.is_hovered = False

    # Only trigger re-render if hover state changes
    if new_hovered_button_index != hovered_button_index:
        hovered_button_index = new_hovered_button_index
        glutPostRedisplay()

def specialKeyListener(key, x, y):
    if key=='w':
        print("Moving North")
    if key=='a':
        print("Moving West")
    if key== 's':
        print("Moving South")
    if key== 'd':
        print("Moving East")
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
glutSpecialFunc(specialKeyListener)

# Where it all begins
glutMainLoop()