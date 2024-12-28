from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from algorithms import drawLine, drawCircle, drawFilledRectangle, drawText

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