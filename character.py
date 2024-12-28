from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from algorithms import drawLine, drawCircle, drawFilledCircle, drawFilledRectangle, drawText

recoil = 0.0

# Drawing the player's character sprite
def drawCharacter(x, y, scale=1):
    global recoil
    drawFilledRectangle(x - (40*scale), y + (40*scale), x + (40*scale), y - (50*scale), (1.0, 0.88, 0.74)) # Skin
    drawFilledCircle(x - (24*scale), y + (8*scale), 16*scale, (0.0,0.0,0.0)) # Left Eye outline
    drawFilledCircle(x - (1*scale), y + (8*scale), 16*scale, (0.0,0.0,0.0)) # Right Eye outline
    drawFilledCircle(x - (24*scale), y + (8*scale), 15*scale, (1.0,1.0,1.0)) # Left Eye
    drawFilledCircle(x - (1*scale), y + (8*scale), 15*scale, (1.0,1.0,1.0)) # Right Eye
    drawFilledCircle(x - (24*scale), y + (8*scale), 2*scale, (0.0,0.0,0.0)) # Left Eye pupil
    drawFilledCircle(x - (1*scale), y + (8*scale), 2*scale, (0.0,0.0,0.0)) # Right Eye pupil
    drawFilledRectangle(x - (40*scale), y + (40*scale), x + (40*scale), y + (20*scale), (0.0, 0.0, 0.0)) # Hair
    drawFilledRectangle(x - (40*scale), y + (20*scale), x + (40*scale), y + (18*scale), (0.8, 0.0, 0.0)) # Ribbon
    drawFilledRectangle(x - (40*scale), y - (20*scale), x + (40*scale), y - (50*scale), (0.0, 0.5, 0.0)) # Cloth
    drawFilledRectangle(x - (60*scale) + recoil, y - (15*scale), x + (20*scale) + recoil, y - (40*scale), (0.0, 0.0, 0.0)) # Gun P1
    drawFilledRectangle(x - (70*scale) + recoil, y - (10*scale), x - (60*scale) + recoil, y - (30*scale), (0.0, 0.0, 0.0)) # Gun P2
    drawFilledRectangle(x - (80*scale) + recoil, y - (20*scale), x - (60*scale) + recoil, y - (30*scale), (0.0, 0.0, 0.0)) # Gun P3
    drawFilledRectangle(x + (5*scale) + recoil, y - (20*scale), x + (20*scale) + recoil, y - (35*scale), (1.0, 0.88, 0.74)) # Hand1 P1
    drawFilledRectangle(x + (0*scale) + recoil, y - (20*scale), x + (20*scale) + recoil, y - (25*scale), (1.0, 0.88, 0.74)) # Hand1 P2
    drawFilledRectangle(x - (50*scale) + recoil, y - (20*scale), x - (35*scale) + recoil, y - (35*scale), (1.0, 0.88, 0.74)) # Hand2
    