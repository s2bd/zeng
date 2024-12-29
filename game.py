from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
from shared import W_Width, W_Height, showScreen
from character import drawCharacter

# Global variables
player_position = [W_Width // 2, W_Height // 2]
player_size = 20
player_speed = 5
bullets = []
zombies = []
zombie_speed = 2
tile_size = 40
world = []
mouse_position = [0, 0]

# Initialize the world with random tiles
def generate_world():
    global world
    cols = W_Width // tile_size
    rows = W_Height // tile_size
    world = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

def draw_world():
    for row_idx, row in enumerate(world):
        for col_idx, tile in enumerate(row):
            if tile == 1:  # Draw a solid tile
                x = col_idx * tile_size
                y = row_idx * tile_size
                glColor3f(0.5, 0.5, 0.5)
                glBegin(GL_QUADS)
                glVertex2f(x, y)
                glVertex2f(x + tile_size, y)
                glVertex2f(x + tile_size, y + tile_size)
                glVertex2f(x, y + tile_size)
                glEnd()

# Handle player movement
def move_player(keys):
    if b'w' in keys:
        player_position[1] += player_speed
    if b's' in keys:
        player_position[1] -= player_speed
    if b'a' in keys:
        player_position[0] -= player_speed
    if b'd' in keys:
        player_position[0] += player_speed

    # Keep player within bounds
    player_position[0] = max(0, min(player_position[0], W_Width - player_size))
    player_position[1] = max(0, min(player_position[1], W_Height - player_size))

# Draw bullets
def draw_bullets():
    glColor3f(1, 1, 0)
    for bullet in bullets:
        glBegin(GL_QUADS)
        glVertex2f(bullet[0] - 5, bullet[1] - 5)
        glVertex2f(bullet[0] + 5, bullet[1] - 5)
        glVertex2f(bullet[0] + 5, bullet[1] + 5)
        glVertex2f(bullet[0] - 5, bullet[1] + 5)
        glEnd()

# Draw zombies
def draw_zombies():
    glColor3f(1, 0, 0)
    for zombie in zombies:
        glBegin(GL_QUADS)
        glVertex2f(zombie[0] - 15, zombie[1] - 15)
        glVertex2f(zombie[0] + 15, zombie[1] - 15)
        glVertex2f(zombie[0] + 15, zombie[1] + 15)
        glVertex2f(zombie[0] - 15, zombie[1] + 15)
        glEnd()

# Update bullets
def update_bullets():
    for bullet in bullets[:]:
        bullet[0] += bullet[2] * 10
        bullet[1] += bullet[3] * 10
        if bullet[0] < 0 or bullet[0] > W_Width or bullet[1] < 0 or bullet[1] > W_Height:
            bullets.remove(bullet)

# Update zombies
def update_zombies():
    for zombie in zombies:
        dx = player_position[0] - zombie[0]
        dy = player_position[1] - zombie[1]
        dist = (dx**2 + dy**2)**0.5
        if dist > 0:
            zombie[0] += zombie_speed * dx / dist
            zombie[1] += zombie_speed * dy / dist

# Mouse callback
def mouse_motion(x, y):
    global mouse_position
    mouse_position = [x, W_Height - y]

# Mouse click callback
def mouse_click(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        dx = mouse_position[0] - player_position[0]
        dy = mouse_position[1] - player_position[1]
        dist = (dx**2 + dy**2)**0.5
        if dist > 0:
            bullets.append([player_position[0], player_position[1], dx / dist, dy / dist])

# Keyboard callback
def keyboard_down(key, x, y):
    keys_down.add(key)

def keyboard_up(key, x, y):
    keys_down.discard(key)

# Main display function
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_world()
    drawCharacter(player_position[0], player_position[1], player_size)
    draw_bullets()
    draw_zombies()

    glutSwapBuffers()

# Timer function
def update(value):
    move_player(keys_down)
    update_bullets()
    update_zombies()
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

# Initialize game screen
def game_screen():
    global keys_down
    keys_down = set()
    generate_world()

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard_down)
    glutKeyboardUpFunc(keyboard_up)
    glutMouseFunc(mouse_click)
    glutPassiveMotionFunc(mouse_motion)
    glutTimerFunc(16, update, 0)

    showScreen()
