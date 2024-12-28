'''Import statements for dependencies'''
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from time import sleep
from algorithms import drawLine, drawCircle, drawFilledRectangle, drawText
''' Highlights of the syntax:
drawLine(x1, y1, x2, y2, color), drawCircle(xi, yi, r, color), drawFilledRectangle(x1, y1, x2, y2, color), \
    drawText(text, x, y, color, scale)
'''

'''Global variables/constants'''
W_Width, W_Height = 450,750
buttons = []
hovered_button_index, pressed_button_index = -1, -1

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

 

def setup_buttons():
    global buttons
    y_position = 50

    '''Button(left, bottom, width, height, label, labelsize=0.55)'''

    # "Play" button
    play_button_x = (W_Width - 180) // 2
    buttons.append(Button(play_button_x, y_position, 180, 100, "Play", label_offset=-55))


    # Left button
    left_button_x = play_button_x - 100
    buttons.append(Button(left_button_x, y_position, 80, 100, "<", label_offset=-25))

    # Right button
    right_button_x = play_button_x + 200
    buttons.append(Button(right_button_x, y_position, 80, 100, ">", label_offset=-20))

def iterate():
    glViewport(0, 0, W_Width, W_Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_Width, 0.0, W_Height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global buttons, W_Width, W_Height
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    drawText("ZenG", W_Width//2 -150, W_Height//2 +250, (0.1,1.0,0.1), 1.00) # Title
    drawText("423 Group12", W_Width//2 -70, W_Height//2 +280, (0.5,0.5,0.5), 0.15) # Subtitle
   
    # Rendering the buttons
    for button in buttons:
        button.draw()
    
    glutSwapBuffers() # Default function for GLUT

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