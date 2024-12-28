from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from algorithms import drawLine, drawCircle, drawFilledCircle, drawFilledRectangle, drawText
from userinferface import Button
from character import drawCharacter
from shared import showScreen, buttons, W_Width, W_Height

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
    # glutMouseFunc(mouseListener2)
    # glutPassiveMotionFunc(passiveMouseListener2)
    # glutSpecialFunc(specialKeyListener2)
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
    
    drawText("Help", W_Width//2 - 50, W_Height//2, (1.0, 1.0, 1.0), 0.5)

    back_button_x = (W_Width - 180) // 2 + 200
    buttons.append(Button(back_button_x, 50, 80, 100, ">", label_offset=-20))

    for button in buttons:
        button.draw()

    glutSwapBuffers()

def play_screen():
    global buttons
    buttons.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    drawText("Game", W_Width//2 - 50, W_Height//2, (1.0, 1.0, 1.0), 0.5)
    
    glutSwapBuffers()

# Shop screen
def right_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    drawText("Shop", W_Width//2 - 50, W_Height//2, (1.0, 1.0, 1.0), 0.5)

    back_button_x = (W_Width - 180) // 2 - 100
    buttons.append(Button(back_button_x, 50, 80, 100, "<", label_offset=-20))

    for button in buttons:
        button.draw()

    glutSwapBuffers()


'''I/O related functions'''
def mouseListener2(button, state, x, y):
    global buttons, pressed_button_index
    y = W_Height - y  # Invert y-coordinate for OpenGL

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            for index, button_obj in enumerate(buttons):  # Only check active buttons
                if button_obj.left <= x <= button_obj.left + button_obj.width and \
                        button_obj.bottom <= y <= button_obj.bottom + button_obj.height:
                    button_obj.is_pressed = True
                    pressed_button_index = index
                    print(f"Button '{button_obj.label}' pressed!")
        elif state == GLUT_UP:
            if pressed_button_index != -1:
                buttons[pressed_button_index].is_pressed = False
                print(f"Button '{buttons[pressed_button_index].label}' released!")

                if buttons[pressed_button_index].label in [">", "<"]:  # Back buttons
                    glutDisplayFunc(showScreen)
                    glutMouseFunc(None)
                    # glutPassiveMotionFunc(None)
                    # glutSpecialFunc(None)
                    glutPostRedisplay()

                pressed_button_index = -1

    glutPostRedisplay()


def specialKeyListener2(key, x, y):
    if key=='w':
        print("Moving North")
    if key=='a':
        print("Moving West")
    if key== 's':
        print("Moving South")
    if key== 'd':
        print("Moving East")
    glutPostRedisplay()