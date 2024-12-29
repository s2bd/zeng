'''Import statements for dependencies'''
# Essential OpenGL modules
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
# Project-specific custom modules
from algorithms import drawLine, drawCircle, drawFilledCircle, drawFilledRectangle, drawText
from userinferface import Button
from screens import play_action, help_action, shop_action
from shared import buttons, hovered_button_index, pressed_button_index, showScreen, W_Width, W_Height, current_screen
from character import drawCharacter
from controls import passiveMouseListener, mouseListener, keyboardListener


def iterate():
    glViewport(0, 0, W_Width, W_Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_Width, 0.0, W_Height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


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

# Where it all begins
glutMainLoop()