# Midpoint Line drawing and Midpoint Circle drawing algorithms
# To be used for the Zen G group project

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

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
