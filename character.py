from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from algorithms import drawLine, drawCircle, drawFilledCircle, drawFilledRectangle, drawText

recoil = 0.0

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
    